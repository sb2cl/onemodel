from onemodel.core.check import check
from onemodel.core.objects.object import Object


class Species(Object):

    def __init__(self):
        super().__init__()
        self.compartment = 'default_compartment'
        self.initialConcentration = 0
        self.substanceUnits = 'mole'
        self.constant = False
        self.boundaryCondition = False
        self.hasOnlySubstanceUnits = False

    def add_to_SBML_model(self, name, model):
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
