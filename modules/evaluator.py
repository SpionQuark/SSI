from modules.lexer import Lexer
from modules.parser import Parser
from modules.nodes import *
from modules.helpers import SSIError, Scope, parse_output, p_o

class Evaluator:

    def __init__(self):
        pass

    def run(self, code = None, tree = None):
        self.scope = Scope()
        if tree is None and code is None:
            raise SSIError("No code given", -1)
        if tree is None: 
            tokens = Lexer(code).tokenize()
            tree = Parser(tokens).parse_program()
        res = self.evaluate(tree)
        return parse_output(res)

    def evaluate(self, node):
        if isinstance(node, Block):
            _last = None
            for n in node.statements:
                _last = self.evaluate(n)
            return _last
        if isinstance(node, Variable):
            return self.scope.get(node.name, node.line)
        if isinstance(node, Assign):
            value = self.evaluate(node.value)
            self.scope.set(node.name, value, node.line)
            return value
        if isinstance(node, BinaryOp):
            return self.e_binary_op(node)
        if isinstance(node, UnaryOp):
            return self.e_unary_op(node)
        if isinstance(node, Number):
            return self.e_number(node)
        if isinstance(node, String):
            return self.e_string(node)
        if isinstance(node, Boolean):
            return self.e_boolean(node)
        raise SSIError(f"Unknown Node given: {node}", node.line)

    def integer_conversion(self, n:float):
        return round(n)
    
    # BinaryOp(left=Number(value=3.0), operator='+', right=Number(value=2.0))
    def e_number(self, n: Number):
        return n.value
    def e_string(self, s: String):
        return s.value
    def e_boolean(self, b: Boolean):
        return b.value

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
            raise SSIError(f"Division by zero not possible: {p_o(left, str) + '/' + p_o(right, str)}", node.line)
        if node.operator == "*":
            return left * right
        raise SSIError(f"Unknown operator {node.operator}", node.line)

    # UnaryOp(operator='-', operand=Number(value=3.0))
    def e_unary_op(self, node):
        operand = self.evaluate(node.operand)
        if node.operator == "-":
            return - operand
        raise SSIError(f"Unknown operator {node.operator}", node.line)
