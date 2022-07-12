import libsbml
from libsbml import UNIT_KIND_SECOND, SBMLDocument

from onemodel.core.utils.check import check
from onemodel.core.namespace import Namespace
from onemodel.core.scope import Scope


class OneModel:
    def __init__(self):

        self.model_name = "main"
        self.root = Namespace()
        self.SBML_document = None
        self.SBML_model = None

    def init_SBML_document(self):

        # Create and empty SBMLDocument object.
        try:
            self.document = SBMLDocument(3, 2)
        except ValueError:
            raise SystemExit("Could not create SBMLDocument object")

        # Create the basic Model object inside the SBMLDocument object.
        self.SBML_model = self.document.createModel()
        check(self.SBML_model, "create model")
        check(self.SBML_model.setName(self.model_name), "set model name")
        check(self.SBML_model.setId(self.model_name), "set model id")
        check(self.SBML_model.setTimeUnits("second"), "set model-wide time units")
        check(self.SBML_model.setExtentUnits("mole"), "set model units of extent")
        check(self.SBML_model.setSubstanceUnits("mole"), "set model substance units")

        # Create a unit definition we will need later.
        per_second = self.SBML_model.createUnitDefinition()
        check(per_second, "create unit definition")
        check(per_second.setId("per_second"), "set unit definition id")

        unit = per_second.createUnit()
        check(unit, "create unit on per_second")
        check(unit.setKind(UNIT_KIND_SECOND), "set unit kind")
        check(unit.setExponent(-1), "set unit exponent")
        check(unit.setScale(0), "set unit scale")
        check(unit.setMultiplier(1), "set unit multiplier")

        # Create a default_compartment.
        c = self.SBML_model.createCompartment()

        # TODO: This should be added to root context.
        # self.current_context.set(
        #    'default_compartment',
        #    c
        # )

        check(c, "create default compartment")
        check(c.setId("default_compartment"), "set compartment id")
        check(c.setConstant(True), 'set compartment "constant"')
        check(c.setSize(1), 'set compartment "size"')
        check(c.setSpatialDimensions(3), "set compartment dimensions")
        check(c.setUnits("litre"), "set compartment size units")

    def populate_SBML_document(self, scope=None):

        if scope == None:
            scope = Scope()
            scope.push(self.root, "")

        if scope.peek().is_empty():
            return

        for name, value  in scope.peek().items():
            
            value.add_to_SBML_model(name, scope, self.SBML_model)
            
            scope.push(value, name)
            self.populate_SBML_document(scope)
            scope.pop()

    def get_SBML_string(self):
        self.init_SBML_document()
        self.populate_SBML_document()
        # self.check_SBML_consistency()
        result = libsbml.writeSBMLToString(self.document)

        return result
