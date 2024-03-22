import re
from config import *

def is_variable(s:str) -> bool:
    m = re.match('[p-z]_*\d*', s)
    return m != None

def is_constant(s:str) -> bool:
    return s in CONSTANT_LIST

def is_unary(s:str) -> bool:
    return s in UNARY_LIST

def is_binary(s:str) -> bool:
    return s in BINARY_LIST

def is_operator(s:str) -> bool:
    return is_unary(s) or is_binary(s)

def get_reverse_constant(s:str) -> str:
    if s == 'T':
        return 'F'
    elif s == 'F':
        return 'T'
    elif s == '0':
        return '1'
    elif s == '1':
        return '0'

def split_str(s):
    # if s[0] == '-':
    #     prefix, rest = s[:2], s[2:]
    # elif s[0] == '<':
    #      prefix, rest = s[:3], s[3:]
    # else:
    #     prefix, rest = s[:1], s[1:]
    prefix, rest = s[:1], s[1:]
    m = re.match('(->)|(<->)', s)
    if m:
        end = m.end()
        prefix, rest = s[0:end], s[end:]
        return prefix, rest
    m = re.match('[p-z]_*\d*', s)
    if m:
        end = m.end()
        prefix, rest = s[0:end], s[end:]
        return prefix, rest
    return prefix, rest

prior_map = {}
for o in UNARY_LIST:
    prior_map[o] = 2
for o in (AND_LIST + OR_LIST):
    prior_map[o] = 1
for o in (IMPL_LIST + DB_IMPL_LIST):
    prior_map[o] = 1      

# prior_map = {
#     '&': 1,
#     '|': 1,
#     '∧': 1,
#     '∨': 1,
#     '->': 0,
#     '<->': 0,
#     '⟶': 0,
#     '⟷': 0,
#     '~': 2,
#     '¬': 2
# }
comb_order_map = {}
for o in UNARY_LIST:
    comb_order_map[o] = 'r'
for o in BINARY_LIST:
    comb_order_map[o] = 'l'


# comb_order_map = {
#     '&': 'l',
#     '|': 'l',
#     '∧': 'l',
#     '∨': 'l',
#     '->': 'l',
#     '⟶': 'l',
#     '⟷': 'l',
#     '~': 'r',
#     '¬': 'r'
# }
def str_to_operator(s:str) -> OperatorType:
    if s in NEG_LIST:
        return OperatorType.NEG
    elif s in AND_LIST:
        return OperatorType.AND
    elif s in OR_LIST:
        return OperatorType.OR
    elif s in IMPL_LIST:
        return OperatorType.IMPL
    elif s in DB_IMPL_LIST:
        return OperatorType.DB_IMPL

def str_to_constant(s:str) -> ConstantType:
    if s in FALSE_LIST:
        return ConstantType.FALSE
    elif s in TRUE_LIST:
        return ConstantType.TRUE   

if __name__ == '__main__':
    print(split_str('x_123&'))
    print(split_str('->x_123&'))
    print(split_str('<->x_123&'))
    print(split_str('⟶x_123&'))