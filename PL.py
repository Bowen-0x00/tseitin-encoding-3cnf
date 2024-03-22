from typing import Optional, TypeVar, Set, Tuple, Union, List
import config
from utils import *
import math


class Operator:
    value: OperatorType
    nary: int
    def __init__(self, value) -> None:
        if isinstance(value, OperatorType):
            self.value = value
        elif isinstance(value, str):
            self.value = str_to_operator(value)
        self.nary = Operator.value_to_nary(self.value)

    def value_to_nary(value: OperatorType) -> int:
        if value == OperatorType.NEG:
            return 1
        elif value == OperatorType.NONE:
            return 0
        else:
            return 2
    def __repr__(self) -> str:
        return config.OPERATOR_PRINT_MAP[self.value]

    def demorgan(self):
        if self.value == OperatorType.AND:
            return Operator(OperatorType.OR)
        elif self.value == OperatorType.OR:
            return Operator(OperatorType.AND)





class Constant:
    value: ConstantType

    def __init__(self, value) -> None:
        if isinstance(value, ConstantType):
            self.value = value
        elif isinstance(value, str):
            self.value = str_to_constant(value)

    def __repr__(self) -> str:
        return config.CONSTANT_PRINT_MAP[self.value]

    def _get_reverse(value: ConstantType) -> ConstantType:
        if value == ConstantType.TRUE:
            return ConstantType.FALSE
        else:
            return ConstantType.TRUE

    def get_reverse(self):
        return Constant(Constant._get_reverse(self.value))



class Element:
    type: ElementType
    value: Union[Operator, str, Constant]

    def __init__(self, value:Union[Operator, str, Constant], type: ElementType=None) -> None:
        if type != None:
            self.type = type
            self.value = value
        elif isinstance(value, str):
            if is_constant(value):
                self.type = ElementType.CONSTANT
                self.value = Constant(value)
            elif is_variable(value):
                self.type = ElementType.VARIABLE
                self.value = value
            elif is_operator(value):
                self.type = ElementType.OPERATOR
                self.value = Operator(value)
        
    def __repr__(self) -> str:
        return str(self.value)

    def demorgan(self):
        assert self.type == ElementType.OPERATOR and self.value.nary == 2
        return Element(self.value.demorgan(), ElementType.OPERATOR)

Expr = TypeVar('Expr')
class Expr:
    root: Element
    first: Optional[Expr]
    second: Optional[Expr]

    is_constant: bool = False
    is_variable: bool = False
    is_unary: bool = False
    is_binary: bool = False

    parent_op_type: OperatorType

    def __init__(self, root: Union[str, Element], first: Optional[Expr] = None, second: Optional[Expr] = None, parent_op_type=None):
        if isinstance(root, str):
            if is_constant(root):
                assert first is None and second is None
                self.root = Element(Constant(root), ElementType.CONSTANT)
                self.is_constant = True
            elif is_variable(root):
                assert first is None and second is None
                self.root = Element(root, ElementType.VARIABLE)
                self.is_variable = True
            elif is_unary(root):
                assert first is not None and second is None
                self.root = Element(Operator(root), ElementType.OPERATOR)
                self.first = first
                self.is_unary = True
                self.first.parent_op_type = OperatorType.NEG
            elif is_binary(root):
                assert first is not None and second is not None
                self.root = Element(Operator(root), ElementType.OPERATOR)
                self.first = first
                self.second = second
                self.is_binary = True
                self.first.parent_op_type = self.root.value.value
                self.second.parent_op_type = self.root.value.value
        elif isinstance(root, Element):
            self.root = root
            if self.root.type == ElementType.CONSTANT:
                assert first is None and second is None
                self.is_constant = True
            elif self.root.type == ElementType.VARIABLE:
                assert first is None and second is None
                self.is_variable = True
            elif self.root.type == ElementType.OPERATOR and self.root.value.nary == 1:
                assert first is not None and second is None
                self.first = first
                self.is_unary = True
                self.first.parent_op_type = OperatorType.NEG
            elif self.root.type == ElementType.OPERATOR and self.root.value.nary == 2:
                assert first is not None and second is not None
                self.first = first
                self.second = second
                self.is_binary = True
                self.first.parent_op_type = self.root.value.value
                self.second.parent_op_type = self.root.value.value
        self.parent_op_type = parent_op_type
    def __repr__(self) -> str:
        if self.is_constant or self.is_variable:
            return str(self.root)
        elif self.is_unary:
            return str(self.root) + str(self.first)
        elif self.is_binary:
            if self.root.value.value == self.parent_op_type:
                return f'{str(self.first)}{str(self.root)}{str(self.second)}'
            return f'({str(self.first)}{str(self.root)}{str(self.second)})'

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Expr) and str(self) == str(__o)

    def __ne__(self, __o: object) -> bool:
        return not self == __o

    def __hash__(self) -> int:
        return hash(str(self))

    def variables(self) -> Set[str]:
        variables = set()
        def get_variables(expr: Expr, variables: Set[str]):
            if expr.is_constant:
                return variables
            elif expr.is_variable:
                variables.add(expr.root)
                return variables 
            elif expr.is_unary:
                return get_variables(expr.first, variables)
            elif expr.is_binary:
                variables = get_variables(expr.first, variables)
                return get_variables(expr.second, variables)
        return get_variables(self, variables)

    def operators(self) -> Set[str]:
        operators = set()
        def get_operators(expr, operators: Set[str]):
            if self.is_constant:
                operators.add(expr.root)
                return operators
            elif self.is_variable:
                return operators 
            elif expr.is_unary:
                operators.add(expr.root)
                return get_operators(expr.first, operators)
            elif expr.is_binary:
                operators.add(expr.root)
                operators = get_operators(expr.first, operators)
                return get_operators(expr.second, operators)
        return get_operators(self, operators)

    def infix_to_suffix(s: str) -> list:
        op_stack = []
        result = []
        res = s
        while res != '':
            e, res = split_str(res)
            if is_constant(e) or is_variable(e):
                result.append(e)
            elif e == '(':
                op_stack.append(e)
            elif e == ')':
                while op_stack:
                    op = op_stack[-1]
                    op_stack.pop()
                    if op == '(':
                        break
                    result.append(op)
            elif is_operator(e):
                # if op_stack == []:
                #     op_stack.append(temp)
                #     continue
                while op_stack:
                    op = op_stack[-1]
                    if op != '(' and prior_map[e] < prior_map[op]:
                        result.append(op)
                        op_stack.pop()
                    elif op != '(' and prior_map[e] == prior_map[op]:
                        if comb_order_map[e] == 'l':
                            result.append(op)
                            op_stack.pop()
                        else:
                            break
                    else:
                        break
                op_stack.append(e)
        while op_stack:
            op = op_stack.pop()
            result.append(op)
        return result
    def build_from_suffix(suffix:str) -> Expr:
        variables = []
        while suffix:
            e = suffix.pop(0)
            if is_constant(e) or is_variable(e):
                v = Expr(e)
                variables.append(v)
            elif is_unary(e):
                v = variables.pop()
                variables.append(Expr(e, v))
            elif is_binary(e):
                v1 = variables.pop()
                v2 = variables.pop()
                variables.append(Expr(e, v2, v1))
        return variables[-1]
    def build_from_infix(s:str) -> Expr:
        suffix = Expr.infix_to_suffix(s)
        return Expr.build_from_suffix(suffix)

    def neg(self) -> Expr:
        # return Expr('~', self)
        if self.is_constant:
            return Expr(self.root.value.get_reverse(), parent_op_type=self.parent_op_type)
        elif self.is_variable:
            return Expr('~', self, parent_op_type=self.parent_op_type)
        elif self.is_unary:
            return self.first
        elif self.is_binary:
            if self.root.value.value == OperatorType.AND:
                return Expr('|', self.first.neg(), self.second.neg(), parent_op_type=self.parent_op_type)
            elif self.root.value.value == OperatorType.OR:
                return Expr('&', self.first.neg(), self.second.neg(), parent_op_type=self.parent_op_type)
            elif self.root.value.value == OperatorType.IMPL:#~(x->y) = ~(~x|y)=x&~y
                return Expr('&', self.first, self.second.neg(), parent_op_type=self.parent_op_type)
            elif self.root.value.value == OperatorType.DB_IMPL:#~(x<->y) = ~((~x|y)&(x|~y))=(x&~y)|(~x&y)
                return Expr('|', Expr('&', self.first, self.second.neg(), parent_op_type=OperatorType.OR),Expr('&', self.first, self.second.neg(), parent_op_type=OperatorType.OR), parent_op_type=self.parent_op_type)
    def imp_free(self) -> Expr:
        if self.is_constant or self.is_variable:
            return self
        if self.is_unary:
            self.first = self.first.imp_free()
            return self
        elif self.is_binary:
            if self.root.value.value == OperatorType.AND or self.root.value.value == OperatorType.OR:
                self.first =  self.first.imp_free()
                self.second =  self.second.imp_free()
                return self
            if self.root.value.value == OperatorType.IMPL:
                return Expr('|', self.first.neg(), self.second, parent_op_type=self.parent_op_type).imp_free()
            if self.root.value.value == OperatorType.DB_IMPL:
                return Expr('&', Expr('|', self.first.neg(), self.second, parent_op_type=OperatorType.AND).imp_free(),Expr('|', self.first, self.second.neg(), parent_op_type=OperatorType.AND).imp_free(), parent_op_type=self.parent_op_type)
    def nnft(self) -> Expr:
        if self.is_constant or self.is_variable:
            return self
        if self.is_unary:
            if self.first.is_binary:
                return Expr(self.first.root.demorgan(), Expr('~', self.first.first).nnft(), Expr('~', self.first.second).nnft(), parent_op_type=self.parent_op_type)
            elif self.first.is_unary:
                return self.first.first.nnft()
            elif self.first.is_constant or self.first.is_variable:
                return self
        elif self.is_binary:
            if self.root.value.value == OperatorType.AND or self.root.value.value == OperatorType.OR:
                self.first =  self.first.nnft()
                self.second =  self.second.nnft()
                return self
    def distr(f:Expr, g:Expr) -> Expr:
        if f.is_binary and f.root.value.value == OperatorType.AND:
            f.first.parent_op_type = OperatorType.AND
            f.second.parent_op_type = OperatorType.AND
            g.parent_op_type = OperatorType.AND
            return Expr('&', Expr.distr(f.first, g), Expr.distr(f.second, g))
        elif g.is_binary and g.root.value.value == OperatorType.AND:
            g.first.parent_op_type = OperatorType.AND
            g.second.parent_op_type = OperatorType.AND
            f.parent_op_type = OperatorType.AND
            return Expr('&', Expr.distr(f, g.first), Expr.distr(f, g.second))
        else:
            f.parent_op_type = OperatorType.OR
            g.parent_op_type = OperatorType.OR
            return Expr('|', f, g)

    def cnf(self) -> Expr:
        if self.is_constant or self.is_variable or self.is_unary:
            return self
        elif self.is_binary:
            if self.root.value.value == OperatorType.AND:
                self.first =  self.first.cnf()
                self.second =  self.second.cnf()
                return self
            elif self.root.value.value == OperatorType.OR:
                e = Expr.distr(self.first.cnf(), self.second.cnf())
                e.parent_op_type = self.parent_op_type
                return e
    def set_variable(self, s:str) -> None:
        self.is_constant = False
        self.is_unary = False
        self.is_binary = False
        self.is_variable = True
        self.first = None
        self.second = None
        self.root = Element(s)

    def tseitin(self) -> Expr:
        expr_list = []
        i = 1
        def get_expr(e:Expr,expr_list:list) -> Expr:
            nonlocal i
            if e.is_constant or e.is_variable:
                return e
            elif e.is_unary:
                e.first = get_expr(e.first, expr_list)
                return e
            elif e.is_binary:
                e.first = get_expr(e.first, expr_list)
                e.second = get_expr(e.second, expr_list)
                e_new = Expr(Element(config.NEW_VARIABLE_PRINT.format(i)))
                i+=1
                expr_list.append(Expr('<->', e_new, e, parent_op_type=e.parent_op_type))
                return e_new
            else:
                return e
        e_new = get_expr(self, expr_list)
        E = e_new
        for e in reversed(expr_list):
            E = Expr('&', E, e.imp_free().nnft().cnf(), parent_op_type=OperatorType.AND)
        return E

class Clause:
    literals = None

    def __init__(self, literals) -> None:
        self.literals = {}.fromkeys(literals).keys()

    def __eq__(self, __o: object) -> bool:
        return set(__o.literals) == set(self.literals) 

    def __repr__(self) -> str:
        result = ''
        
        if len(self.literals) > 1:
            result += '('    
        for j, literal in enumerate (self.literals):
            if j > 0:
                result += config.OPERATOR_PRINT_MAP[OperatorType.OR]
            result += literal
        if len(self.literals) > 1:
            result += ')' 
        return result
    def __hash__(self) -> int:
        total = 0
        for s in str(list(self.literals)):
            total += ord(s)
        return total

    def __len__(self) -> int:
        return len(self.literals)

class CNF:
    clauses: list
    def __init__(self, s:str) -> None:
        s = s.replace('(', '')
        s = s.replace(')', '')
        and_str = config.OPERATOR_PRINT_MAP[OperatorType.AND]
        or_str = config.OPERATOR_PRINT_MAP[OperatorType.OR]
        clauses = []
        clause_str_list = s.split(and_str)
        for clause_str in clause_str_list:
            clauses.append(Clause(clause_str.split(or_str)))
        self.clauses = {}.fromkeys(clauses).keys()

    def __repr__(self) -> str:
        result = ''
        for i, clause in enumerate(self.clauses):
            if i > 0:
                result += config.OPERATOR_PRINT_MAP[OperatorType.AND]
            result += str(clause)
        return result

if __name__ == '__main__':
    # print(type(ElementType.CONSTANT))
    # e1 = Expr('x1')
    # e2 = Expr('x2')
    # expr = Expr('->', e1, e2)
    # print(Expr('T'))
    # print(Expr("->", Expr("->", Expr("p"), Expr("q")), \
    #                          Expr("->", Expr("~", Expr("q")), Expr("~", Expr("p")))))
    # print(expr.variables())
    # print(split_str('&y'))
    print(Expr.build_from_infix('(x123&x4)').neg())
    print(Expr.build_from_infix('~(x123&x4)').neg())
    print(Expr.build_from_infix('(x123->x4)').neg())
    print(Expr.build_from_infix('(x123->x4)').imp_free())
    print(Expr.build_from_infix('(x1|x2|x3)'))
    print(Expr.build_from_infix('((x1⟶x2)∨¬((¬x1⟷x3)∨x4))∧¬x2)').imp_free())
    print(Expr.build_from_infix('((x1⟶x2)∨¬((¬x1⟷x3)∨x4))∧¬x2)'))
    print(Expr.build_from_infix('x1<->x2|x3'))
    print(Expr.build_from_infix('x1<->x2|x3').imp_free())
    print(Expr.build_from_infix('~~x1').imp_free().nnft())
    print(Expr.build_from_infix('~(x1&x2)&~(x3|x4)').imp_free().nnft())
    print(Expr.distr(Expr.build_from_infix('x'), Expr.build_from_infix('(y1&y2)')))
    print(Expr.distr(Expr.build_from_infix('(x1&x2)'), Expr.build_from_infix('y')))
    print(Expr.build_from_infix('~(x1&x2)&~(x3|x4)').imp_free().nnft().cnf())
    print(Expr.build_from_infix('x1<->x2|x3').imp_free().nnft().cnf())
    # print(Expr_seq())
    print(Expr.build_from_infix('(~(~x1&~x2)&~(x1&x2))&x3').tseitin())
    print(CNF(str(Expr.build_from_infix('(~(~x1&~x2)&~(x1&x2))&x3').tseitin())))
    # print(Expr.build_from_infix('((x1⟶x2)∨¬((¬x1⟷x3)∨x4))∧¬x2)').tseitin())
    # print(Expr.build_from_infix('(x_1∨x_2∨x_3∨x_4∨x_5)∧(x_2∨x_3∨x_4∨x_5∨x_6)∧(x_3∨x_4∨x_5∨x_6∨x_7)').tseitin())
    # print(CNF(str(Expr.build_from_infix('((x_1⟷x_2)⟷(x_3⟷x_4))⟷((x_1⟷x_3)⟷(x_2⟷x_4))').tseitin())))