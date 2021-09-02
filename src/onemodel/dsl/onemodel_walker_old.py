import tatsu
from tatsu.walkers import NodeWalker
 
from onemodel.onemodel import OneModel
from onemodel.symbol import Symbol
from onemodel.parameter import Parameter
from onemodel.variable import Variable
from onemodel.equation import Equation, EquationType

class SymbolTable:
  def __init__(self, parent=None):
    self.symbols = {}
    self.parent = parent

  def get(self, name):
    value = self.symbols.get(name, None)

    if value == None and self.parent:
        return self.parent.get(name)
    
    if value == None:
        raise NameError(f"NameError: name '{name}' is not defined")
    
    return value

  def set(self, name, value):
    self.symbols[name] = value

  def remove(self, name):
    del self.symbols[name]

class OneModelWalker(NodeWalker):
    def __init__(self, basename, export_path):
        self.onemodel = OneModel(basename, export_path)
        self.equation_num = 0

        self.symbol_table = SymbolTable()

    def populate_model(self):
        for name, symbol in self.symbol_table.symbols.items():
            if isinstance(symbol, Symbol):
                self.onemodel.add(symbol)

    def walk_object(self, node):
        return node

    def walk_BinaryOperation(self, node):
        left = self.walk(node.left)
        right = self.walk(node.right)
        op = node.op

        if op == '+':
            return left + right

        if op == '-':
            return left - right

        if op == '*':
            return left * right

        if op == '/':
            return left / right

        if op == '^':
            return left ** right
        
    def walk_UnaryOperation(self, node):
        right = self.walk(node.right)
        op = node.op
        
        if op == '+':
            return right

        if op == '-':
            return -right

    def walk_Parameter(self, node):
        p = Parameter(node.name)
        p.value = str(self.walk(node.value))
        p.units = node.units
        if node.comment != None:
            p.comment = node.comment

        self.symbol_table.set(node.name, p)

        return 

    def walk_Variable(self, node):
        v = Variable(node.name)
        v.value = str(self.walk(node.value))
        v.units = node.units
        if node.comment != None:
            v.comment = node.comment

        self.symbol_table.set(node.name, v)

        return 

    def walk_EquationOde(self, node):
        e = Equation(f'eq_{self.equation_num}')
        e.equation_type = EquationType.ODE
        e.variable_name = node.name

        # '0+value' makes the value into a math_expr in case just a Symbol is
        # passed.
        e.value = 0+self.walk(node.value)
        if node.comment != None:
            e.comment = node.comment

        self.symbol_table.set(f'eq_{self.equation_num}', e)
        self.equation_num += 1

    def walk_EquationSubstitution(self, node):
        e = Equation(f'eq_{self.equation_num}')
        e.equation_type = EquationType.SUBSTITUTION
        e.variable_name = node.name

        # '0+value' makes the value into a math_expr in case just a Symbol is
        # passed.
        e.value = 0+self.walk(node.value)
        if node.comment != None:
            e.comment = node.comment

        self.symbol_table.set(f'eq_{self.equation_num}', e)
        self.equation_num += 1

    def walk_EquationAlgebraic(self, node):
        e = Equation(f'eq_{self.equation_num}')
        e.equation_type = EquationType.ALGEBRAIC
        e.variable_name = node.name

        # '0+value' makes the value into a math_expr in case just a Symbol is
        # passed.
        e.value = 0+self.walk(node.value)
        if node.comment != None:
            e.comment = node.comment

        self.symbol_table.set(f'eq_{self.equation_num}', e)
        self.equation_num += 1

    def walk_AssignProperty(self, node):
        name = node.name
        property_name = node.property_name
        value = self.walk(node.value)

        symbol = self.symbol_table.get(name)

        setattr(symbol, property_name, value)

        return

    def walk_AssignIdentifier(self, node):
        name = node.name
        value = self.walk(node.value)

        self.symbol_table.set(name, value)

        return

    def walk_AccessProperty(self, node):
        name = node.name
        value = self.symbol_table.get(name)
        property_name = node.property_name

        value = getattr(value, property_name)

        return value

    def walk_AccessIdentifier(self, node):
        name = node.name
        value = self.symbol_table.get(name)

        return value

    def walk_list(self, nodes):
        results = []

        for node in nodes:
            results.append(self.walk(node))

        if len(results) == 1:
            results = results[0]

        return results

#    def walk_closure(self, nodes):
#        results = []
#
#        for node in nodes:
#            result = self.walk(node)
#
#            if result == '\n' or result == ';':
#                continue
#
#            results.append(result)
#
#        if len(results) == 1:
#            results = results[0]
#
#        return results
#
#    def walk_AccessIdentifier(self, node):
#        value = self.onemodel.get(node.name)
#        return Identifier(node.name, value)
#
#    def walk_AccessProperty(self, node):
#        symbol = self.walk(node.var)
#        property_ = self.walk(node.prop)
#
#        value = getattr(symbol.value, property_.name) 
#
#        return Identifier('ans', value)
#
#    def walk_ChangeProperty(self, node):
#        symbol = self.walk(node.var)
#        property_ = self.walk(node.prop)
#        value = str(self.walk(node.value))
#
#        setattr(symbol.value, property_.name, value) 
#
#        return Identifier(symbol.name, symbol.value)
#
#    def walk_DefineParameter(self, node):
#        p = Parameter(self.walk(node.name).name)
#        p.value = str(self.walk(node.value))
#        p.units = self.walk(node.units)
#        p.comment = self.walk(node.comment)
#        self.onemodel.add(p)
#
#        return Identifier(p.name, p)
#
#    def walk_DefineVariable(self, node):
#        v = Variable(self.walk(node.name).name)
#        v.value = str(self.walk(node.value))
#        v.units = self.walk(node.units)
#        v.comment = self.walk(node.comment)
#        self.onemodel.add(v)
#        
#        return Identifier(v.name, v)
#
#    def walk_DefineEquationOde(self, node):
#        e = Equation(f'eq_{self.equation_num}')
#        self.equation_num += 1
#        e.equation_type = EquationType.ODE
#        e.variable_name = self.walk(node.name).name
#        e.value = self.walk(node.eqn)
#        e.comment = self.walk(node.comment)
#        self.onemodel.add(e)
#
#        return Identifier(e.name, e)
#
#    def walk_DefineEquationSubstitution(self, node):
#        e = Equation(f'eq_{self.equation_num}')
#        self.equation_num += 1
#        e.equation_type = EquationType.SUBSTITUTION
#        e.variable_name = self.walk(node.name).name
#        e.value = self.walk(node.eqn)
#        e.comment = self.walk(node.comment)
#        self.onemodel.add(e)
#        return e
#
#    def walk_DefineEquationAlgebraic(self, node):
#        e = Equation(f'eq_{self.equation_num}')
#        self.equation_num += 1
#        e.equation_type = EquationType.ALGEBRAIC
#        e.variable_name = self.walk(node.name).name
#        e.value = self.walk(node.eqn)
#        e.comment = self.walk(node.comment)
#        self.onemodel.add(e)
#        return e
#
#    def walk_MathExpression(self, node):
#        result = ''
#
#        for item in node.ast:
#            item = self.walk(item)
#            if isinstance(item, float):
#                item = str(item)
#            if isinstance(item, Identifier):
#                item = item.name
#            result += item
#
#        return result