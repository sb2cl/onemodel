import sys

import tatsu
from tatsu.walkers import NodeWalker

from libsbml import *

from onemodel.dsl.values.python_value import PythonValue
from onemodel.dsl.values.species import Species
from onemodel.dsl.values.parameter import Parameter
from onemodel.dsl.values.reaction import Reaction
from onemodel.dsl.values.rate_rule import RateRule
from onemodel.dsl.values.assignment_rule import AssignmentRule
from onemodel.dsl.values.function import Function
from onemodel.dsl.utils import check, getAstNames

class OneModelWalker(NodeWalker):
    def __init__(self, model_name, context):
        # Name for generating files.
        self.model_name = model_name

        # Create context with the symbol table where we will save all objects.
        self.context = context

        # Add this walker to the context.
        self.context.walker = self

        self.document = None
        self.model = None

        self.numReactions = 0
        self.numRules = 0

    def initSBMLDocument(self):
        # Create and empty SBMLDocument object.
        try:
            self.document = SBMLDocument(3, 2)
        except ValueError:
            raise SystemExit('Could not create SBMLDocument object')

        # Create the basic Model object inside the SBMLDocument object.
        self.model = self.document.createModel()
        check(self.model, 'create model')
        check(self.model.setName(self.model_name), 'set model name')
        check(self.model.setId(self.model_name), 'set model id')
        check(self.model.setTimeUnits('second'), 'set model-wide time units')
        check(self.model.setExtentUnits('mole'), 'set model units of extent')
        check(self.model.setSubstanceUnits('mole'), 'set model substance units')

        # Create a unit definition we will need later.
        per_second = self.model.createUnitDefinition()
        check(per_second, 'create unit definition')
        check(per_second.setId('per_second'),'set unit definition id')

        unit = per_second.createUnit()
        check(unit, 'create unit on per_second')
        check(unit.setKind(UNIT_KIND_SECOND),'set unit kind')
        check(unit.setExponent(-1), 'set unit exponent')
        check(unit.setScale(0), 'set unit scale')
        check(unit.setMultiplier(1), 'set unit multiplier')

        # Create a default_compartment.
        c = self.model.createCompartment()

        self.context.symbol_table.set(
            'default_compartment', 
            PythonValue(c)
        )

        check(c, 'create default compartment')
        check(c.setId('default_compartment'), 'set compartment id')
        check(c.setConstant(True), 'set compartment "constant"')
        check(c.setSize(1), 'set compartment "size"')
        check(c.setSpatialDimensions(3), 'set compartment dimensions')
        check(c.setUnits('litre'), 'set compartment size units')

    def populateSBMLDocument(self):
        symbol_table = self.context.symbol_table

        for symbol in symbol_table.symbols:
            value = symbol_table.get(symbol)
            value.add_value_to_model(symbol, self.model)

    def checkConsistency(self):
        if self.document.checkConsistency():
            self.document.printErrors()

    def getSBML(self):
        self.initSBMLDocument()
        self.populateSBMLDocument()
        self.checkConsistency()
        return writeSBMLToString(self.document)

    ### Walk methods ###

    def walk_Species(self, node):
        name = node.name
        value = self.walk(node.value).value

        if value == None:
            value = 0

        s = Species()

        s.initialConcentration = value

        self.context.symbol_table.set(name, s)

        return s

    def walk_Parameter(self, node):
        name = node.name
        value = self.walk(node.value).value

        if value == None:
            value = 0

        if not type(value) in (int, float):
            print('Error: value must be int or float')
            return
            
        p = Parameter()

        p.value = value

        self.context.symbol_table.set(name, p)

        return p

    def walk_Reaction(self, node):
        name = node.name
        reactants = node.reactants
        products = node.products
        kinetic_law_str = node.kinetic_law

        if type(reactants) != list:
            reactants = [reactants] 

        if type(products) != list:
            products = [products] 

        if name == None:
            name = f'_J{self.numReactions}'
            self.numReactions += 1

        # Create reaction.
        r = Reaction()

        r.reactants = reactants
        r.products = products
        r.kinetic_law = kinetic_law_str

        self.context.symbol_table.set(name, r)

        return r

    def walk_RateRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.numRules}'
            self.numRules += 1

        # Create rate rule.
        r = RateRule()

        r.variable = variable
        r.math = math

        self.context.symbol_table.set(name, r)

        return r

    def walk_AssignmentRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.numRules}'
            self.numRules += 1

        r = AssignmentRule()

        r.variable = variable
        r.math = math

        self.context.symbol_table.set(name, r)

        return r

    def walk_AlgebraicRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.model.getNumRules()}'

        # We have to pass the variable to the other equation side.
        math = f'{variable} - ({math})'

        math_ast = parseL3Formula(math)

        r = self.model.createAlgebraicRule ()

        self.context.symbol_table.set(name, PythonValue(r))

        check(
            r,
            f'create algebraic rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set algebraic rule id {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on algebraic rule {name}'
        )

        return r

    def walk_Call(self, node):
        if node.next:
            return self.walk(node.next)

        value = self.walk(node.value)

        arguments = self.walk(node.arguments)

        if arguments == None:
            arguments = []

        if type(arguments) != list:
            arguments = [arguments]

        # TODO: Check that using context this way makes sense.
        value.set_context(self.context)

        result = value(arguments)

        if type(result) == list:
            result = result[-1]

        return result

    def walk_Integer(self, node):
        value = int(node.value)

        return PythonValue(value)

    def walk_Float(self, node):
        value = float(node.value)

        return PythonValue(value)

    def walk_String(self, node):
        value = str(node.value)

        return PythonValue(value)

    def walk_FunctionDefinition(self, node):
        name = node.name
        args = node.args
        body = node.body

        if args == None:
            args = []

        if type(args) != list:
            args = [args]

        f = Function(name, args, body)

        self.context.symbol_table.set(name, f)

        return f

    def walk_AccessProperty(self, node):
        base = node.base
        name = node.name
        
        base = self.context.symbol_table.get(base)
        value = base.get(name)

        return value

    def walk_AccessIdentifier(self, node):
        name = node.name
        value = self.context.symbol_table.get(name)

        return value

    def walk_list(self, nodes):
        results = []

        for node in nodes:
            results.append(self.walk(node))

        if len(results) == 1:
            results = results[0]

        return results

    def walk_object(self, node):
        return node
