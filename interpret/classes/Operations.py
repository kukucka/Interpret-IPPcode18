from enum import Enum

class ArithmeticOperations(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    IDIV = 4

class CompareOperations(Enum):
    LT = 1
    GT = 2
    EQ = 3

class LogicOperations(Enum):
    AND = 1
    OR = 2
    NOT = 3
