from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check

class Species(Value):
    """ SBML species.
    """
    def __init__(self):
        super().__init__()
        self.compartment = 'default_compartment'
        self.initialConcentration = 0
        self.substanceUnits = 'mole'
        self.constant = False
        self.boundaryCondition = False
        self.hasOnlySubstanceUnits = False

    def add_value_to_model(self, name, model):
        """ Add this value to the SBML model.

        Arguments:
            name: str
                Name of this value.
            model: LibSBML model
                Model to include this value.
        """
        s = model.createSpecies()

        check(
            s, 
            f'create species {name}'
        )

        check(
            s.setId(name), 
            f'set species {name} id'
        )

        check(
            s.setCompartment(self.compartment), 
            f'set species {name} in default_compartment'
        )

        check(
            s.setConstant(self.constant), 
            f'set "constant" attribute on {name}'
        )

        check(
            s.setInitialConcentration(self.initialConcentration), 
            f'set initial amount for {name}'
        )

        check(
            s.setSubstanceUnits(self.substanceUnits), 
            f'set substance units for {name}'
        )

        check(
            s.setBoundaryCondition(self.boundaryCondition),
            f'set "boundaryCondition" on {name}'
        )

        check(
            s.setHasOnlySubstanceUnits(self.hasOnlySubstanceUnits),
            f'set "hasOnlySubstanceUnits" on {name}'
        )

    def __str__(self):
        return f'<species>'
    
    def __repr__(self):
        return self.__str__()
