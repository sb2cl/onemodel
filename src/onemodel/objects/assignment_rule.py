from libsbml import parseL3Formula

from onemodel.utils.check import check
from onemodel.utils.math_2_fullname import math_2_fullname
from onemodel.objects.object import Object


class AssignmentRule(Object):
    """An equation that sets the value of a Species.

    Parameters
    ----------
    variable : :obj:`str`
        The name of the species to set the value.
    math : :obj:`str`
        The math expression to evaluate.
    """

    def __init__(self):
        super().__init__()
        self["variable"] = ""
        self["math"] = ""

    def add_to_SBML_model(self, name, scope, model):
        """Include this object into a SBML model. """

        fullname = scope.get_fullname(name)

        variable_fullname = scope.get_fullname(self["variable"])

        math_fullname = math_2_fullname(self["math"], scope)
        math_ast = parseL3Formula(math_fullname)

        r = model.createAssignmentRule()

        check(
            r, 
            f"create assignment rule {fullname}"
        )

        check(
            r.setIdAttribute(fullname), 
            f"set assignment rule id {fullname}"
        )

        check(
            r.setVariable(variable_fullname),
            f"set variable on assignment rule {fullname}"
        )

        check(
            r.setMath(math_ast),
            f"set math on assignment rule {fullname}"
        )

    def __repr__(self):
        result = "<assignment-rule"
        result += f" eq='{self['variable']} := {self['math'].strip()}'"
        result += ">"

        return result
