from modules.parser import Parser
from modules.lexer import Lexer

code = "3 + 2;"

tokens = Lexer(code).tokenize()
print(tokens)
parser = Parser(tokens).parse_expression()
print(parser)