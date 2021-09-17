import sys

from importlib_resources import files

import tatsu
from tatsu.walkers import NodeWalker

from libsbml import *

from onemodel.dsl.context import Context
from onemodel.dsl.context_root import ContextRoot

from onemodel.dsl.values.number import Number
from onemodel.dsl.values.function import Function

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

        # Add this walker to the context.
        self.current_context.walker = self

        # SBMLDocument and SBMLModel
        self.document = None
        self.model = None

        # Keep track of number of unnamed reactions and rules.
        self.numReactions = 0
        self.numRules = 0

        # Load the grammar.
        self.grammar = files('onemodel.dsl').joinpath('onemodel.ebnf').read_text()

        # Load the parser with the grammar.
        self.parser = tatsu.compile(self.grammar, asmodel=True)

    def run(self, text):
        model = self.parser.parse(text)
        result = self.walk(model)

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

        self.current_context.set(
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
        return writeSBMLToString(self.document)

    ### Walk methods ###

    def walk_AssignVariable(self, node):
        name = node.name
        value = self.walk(node.value)

        self.current_context.set(name, value)

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
            self.current_context,
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

        return value

    def walk_AccessIdentifier(self, node):
        name = node.name
        value = self.current_context.get(name)

        return value

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

    def walk_list(self, nodes):
        results = []

        for node in nodes:
            results.append(self.walk(node))

        if len(results) == 1:
            results = results[0]

        return results

    def walk_object(self, node):
        return node
