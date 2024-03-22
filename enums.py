from enum import Enum

class OperatorType(Enum):
    NEG = 0
    AND = 1
    OR = 2
    IMPL = 3
    DB_IMPL = 4
    NONE = -1

class ConstantType(Enum):
    FALSE = 0
    TRUE = 1

class ElementType(Enum):
    CONSTANT = 0
    VARIABLE = 1
    OPERATOR = 2