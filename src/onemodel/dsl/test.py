import json

import tatsu
from tatsu.ast import AST

from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter
from onemodel.variable import Variable
from onemodel.equation import Equation, EquationType
from onemodel.export.matlab.matlab import Matlab

class OnemodelSemantics(object):
    def __init__(self):
        self.onemodel = OneModel('test')
        self.equation_num = 0

    def number(self, ast):
        return float(ast)

    def string(self, ast):
        return str(ast)

    def operator(self, ast):
        return str(ast)
    
    def identifier(self, ast):
        return str(ast)

    def math_expr(self, ast):
        expr = ''
        for item in ast:
            expr += str(item)

        return expr

    def parameter(self, ast):
        p = Parameter(ast.name)
        p.value = str(ast.value)
        p.units = ast.units
        p.comment = ast.comment
        self.onemodel.add(p)

    def variable(self, ast):
        v = Variable(ast.name)
        v.value = str(ast.value)
        v.units = ast.units
        v.comment = ast.comment
        self.onemodel.add(v)

        return v

    def equation_ode(self, ast):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.ODE
        e.variable_name = ast.name
        e.value = ast.eqn
        e.comment = ast.comment
        self.onemodel.add(e)

    def equation_susbtitution(self, ast):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.SUBSTITUTION
        e.variable_name = ast.name
        e.value = ast.eqn
        e.comment = ast.comment
        self.onemodel.add(e)

    def equation_algebraic(self, ast):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.ALGEBRAIC
        e.variable_name = ast.name
        e.value = ast.eqn
        e.comment = ast.comment
        self.onemodel.add(e)

    def statement(self, ast):
        return ast

def main(data):
    grammar = open('/home/nobel/Sync/python/workspace/onemodel/src/onemodel/dsl/grammars/onemodel.ebnf').read()

    # data = '(a+b)*10'

    semantics = OnemodelSemantics()
    parser = tatsu.compile(grammar)

    try:
        result = parser.parse(data, semantics=semantics)
    except Exception as e:
        print(str(e))

    print(result)

    onemodel = semantics.onemodel

    matlab = Matlab(onemodel)
    matlab.generate_param()
    matlab.generate_ode()
    matlab.generate_driver()
    matlab.generate_states()

if __name__ == '__main__':
    from sys import argv

    if len(argv) > 1:
        filename = str(argv[1])
        data = open(filename).read()

        main(data)
    else:
        print('Error: no filename passed')


