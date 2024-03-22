from PL import Expr, CNF
import config

config.set_print_style('latex')

e = Expr.build_from_infix('((x_1⟶x_2)∨¬((¬x_1⟷x_3)∨x_4))∧¬x_2)')
print(e)
print('----------------------------------------------')
e = e.tseitin()
print(e)
print('----------------------------------------------')
print(CNF(str(e)))
print('==============================================')
e = Expr.build_from_infix('(x_1∨x_2∨x_3∨x_4∨x_5)∧(x_2∨x_3∨x_4∨x_5∨x_6)∧(x_3∨x_4∨x_5∨x_6∨x_7)')
print(e)
print('----------------------------------------------')
e = e.tseitin()
print(e)
print('----------------------------------------------')
print(CNF(str(e)))
print('==============================================')
e = Expr.build_from_infix('((x_1⟷x_2)⟷(x_3⟷x_4))⟷((x_1⟷x_3)⟷(x_2⟷x_4))')
print(e)
print('----------------------------------------------')
e = e.tseitin()
print(e)
print('----------------------------------------------')
print(CNF(str(e)))


