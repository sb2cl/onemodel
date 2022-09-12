from importlib_resources import files
import tatsu
from tatsu.walkers import NodeWalker
from onemodel.onemodel import OneModel
from onemodel.objects.parameter import Parameter
from onemodel.objects.species import Species
from onemodel.objects.reaction import Reaction
from onemodel.objects.assignment_rule import AssignmentRule
from onemodel.objects.algebraic_rule import AlgebraicRule
from onemodel.objects.rate_rule import RateRule
from onemodel.objects.function import Function
from onemodel.builtin_functions import load_builtin_functions

def load_file(filename):
    """Load a file into OneModel. """

    file = open(filename)
    text = file.read()
    file.close()

    walker = OneModelWalker()
    result, ast = walker.run(text)
    
    onemodel = walker.onemodel

    return walker.onemodel

class OneModelWalker(NodeWalker):

    numberOfUnnamedReactions = 0
    numberOfUnnamedRules = 0
    
    def __init__(self):
        self.onemodel = OneModel()
        load_builtin_functions(self.onemodel)

        grammar = files("onemodel").joinpath("onemodel.ebnf").read_text()
        self.parser = tatsu.compile(grammar, asmodel=True)

    def run(self, onemodel_code):

        ast = self.parser.parse(onemodel_code)
        result = self.walk(ast)

        return result, ast

    def walk_Addition(self, node):
        left = self.walk(node.left)
        right = self.walk(node.right)
        return left + right

    def walk_Subtraction(self, node):
        left = self.walk(node.left)
        right = self.walk(node.right)
        return left - right

    def walk_Multiplication(self, node):
        left = self.walk(node.left)
        right = self.walk(node.right)
        return left * right

    def walk_Division(self, node):
        left = self.walk(node.left)
        right = self.walk(node.right)
        return left / right

    def walk_Parameter(self, node):
        result = self.walk(node.name)
        name = result["name"]
        namespace = result["namespace"]
        value = self.walk(node.value)
        documentation = self.walk(node.documentation)

        namespace[name] = Parameter()

        if value:
            namespace[name]["value"] = value

        if documentation:
            namespace[name]["__doc__"] = documentation

    def walk_Species(self, node):
        result = self.walk(node.name)
        name = result["name"]
        namespace = result["namespace"]
        value = self.walk(node.value)
        documentation = self.walk(node.documentation)

        namespace[name] = Species()

        if value:
            namespace[name]["value"] = value

        if documentation:
            namespace[name]["__doc__"] = documentation

    def walk_Reaction(self, node):
        result = self.walk(node.name)

        if result is None:
            name = f"_J{self.numberOfUnnamedReactions}"
            self.numberOfUnnamedReactions += 1
            namespace = self.onemodel
        else:
            name = result["name"]
            namespace = result["namespace"]

        reactants = self.walk(node.reactants)
        products = self.walk(node.products)
        kinetic_law = node.kinetic_law

        namespace[name] = Reaction()

        namespace[name]["reactants"] = []
        for reactant in reactants:
            namespace[name]["reactants"].append(reactant["dotted_name"])

        namespace[name]["products"] = []
        for product in products:
            namespace[name]["products"].append(product["dotted_name"])

        namespace[name]["kinetic_law"] = kinetic_law

    def walk_AssignmentRule(self, node):
        result = self.walk(node.name)

        if result is None:
            name = f"_R{self.numberOfUnnamedReactions}"
            self.numberOfUnnamedReactions += 1
            namespace = self.onemodel
        else:
            name = result["name"]
            namespace = result["namespace"]

        variable = self.walk(node.variable)['dotted_name']
        math = node.math

        namespace[name] = AssignmentRule()
        namespace[name]['variable'] = variable
        namespace[name]['math'] = math

    def walk_AlgebraicRule(self, node):
        result = self.walk(node.name)

        if result is None:
            name = f"_R{self.numberOfUnnamedReactions}"
            self.numberOfUnnamedReactions += 1
            namespace = self.onemodel
        else:
            name = result["name"]
            namespace = result["namespace"]

        variable = self.walk(node.variable)['dotted_name']
        math = node.math

        namespace[name] = AlgebraicRule()
        namespace[name]['variable'] = variable
        namespace[name]['math'] = math

    def walk_RateRule(self, node):
        result = self.walk(node.name)

        if result is None:
            name = f"_R{self.numberOfUnnamedReactions}"
            self.numberOfUnnamedReactions += 1
            namespace = self.onemodel
        else:
            name = result["name"]
            namespace = result["namespace"]

        variable = self.walk(node.variable)['dotted_name']
        math = node.math

        namespace[name] = RateRule()
        namespace[name]['variable'] = variable
        namespace[name]['math'] = math

    def walk_Call(self, node):
        if node.next:
            return self.walk(node.next)

        value = self.walk(node.value)
        args = self.walk(node.args)

        if args == None:
            args = []

        result = value.call(self.onemodel, args)

        if type(result) == list:
            result = result[-1]

        return result

    def walk_AssignName(self, node):
        result = self.walk(node.name)
        name = result["name"]
        namespace = result["namespace"]
        value = self.walk(node.value)

        namespace[name] = value

    def walk_AccessName(self, node):
        result = self.walk(node.name)
        name = result["name"]
        namespace = result["namespace"]

        return namespace[name]

    def walk_DottedName(self, node):
        qualifiers = node.qualifiers
        name = node.name
        namespace = self.onemodel

        dotted_name = ''

        if qualifiers:
            dotted_name = '.'.join(qualifiers)
            dotted_name = dotted_name + '.' + name
        else:
            dotted_name = name

        for qualifier in qualifiers:
            namespace = namespace[qualifier]

        result = {}
        result["name"] = name
        result["namespace"] = namespace
        result["dotted_name"] = dotted_name

        return result

    def walk_Float(self, node):
        return float(node.value)

    def walk_Integer(self, node):
        return int(node.value)

    def walk_Docstring(self, node):
        text = str(node.value)
        lines = text.split("\n")
        result = "\n".join(line.strip() for line in lines)  
        return result
    
    def walk_String(self, node):
        return str(node.value)

    def walk_list(self, nodes):
        """Walk every object in a list. 
        
        Notes
        -----
        If we don't implement this method, the walker will not
        evaluate list nodes.
        """
        results = []

        for node in nodes:
            results.append(self.walk(node))

        return results

    def walk_tuple(self, nodes):
        return self.walk_list(nodes)
