import sys

from importlib_resources import files

import tatsu
from tatsu.walkers import NodeWalker

from libsbml import *

from onemodel.dsl.context import Context
from onemodel.dsl.context_root import ContextRoot

from onemodel.dsl.values.species import Species
from onemodel.dsl.values.parameter import Parameter
from onemodel.dsl.values.reaction import Reaction
from onemodel.dsl.values.rule_rate import RuleRate
from onemodel.dsl.values.rule_assignment import RuleAssignment
from onemodel.dsl.values.rule_algebraic import RuleAlgebraic
from onemodel.dsl.values.number import Number
from onemodel.dsl.values.string import String
from onemodel.dsl.values.struct import Struct
from onemodel.dsl.values.function import Function
from onemodel.dsl.values.model import Model

from onemodel.dsl.utils import check, getAstNames

class OneModelWalker(NodeWalker):
    def __init__(self, model_name, context = None):
        # Name for generating files.
        self.model_name = model_name

        # If context is passed.
        if context:
            # Save it.
            self.current_context = context
        else:
            # If not, generate a root context.
            self.current_context = ContextRoot()

        # SBMLDocument and SBMLModel
        self.document = None
        self.model = None

        # Keep track of number of unnamed reactions and rules.
        self.numReactions = 0
        self.numRules = 0

        # Filepath of the text which is being executed with self.run().
        self.filepath_running = None

        # Are we importing code from other file?
        self.isImporting = False

        # Load the grammar.
        self.grammar = files('onemodel.dsl').joinpath('onemodel.ebnf').read_text()

        # Load the parser with the grammar.
        self.parser = tatsu.compile(self.grammar, asmodel=True)

    def run(self, text, filepath=None):
        # If filepath is none, the text does not proceed from
        # a file.

        # Save previous filepath.
        filepath_previous = self.filepath_running

        # Set current filepath.
        self.filepath_running = filepath

        model = self.parser.parse(text)
        result = self.walk(model)

        # Restore previous filepath.
        self.filepath_running = filepath_previous

        return result

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
    

        # TODO: This should be added to root context.
        #self.current_context.set(
        #    'default_compartment', 
        #    c
        #)

        check(c, 'create default compartment')
        check(c.setId('default_compartment'), 'set compartment id')
        check(c.setConstant(True), 'set compartment "constant"')
        check(c.setSize(1), 'set compartment "size"')
        check(c.setSpatialDimensions(3), 'set compartment dimensions')
        check(c.setUnits('litre'), 'set compartment size units')

    def populateSBMLDocument(self):
        for symbol in self.current_context.symbols:
            value = self.current_context.get(symbol)
            value.add_value_to_model(symbol, self.model)

    def checkConsistency(self):
        if self.document.checkConsistency():
            self.document.printErrors()

    def getSBML(self):
        self.initSBMLDocument()
        self.populateSBMLDocument()
        self.checkConsistency()
        sbml = writeSBMLToString(self.document)
        return sbml

    ### Walk methods ###

    def walk_Import(self, node):
        import os

        filepath = self.walk(node.filepath).value

        f = os.path.abspath(self.filepath_running)
        f = os.path.dirname(f)
        f = os.path.join(f, filepath)
        f = os.path.abspath(f)

        text = open(f).read()

        # Save current self.isImporting.
        aux = self.isImporting
        # Set it to true.
        self.isImporting = True

        self.run(text, f)

        # Restores old self.isImporting.
        self.isImporting = aux

        return

    def walk_Standalone(self, node):
        if self.isImporting == False:
            return self.walk(node.code)

        return

    def walk_Species(self, node):
        name = node.name
        value = self.walk(node.value).value

        context = self.current_context

        if type(name) == list:
            for i in range(len(name)-1):
                context = context.get(name[i])
            name = name[-1]

        if value == None:
            value = 0

        if not type(value) in (int, float):
            print('Error: value must be int or float')
            return
 
        s = Species()

        s.initialConcentration = value

        context.set(name, s)

        return s

    def walk_Parameter(self, node):
        name = node.name
        value = self.walk(node.value)

        context = self.current_context

        if type(name) == list:
            for i in range(len(name)-1):
                context = context.get(name[i])
            name = name[-1]

        if value != None: 
            value = value.value
        else:
            value = 0

        if not type(value) in (int, float):
            print('Error: value must be int or float')
            return
            
        p = Parameter()

        p.value = value

        context.set(name, p)

        return p

    def walk_Reaction(self, node):
        name = node.name
        reactants = self.walk(node.reactants)
        products = self.walk(node.products)
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

        self.current_context.set(name, r)

        return r

    def walk_RuleRate(self, node):
        name = node.name
        variable = self.walk(node.variable)
        math = node.math

        if not isinstance(variable, Species):
            raise TypeError('variable must be "Species"')

        if type(name) == list:
            full_name = ''
            for item in name:
                full_name += item + '__'
            name = full_name[0:-2]

        if name == None:
            name = f'_R{self.numRules}'
            self.numRules += 1

        # Create rate rule.
        r = RuleRate()

        r.variable = variable.getFullname()
        r.math = math

        self.current_context.set(name, r)

        return r

    def walk_RuleAssignment(self, node):
        name = node.name
        variable = self.walk(node.variable)
        math = node.math

        if not isinstance(variable, Species):
            raise TypeError('variable must be "Species"')

        if name == None:
            name = f'_R{self.numRules}'
            self.numRules += 1

        if type(name) == list:
            full_name = ''
            for item in name:
                full_name += item + '__'
            name = full_name[0:-2]

        r = RuleAssignment()

        r.variable = variable.getFullname()
        r.math = math

        self.current_context.set(name, r)

        return r

    def walk_RuleAlgebraic(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.numRules}'
            self.numRules += 1

        r = RuleAlgebraic()

        r.variable = variable
        r.math = math

        self.current_context.set(name, r)

        return r

    def walk_Input(self, node):
        name = node.name

        # Set default value to cero.
        value = 0

        s = Species()

        s.initialConcentration = value
        self.current_context.set(name, s)

        return s

    def walk_AssignVariable(self, node):
        name = node.name
        value = self.walk(node.value)

        context = self.current_context

        if type(name) == list:
            for i in range(len(name)-1):
                context = context.get(name[i])

            context.set(name[-1], value)
        else:
            context.set(name, value)

        return value

    def walk_Call(self, node):
        if node.next:
            return self.walk(node.next)

        value = self.walk(node.value)
        args = self.walk(node.args)

        if args == None:
            args = []

        if type(args) != list:
            args = [args]

        result = value.__call__(
            self,
            args
        )

        if type(result) == list:
            result = result[-1]

        return result

    def walk_Float(self, node):
        value = float(node.value)

        value = Number(value)

        return value

    def walk_Integer(self, node):
        value = int(node.value)

        value = Number(value)

        return value

    def walk_String(self, node):
        value = str(node.value)
        
        value = String(value)

        return value

    def walk_Struct(self, node):
        struct = Struct()

        return struct

    def walk_AccessIdentifier(self, node):
        name = node.name

        context = self.current_context

        if type(name) == list:
            for i in range(len(name)-1):
                context = context.get(name[i])

            value = context.get(name[-1])
        else:
            value = context.get(name)

        return value

    def walk_If(self, node):
        condition = self.walk(node.condition)
        body = node.body

        if bool(condition):
            self.walk(body)

        return

    def walk_FunctionDefinition(self, node):
        name = node.name
        args = node.args
        body = node.body

        if args == None:
            args = []

        if type(args) != list:
            args = [args]

        function = Function(
                name,
                args,
                body)

        self.current_context.set(name, function)

        return function

    def walk_ModelDefinition(self, node):
        name = node.name
        body = node.body
        parent_model = node.parent_model

        m = Model(name, body, parent_model)

        self.current_context.set(name, m)

        return m

    def walk_list(self, nodes):
        results = []

        for node in nodes:
            results.append(self.walk(node))

        if len(results) == 1:
            results = results[0]

        return results

    def walk_tuple(self, nodes):
        return self.walk_list(nodes)

    def walk_object(self, node):
        return node
