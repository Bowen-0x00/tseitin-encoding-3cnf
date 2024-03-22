NEG_LIST = ['~', '¬']
AND_LIST = ['&', '∧']
OR_LIST =  ['|', '∨']
IMPL_LIST = ['->', '⟶']
DB_IMPL_LIST = ['<->', '⟷']
FALSE_LIST = ['0', 'F']
TRUE_LIST = ['0', '1']
CONSTANT_LIST =  FALSE_LIST + TRUE_LIST

UNARY_LIST = NEG_LIST
BINARY_LIST = AND_LIST + OR_LIST + IMPL_LIST + DB_IMPL_LIST

from enums import *

print_flag = 'unicode'
def set_print_style(flag: str) -> None:
    assert flag in ['latex', 'unicode', 'ascii']
    global OPERATOR_PRINT_MAP
    global NEW_VARIABLE_PRINT
    if flag == 'latex':
        OPERATOR_PRINT_MAP =  {
            OperatorType.NEG: r'\neg ',
            OperatorType.AND: r'\wedge ',
            OperatorType.OR: r'\vee ',
            OperatorType.IMPL: r'\rightarrow ',
            OperatorType.DB_IMPL: r'\leftrightarrow '#'⟷'
        }
        NEW_VARIABLE_PRINT = 'y_{{{0}}}'
    elif flag == 'ascii':
        OPERATOR_PRINT_MAP = {
            OperatorType.NEG: '~',
            OperatorType.AND: '&',
            OperatorType.OR: '|',
            OperatorType.IMPL: '->',
            OperatorType.DB_IMPL: '<->'
        }
        NEW_VARIABLE_PRINT = 'y{}'
    elif flag == 'unicode':
        OPERATOR_PRINT_MAP = {
            OperatorType.NEG: '¬',
            OperatorType.AND: '∧',
            OperatorType.OR: '∨',
            OperatorType.IMPL: '⟶ ',
            OperatorType.DB_IMPL: '⟷ '#'⟷'
        }
        NEW_VARIABLE_PRINT = 'y{}'
set_print_style(print_flag)

CONSTANT_PRINT_MAP = {
    ConstantType.FALSE: 'F',
    ConstantType.TRUE: 'T'
}