from modules.evaluator import Evaluator
from modules.helpers import SSIError
from modules.lexer import Lexer
from modules.parser import Parser

codes = [
    "-(2+3)",
    "3*-2",
    "3--2",
    "(1+2)*(3+4)",
    "(1 + 2) / 3",
    "2+2/3",
    "x = 3",
    "x = 2; y = 5; x + y",
    "x = 5; y = 12; x + y",
    "x = 3;\n y = -2;\n x / (y + 3)",
    "true",
    "true == false"
]

# for code in codes:
#     print(Evaluator().run(code + ";"))

tokens = Lexer("true;").tokenize()
print(tokens)
tree = Parser(tokens).parse_program()
print(tree)
print(Evaluator().run(tree=tree))