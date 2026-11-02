from modules.lexer import Lexer
from modules.parser import Parser
from modules.nodes import *
from modules.helpers import SSIError

class Evaluator:

    def __init__(self):
        pass

    def run(self, code = None, tree = None):
        if tree is None and code is None:
            raise SSIError("No code given", -1)
        if tree is None: 
            tokens = Lexer(code).tokenize()
            tree = Parser(tokens).parse_program()
        return self.evaluate(tree)

    def evaluate(self, node):
        if isinstance(node, Block):
            _last = None
            for n in node.statements:
                _last = self.evaluate(n)
            return _last
        if isinstance(node, BinaryOp):
            return self.e_binary_op(node)
        if isinstance(node, UnaryOp):
            return self.e_unary_op(node)
        if isinstance(node, Number):
            return self.e_number(node)
        raise SSIError(f"Unknown Node given: {node}", -1)

    # BinaryOp(left=Number(value=3.0), operator='+', right=Number(value=2.0))
    def e_number(self, n: Number):
        return n.value

    def e_binary_op(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        if node.operator == '+':
            return left + right
        if node.operator == '-':
            return left - right
        if node.operator == "/":
            if right != 0:
                return left / right
            raise SSIError(f"Division by zero not possible: {left, '/', right}", -1)
        if node.operator == "*":
            return left * right
        raise SSIError(f"Unknown operator {node.operator}", -1)

    # UnaryOp(operator='-', operand=Number(value=3.0))
    def e_unary_op(self, node):
        operand = self.evaluate(node.operand)
        if node.operator == "-":
            return - operand
        raise SSIError(f"Unknown operator {node.operator}", -1)
