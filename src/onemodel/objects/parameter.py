from onemodel.utils.check import check
from onemodel.objects.object import Object


class Parameter(Object):
    """A parameter is a value constant during simulation time.

    Parameters
    ----------
    isConstant : :obj:`bool`
        True if the parameter is constant, Flase otherwise.

    value : :obj:`float`
        Numeric value of the parameter.

    units : :obj:`str`
        Units of the parameter.
    """

    def __init__(self):
        super().__init__()

        self["isConstant"] = True
        self["value"] = 0
        self["units"] = "per_second"

    def add_to_SBML_model(self, name, scope, model):
        """Include this object into a SBML model. """

        fullname = scope.get_fullname(name)

        p = model.createParameter()

        check(
            p,
            f"create parameter {fullname}"
        )

        check(
            p.setId(fullname), 
            f"set parameter {fullname} id"
        )

        check(
            p.setConstant(self["isConstant"]), 
            f'set parameter {fullname} "constant"'
        )

        check(
            p.setValue(self["value"]), 
            f"set parameter {fullname} value"
        )

        check(
            p.setUnits(self["units"]), 
            f"set parameter {fullname} units"
        )

    def __repr__(self):
        result = "<parameter "
        result += f"value={self['value']}>"

        return result
