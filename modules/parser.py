from modules.nodes import *
from modules.helpers import SSIError

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    # helpers

    def current(self):
        return self.tokens[self.pos]

    def advance(self):
        token = self.tokens[self.pos]
        if token.type != "EOF":
            self.pos += 1
        return token

    def check(self, *types):
        return self.current().type in types

    def match(self, *types):
        if self.check(*types):
            return self.advance()
        return None

    def expect(self, type_, message):
        if self.check(type_):
            return self.advance()
        raise SSIError(message, self.current().line)

    # expression

    def parse_program(self):
        statements = []
        while not self.check("EOF"):
            statements.append(self.parse_statement())
        return Block(statements)

    def parse_statement(self):
        if self.check("IDENTIFIER") and self.peek_type() == "ASSIGN":
            return self.parse_assignment()
        return self.parse_expression_statement()

    def peek_type(self):
        if self.pos + 1 < len(self.tokens):
            return self.tokens[self.pos + 1].type
        return None

    def parse_assignment(self):
        name = self.advance()
        self.advance
        value = self.parse_expression()
        self.expect("SEMICOLON", "Expected ';' after assignment")
        return Assign(name.value, value)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self.expect("SEMICOLON", "Expected ';' after expression")
        return expr

    def parse_expression(self):
        return self.parse_comparison()

    def parse_comparison(self):
        left = self.parse_term()
        while self.check("GREATER_THAN", "LESS_THAN", "EQUALS",
                         "NOT_EQUAL", "GREATER_EQUAL", "LESS_EQUAL"):
            op = self.advance()
            right = self.parse_term()
            left = BinaryOp(left, op.value, right)
        return left

    def parse_term(self):
        left = self.parse_factor()
        while self.check("PLUS", "MINUS"):
            op = self.advance()
            right = self.parse_factor()
            left = BinaryOp(left, op.value, right)
        return left

    def parse_factor(self):
        left = self.parse_unary()
        while self.check("STAR", "SLASH"):
            op = self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op.value, right)
        return left

    def parse_unary(self):
        if self.check("MINUS"):
            op = self.advance()
            return UnaryOp(op.value, self.parse_unary())
        return self.parse_primary()

    def parse_primary(self):
        token = self.current()
        if self.match('NUMBER'):
            return Number(float(token.value))
        if self.match("STRING"):
            return String(token.value)
        if self.match("TRUE"):
            return Boolean(True)
        if self.match("FALSE"):
            return Boolean(False)
        if self.match("IDENTIFIER"):
            return Variable(token.value)
        if self.match("LPAREN"):
            expr = self.parse_expression()
            self.expect("RPAREN", "Expected ')' after expression")
            return expr
        raise SSIError(f"Unexpected token {token.value!r}, {token.type!r}", token.line)