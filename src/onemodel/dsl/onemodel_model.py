import tatsu
from tatsu.walkers import NodeWalker

from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter
from onemodel.variable import Variable
from onemodel.equation import Equation, EquationType
from onemodel.export.matlab.matlab import Matlab

class OneModelWalker(NodeWalker):
    def __init__(self, basename, export_path):
        self.onemodel = OneModel(basename, export_path)
        self.equation_num = 0

    def walk_object(self, node):
        return node

    def walk_closure(self, nodes):
        results = []

        for node in nodes:
            result = self.walk(node)

            if result == '\n' or result == ';':
                continue

            results.append(result)

        if len(results) == 1:
            results = results[0]

        return results

    def walk_DefineParameter(self, node):
        p = Parameter(self.walk(node.name))
        p.value = str(self.walk(node.value))
        p.units = self.walk(node.units)
        p.comment = self.walk(node.comment)
        self.onemodel.add(p)
        return p

    def walk_DefineVariable(self, node):
        v = Variable(self.walk(node.name))
        v.value = str(self.walk(node.value))
        v.units = self.walk(node.units)
        v.comment = self.walk(node.comment)
        self.onemodel.add(v)
        return v

    def walk_DefineEquationOde(self, node):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.ODE
        e.variable_name = self.walk(node.name)
        e.value = self.walk(node.eqn)
        e.comment = self.walk(node.comment)
        self.onemodel.add(e)
        return e

    def walk_DefineEquationSubstitution(self, node):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.SUBSTITUTION
        e.variable_name = self.walk(node.name)
        e.value = self.walk(node.eqn)
        e.comment = self.walk(node.comment)
        self.onemodel.add(e)
        return e

    def walk_DefineEquationAlgebraic(self, node):
        e = Equation(f'eq_{self.equation_num}')
        self.equation_num += 1
        e.equation_type = EquationType.ALGEBRAIC
        e.variable_name = self.walk(node.name)
        e.value = self.walk(node.eqn)
        e.comment = self.walk(node.comment)
        self.onemodel.add(e)
        return e

    def walk_MathExpression(self, node):
        result = ''

        for item in node.ast:
            result += str(self.walk(item))

        return result

def main(data):
    grammar = open('/home/nobel/Sync/python/workspace/onemodel/src/data/grammar/onemodel_model.ebnf').read()

    # data = '(a+b)*10'

    parser = tatsu.compile(grammar, asmodel=True)
    walker = OneModelWalker()

    model = parser.parse(data)
    result = walker.walk(model)
    
    # print(data)

    print(type(model))
    print(model)

    print('# WALKER RESULT IS:')
    print(result)
    print()

    matlab = Matlab(walker.onemodel)
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
        print('Error: no filename passed.')
