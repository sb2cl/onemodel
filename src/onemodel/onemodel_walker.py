import os
from importlib_resources import files
import tatsu
from tatsu.walkers import NodeWalker
from onemodel.onemodel import OneModel
from onemodel.objects.object import Object
from onemodel.objects.parameter import Parameter
from onemodel.objects.species import Species
from onemodel.objects.reaction import Reaction
from onemodel.objects.assignment_rule import AssignmentRule
from onemodel.objects.algebraic_rule import AlgebraicRule
from onemodel.objects.rate_rule import RateRule
from onemodel.objects.function import Function
from onemodel.objects.model import Model
from onemodel.objects.module import Module
from onemodel.objects.module import find_module
from onemodel.objects.module import load_module
from onemodel.builtin_functions import load_builtin_functions

def evaluate(code):
    """Evaluate OneModel code."""

    walker = OneModelWalker()
    result, ast = walker.run(code)

    onemodel = walker.onemodel
    return walker.onemodel

def load_file(filename):
    """Load a file into OneModel. """

    filepath = os.path.abspath(filename)
    file = open(filepath)
    text = file.read()
    file.close()

    walker = OneModelWalker(file=filepath)
    result, ast = walker.run(text)
    
    onemodel = walker.onemodel

    return onemodel

class OneModelWalker(NodeWalker):

    numberOfUnnamedReactions = 0
    numberOfUnnamedRules = 0
    
    def __init__(self, file=None):
        self.onemodel = OneModel()
        self.onemodel["__name__"] = "__main__"
        self.onemodel["__exit__"] = False

        if file:
            self.onemodel["__file__"] = file
            basename = os.path.basename(file)
            basename_without_extension = os.path.splitext(basename)[0]
            self.onemodel.model_name = basename_without_extension
        else:
            self.onemodel["__file__"] = os.path.abspath(os.getcwd())

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

    def walk_InverseAddition(self, node):
        base = self.walk(node.base)
        return - base

    def walk_Power(self, node):
        base = self.walk(node.base)

        if node.exponent is None:
            return base

        exponent = self.walk(node.exponent)
        return base ** exponent

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

    def walk_Import(self, node):
        dots_number = len(node.dots)
        qualifiers = node.qualifiers
        module_name = node.module_name
        import_name = node.import_name
        assign_name = node.assign_name

        load_module(
            self, 
            module_name, 
            import_name, 
            assign_name, 
            qualifiers,
            dots_number
        )

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
            namespace[name]["initialConcentration"] = value
        else:
            namespace[name]["initialConcentration"] = 0

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

        documentation = self.walk(node.documentation)
        if documentation:
            namespace[name]["__doc__"] = documentation

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

        documentation = self.walk(node.documentation)
        if documentation:
            namespace[name]["__doc__"] = documentation


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

        documentation = self.walk(node.documentation)
        if documentation:
            namespace[name]["__doc__"] = documentation

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

        documentation = self.walk(node.documentation)
        if documentation:
            namespace[name]["__doc__"] = documentation

    def walk_Extends(self, node):
        model = self.walk(node.model)
        result = model.extend()

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

    def walk_FunctionDefinition(self, node):
        name = node.name
        args = node.args
        body = node.body

        if args == None:
            args = []

        namespace = self.onemodel

        namespace[name] = Function()
        namespace[name]["argument_names"] = args
        namespace[name]["body"] = body
        namespace[name].walker = self

        return namespace[name]

    def walk_ModelDefinition(self, node):
        name = node.name
        body = node.body

        namespace = self.onemodel

        namespace[name] = Model()
        namespace[name]["body"] = body
        namespace[name].walker = self

        return namespace[name]

    def walk_Standalone(self, node):

        if self.onemodel["__name__"] == "__main__":
            return self.walk(node.body)

        return None

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
