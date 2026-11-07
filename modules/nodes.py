from __future__ import annotations
from dataclasses import dataclass
from typing import Union


# expressions

@dataclass
class Number:
    value: float
    line: int

@dataclass
class String:
    value: str
    line: int

@dataclass
class Boolean:
    value: bool
    line: int

@dataclass
class Variable:
    name: str
    line: int

@dataclass
class ListLiteral:
    elements: list
    line: int

@dataclass
class UnaryOp:
    operator: str
    operand: Expr
    line: int

@dataclass
class BinaryOp:
    left: Expr
    operator: str
    right: Expr
    line: int

@dataclass
class Call:
    callee: Expr
    arguments: list
    line: int


# statements

@dataclass
class Assign:
    name: str
    value: Expr
    line: int

@dataclass
class Block:
    statements: list
    line: int

@dataclass
class If:
    condition: Expr
    then_block: Block
    line: int
    else_block: Block | None = None

@dataclass
class While:
    condition: Expr
    body: Block
    line: int

@dataclass
class For:
    variable: str
    iterable: Expr
    body: Block
    line: int

@dataclass
class FunctionDef:
    name: str
    parameters: list
    body: Block
    line: int

@dataclass
class Return:
    line: int
    value: Expr | None = None;


Expr = Union[Number, String, Boolean, Variable, ListLiteral, UnaryOp, BinaryOp, Call]
Stmt = Union[Assign, Block, If, While, For, FunctionDef, Return, Expr]