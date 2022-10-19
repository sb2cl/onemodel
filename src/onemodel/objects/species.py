from onemodel.utils.check import check
from onemodel.objects.object import Object


class Species(Object):
    """A species is a value that changes during simulation time.

    Parameters
    ----------
    compartment : :obj:`str`
    initialConcentration : :obj:`float`
    substanceUnits : :obj:`str`
    constant : :obj:`bool`
    boundaryCondition : :obj:`bool`
    hasOnlySubstanceUnits : :obj:`bool`
    """

    def __init__(self):
        super().__init__()
        self["compartment"] = "default_compartment"
        self["initialConcentration"] = 0
        self["substanceUnits"] = "mole"
        self["constant"] = False
        self["boundaryCondition"] = False
        self["hasOnlySubstanceUnits"] = False

    def add_to_SBML_model(self, name, scope, model):
        """Include this object into a SBML model. """

        fullname = scope.get_fullname(name)

        s = model.createSpecies()

        check(
            s,
            f"create species {fullname}"
        )

        check(
            s.setId(fullname), 
            f"set species {fullname} id"
        )

        check(
            s.setCompartment(self["compartment"]), 
            f"set species {fullname} in default_compartment"
        )

        check(
            s.setConstant(self["constant"]), 
            f'set "constant" attribute on {fullname}'
        )

        check(
            s.setInitialConcentration(self["initialConcentration"]), 
            f"set initial amount for {fullname}"
        )

        check(
            s.setSubstanceUnits(self["substanceUnits"]), 
            f"set substance units for {fullname}"
        )

        check(
            s.setBoundaryCondition(self["boundaryCondition"]), 
            f'set "boundaryCondition" on {fullname}'
        )

        check(
            s.setHasOnlySubstanceUnits(self["hasOnlySubstanceUnits"]),
            f'set "hasOnlySubstanceUnits" on {fullname}',
        )

    def __repr__(self):
        result = "<species"
        result += f" initialConcentration={self['initialConcentration']}"
        result += ">"

        return result
