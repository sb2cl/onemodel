from libsbml import parseL3Formula

from onemodel.core.utils.check import check
from onemodel.core.utils.math_2_fullname import math_2_fullname
from onemodel.core.objects.object import Object


class RateRule(Object):

    def __init__(self):
        super().__init__()
        self.variable = ""
        self.math = ""

    def add_to_SBML_model(self, name, scope, model):
        variable_fullname = scope.get_fullname(self.variable)

        math_fullname = math_2_fullname(self.math, scope)
        math_ast = parseL3Formula(math_fullname)

        r = model.createRateRule()

        check(
            r, 
            f"create rate rule {name}"
        )

        check(
            r.setIdAttribute(name), 
            f"set rate rule id {name}"
        )

        check(
            r.setVariable(variable_fullname), 
            f"set variable on rate rule {name}"
        )

        check(
            r.setMath(math_ast), 
            f"set math on rate rule {name}"
        )
