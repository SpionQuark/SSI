import pytest

from modules.lexer import Lexer
from modules.helpers import SSIError
from modules.parser import Parser
from modules.nodes import *

def lex(source):
    """Tokenize and return a list of (type, value) tuples."""
    return [(t.type, t.value) for t in Lexer(source).tokenize()]

def lex_full(source):
    """Tokenize and return a list of (type, value, line) tuples."""
    return [(t.type, t.value, t.line) for t in Lexer(source).tokenize()]

def lex_error(source):
    """Tokenize source, expect an SSIError, and return it."""
    with pytest.raises(SSIError) as info:
        Lexer(source).tokenize()
    return info.value

def test_empty_source():
    assert lex("") == [("EOF", None)]

def test_only_whitespace():
    assert lex("  \n\t \n") == [("EOF", None)]

def test_keywords_vs_identifiers():
    assert lex("if iffy for i") == [
        ("IF", "if"), ("IDENTIFIER", "iffy"), ("FOR", "for"), ("IDENTIFIER", "i"), ("EOF", None)
    ]

def test_identifier_with_underscore_and_digits():
    assert lex("my_var2") == [("IDENTIFIER", "my_var2"), ("EOF", None)]

def test_number():
    assert lex("42") == [("NUMBER", "42"), ("EOF", None)]

def test_single_equals():
    assert lex("x = 1") == [("IDENTIFIER", "x"), ("ASSIGN", "="), ("NUMBER", "1"), ("EOF", None)]

def test_double_equals():
    assert lex("x == 1") == [("IDENTIFIER", "x"), ("EQUALS", "=="), ("NUMBER", "1"), ("EOF", None)]

def test_separate_equals_stay_separate():
    assert [t for t, _ in lex("x = = 1")] == ["IDENTIFIER", "ASSIGN", "ASSIGN", "NUMBER", "EOF"]

def test_greater_than():
    assert lex("x > 0") == [("IDENTIFIER", "x"), ("GREATER_THAN", ">"), ("NUMBER", "0"), ("EOF", None)]

def test_plus():
    assert lex("1 + 2") == [("NUMBER", "1"), ("PLUS", "+"), ("NUMBER", "2"), ("EOF", None)]

def test_if_return_with_braces():
    assert lex_full("if x > 0 {\n    return x }") == [
        ("IF", "if", 1), ("IDENTIFIER", "x", 1), ("GREATER_THAN", ">", 1),
        ("NUMBER", "0", 1), ("LBRACE", "{", 1),
        ("RETURN", "return", 2), ("IDENTIFIER", "x", 2), ("RBRACE", "}", 2), ("EOF", None, 2),
    ]

def test_double_equals_in_if():
    assert lex_full("if x == 10 {\n    return x }") == [
        ("IF", "if", 1), ("IDENTIFIER", "x", 1), ("EQUALS", "==", 1),
        ("NUMBER", "10", 1), ("LBRACE", "{", 1),
        ("RETURN", "return", 2), ("IDENTIFIER", "x", 2), ("RBRACE", "}", 2), ("EOF", None, 2),
    ]

def test_parens_in_call():
    assert lex("print(x)") == [
        ("IDENTIFIER", "print"), ("LPAREN", "("), ("IDENTIFIER", "x"), ("RPAREN", ")"), ("EOF", None),
    ]

def test_line_numbers_across_blank_lines():
    tokens = lex_full("x\n\n\ny")
    assert tokens == [("IDENTIFIER", "x", 1), ("IDENTIFIER", "y", 4), ("EOF", None, 4)]

def test_string():
    assert lex_full('x = "hello"\ny = "world"\n print(x + " " + y)') == [
        ("IDENTIFIER", "x", 1), ("ASSIGN", "=", 1), ("STRING", "hello", 1),
        ("IDENTIFIER", "y", 2), ("ASSIGN", "=", 2), ("STRING", "world", 2),
        ("IDENTIFIER", "print", 3), ("LPAREN", "(", 3), ("IDENTIFIER", "x", 3),
        ("PLUS", "+", 3), ("STRING", " ", 3), ("PLUS", "+", 3),
        ("IDENTIFIER", "y", 3), ("RPAREN", ")", 3), ("EOF", None, 3),
    ]


def test_empty_string():
    assert lex('""') == [("STRING", ""), ("EOF", None),]


def test_string_keeps_keywords_as_text():
    assert lex('"if while"') == [("STRING", "if while"), ("EOF", None)]


def test_unterminated_string():
    error = lex_error('x = "hello')
    assert error.line == 1


def test_string_across_lines_is_an_error():
    error = lex_error('x = "hello\n"')
    assert error.line == 1

def test_unknown_character():
    error = lex_error("x = @")
    assert error.line == 1


def test_error_reports_correct_line():
    error = lex_error("x = 1\ny = 2\nz = @")
    assert error.line == 3

@pytest.mark.parametrize("source, expected", [
    ("a <= b", [("IDENTIFIER", "a"), ("LESS_EQUAL", "<="), ("IDENTIFIER", "b"), ("EOF", None)]),
    ("a >= b", [("IDENTIFIER", "a"), ("GREATER_EQUAL", ">="), ("IDENTIFIER", "b"), ("EOF", None)]),
    ("a != b", [("IDENTIFIER", "a"), ("NOT_EQUAL", "!="), ("IDENTIFIER", "b"), ("EOF", None)]),
])
def test_two_character_operators(source, expected):
    assert lex(source) == expected

def test_other_single_character_tokens():
    assert [t for t, _ in lex("- * / [ ] , ;")] == [
        "MINUS", "STAR", "SLASH", "LBRACKET", "RBRACKET", "COMMA", "SEMICOLON", "EOF"
    ]

def test_comment_is_skipped():
    assert lex("x = 1 // this is ignored\ny = 2") == [
        ("IDENTIFIER", "x"), ("ASSIGN", "="), ("NUMBER", "1"),
        ("IDENTIFIER", "y"), ("ASSIGN", "="), ("NUMBER", "2"), ("EOF", None),
    ]

def test_second_dot_message():
    assert "second decimal point" in str(lex_error("1.2.3"))

def test_decimal_number():
    assert lex("3.14") == [("NUMBER", "3.14"), ("EOF", None)]


def parse_expr(source):
    return Parser(Lexer(source).tokenize()).parse_expression()

def test_precedence():
    assert parse_expr("1 + 2 * 3") == BinaryOp(
        Number(1), "+", BinaryOp(Number(2), "*", Number(3)))

def test_left_associative():
    assert parse_expr("1 - 2 - 3") == BinaryOp(
        BinaryOp(Number(1), "-", Number(2)), "-", Number(3))

def test_parentheses():
    assert parse_expr("(1 + 2) * 3") == BinaryOp(
        BinaryOp(Number(1), "+", Number(2)), "*", Number(3))

def test_unary_minus():
    assert parse_expr("3 - -x") == BinaryOp(
        Number(3), "-", UnaryOp("-", Variable("x")))

def test_match_consumes_token():
    parser = Parser(Lexer("3 + 2").tokenize())
    parser.match("NUMBER")
    assert parser.current().type == "PLUS"

def parse_program(source):
    return Parser(Lexer(source).tokenize()).parse_program()

def test_assignment():
    assert parse_program("x = 1 + 2;") == Block([
        Assign("x", BinaryOp(Number(1), "+", Number(2)))
    ])

def test_two_statements():
    assert parse_program("x = 1; y = x;") == Block([
        Assign("x", Number(1)), Assign("y", Variable("x"))
    ])

def test_missing_semicolon():
    with pytest.raises(SSIError):
        parse_program("x = 1")

def test_leftover_tokens():
    with pytest.raises(SSIError):
        parse_program("1 + 2 3;")