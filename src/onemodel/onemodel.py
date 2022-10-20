import libsbml
from libsbml import UNIT_KIND_SECOND, SBMLDocument

from onemodel.utils.check import check
from onemodel.namespace import Namespace
from onemodel.scope import Scope
from onemodel.objects.object import Object

class OneModel(Scope):
    """OneModel contains the root namespace where we define the models.

    The class OneModel is the semantic model of the OneModel syntax. OneModel
    defines the root namespace in which we define the objects that form our
    models.

    Parameters
    ----------
    model_name : :obj:`str`
        The name of the model.

    root : :obj:`Namespace`
        The root namespace of the model.
    """

    def __init__(self):
        super().__init__()

        self.model_name = "main"
        self.root = Namespace()
        self.locals = Namespace()

        self.push(self.root, "")
        self.locals = Namespace()

    def get_SBML_string(self):
        """Returns a SBML representation of the model. """

        # Perform self.pop() until the root namespace.
        while len(self.namespaces) > 1:
            self.pop()

        SBML_document, SBML_model = self._init_SBML_document()
        self._populate_SBML_document(SBML_model)
        # self.check_SBML_consistency()
        result = libsbml.writeSBMLToString(SBML_document)

        return result

    def _init_SBML_document(self):
        """Initializes the SBML document. """

        # Create and empty SBMLDocument object.
        try:
            SBML_document = SBMLDocument(3, 2)
        except ValueError:
            raise SystemExit("Could not create SBMLDocument object")

        # Create the basic Model object inside the SBMLDocument object.
        SBML_model = SBML_document.createModel()
        check(SBML_model, "create model")
        check(SBML_model.setName(self.model_name), "set model name")
        check(SBML_model.setId(self.model_name), "set model id")
        check(SBML_model.setTimeUnits("second"), "set model-wide time units")
        check(SBML_model.setExtentUnits("mole"), "set model units of extent")
        check(SBML_model.setSubstanceUnits("mole"), "set model substance units")

        # Create a unit definition we will need later.
        per_second = SBML_model.createUnitDefinition()
        check(per_second, "create unit definition")
        check(per_second.setId("per_second"), "set unit definition id")

        unit = per_second.createUnit()
        check(unit, "create unit on per_second")
        check(unit.setKind(UNIT_KIND_SECOND), "set unit kind")
        check(unit.setExponent(-1), "set unit exponent")
        check(unit.setScale(0), "set unit scale")
        check(unit.setMultiplier(1), "set unit multiplier")

        # Create a default_compartment.
        c = SBML_model.createCompartment()

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

        return SBML_document, SBML_model

    def _populate_SBML_document(self, SBML_model):
        """Populates the SBML with the objects in the root namespace."""

        for name, value in self.peek().items():

            if not isinstance(value, Object):
                continue

            value.add_to_SBML_model(name, self, SBML_model)
            self.push(value, name)
            self._populate_SBML_document(SBML_model)
            self.pop()

    def __str__(self):
        from tabulate import tabulate

        data = []

        for name in reversed(list(self.root.keys())):
            if name.startswith('__'):
                continue

            if name in ["show", "locals", "globals", "print", "exit"]:
                continue

            value = repr(self.root[name])

            if isinstance(self.root[name], dict):
                doc = self.root[name]['__doc__']
            else:
                doc =""

            row = [name, value, doc]
            data.append(row)

        result = tabulate(data, headers=['Name', 'Value', 'Documentation'])

        return result
