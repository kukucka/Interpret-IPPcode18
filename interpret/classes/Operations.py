from enum import Enum
"""
enumerator pro aritmicke operace
"""
class ArithmeticOperations(Enum):
    ADD = 1
    SUB = 2
    MUL = 3
    IDIV = 4
"""
enumerator pro operace porovnavani
"""
class CompareOperations(Enum):
    LT = 1
    GT = 2
    EQ = 3
"""
enumerator pro logicke operace
"""
class LogicOperations(Enum):
    AND = 1
    OR = 2
    NOT = 3
