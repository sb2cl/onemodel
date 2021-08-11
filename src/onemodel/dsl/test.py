import json

import tatsu
from tatsu.ast import AST

from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter
from onemodel.export.matlab.matlab import Matlab

class OnemodelSemantics(object):
    def __init__(self):
        self.onemodel = OneModel('test')

    def number(self, ast):
        return float(ast)

    def string(self, ast):
        return str(ast)

    def identifier(self, ast):
        name = str(ast)
        value = 'Identifier not defined'
        return name, value

    def parameter(self, ast):
        p = Parameter(ast.name[0])
        p.value = str(ast.value)
        p.units = ast.units
        p.comment = ast.comment
        self.onemodel.add(p)

        return p

def main(data):
    line = 'd1 = {1 , "1/t"} "Degradation time"'
    line = '''
    1 
    2 
    3
    '''

    grammar = open('/home/nobel/Sync/python/workspace/onemodel/src/onemodel/dsl/grammars/onemodel.ebnf').read()

    semantics = OnemodelSemantics()

    parser = tatsu.compile(grammar)
    result = parser.parse(data, semantics=semantics)

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


