from modules.evaluator import Evaluator
from modules.helpers import SSIError
from modules.lexer import Lexer
from modules.parser import Parser

codes = [
    "-(2+3)",
    "3*-2",
    "3--2",
    "x==-1",
    "(1+2)*(3+4)"
]

for code in codes:
    print(Evaluator().run(code + ";"))

# tokens = Lexer("3*-2;").tokenize()
# tree = Parser(tokens).parse_program()
# print(tree)
# print(Evaluator().run(tree=tree))