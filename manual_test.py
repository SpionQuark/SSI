from modules.evaluator import Evaluator
from modules.helpers import SSIError

codes = [
    "-(2+3)",
    "3*-2",
    "3--2",
    "x==-1",
    "(1+2)*(3+4)"
]

for code in codes:
    print(Evaluator().run(code + ";"))