import json

import tatsu
from tatsu.ast import AST

class OnemodelSemantics(object):
    def number(self, ast):
        return float(ast)

    def string(self, ast):
        return str(ast)

def main():
    line = 'd1 = {1 , "1/t"} "Degradation time"'
    line = '0.0'

    grammar = open('grammars/onemodel.ebnf').read()

    semantics = OnemodelSemantics()

    parser = tatsu.compile(grammar)
    result = parser.parse(line, semantics=semantics)

    print('# Result')
    print(result)

if __name__ == '__main__':
    main()
