from __future__ import annotations
from dataclasses import dataclass
from typing import Union


# expressions

@dataclass
class Number:
    value: float

@dataclass
class String:
    value: str

@dataclass
class Boolean:
    value: bool

@dataclass
class Variable:
    name: str

@dataclass
class ListLiteral:
    elements: list

@dataclass
class UnaryOp:
    operator: str
    operand: Expr

@dataclass
class BinaryOp:
    left: Expr
    operator: str
    right: Expr

@dataclass
class Call:
    callee: Expr
    arguments: list


# statements

@dataclass
class Assign:
    name: str
    value: Expr

@dataclass
class Block:
    statements: list

@dataclass
class If:
    condition: Expr
    then_block: Block
    else_block: Block | None = None

@dataclass
class While:
    condition: Expr
    body: Block

@dataclass
class For:
    variable: str
    iterable: Expr
    body: Block

@dataclass
class FunctionDef:
    name: str
    parameters: list
    body: Block

@dataclass
class Return:
    value: Expr | None = None


Expr = Union[Number, String, Boolean, Variable, ListLiteral, UnaryOp, BinaryOp, Call]
Stmt = Union[Assign, Block, If, While, For, FunctionDef, Return, Expr]