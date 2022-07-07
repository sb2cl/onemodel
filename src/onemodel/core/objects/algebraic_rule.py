from libsbml import parseL3Formula

from onemodel.core.utils.check import check
from onemodel.core.utils.math_2_fullname import math_2_fullname
from onemodel.core.objects.object import Object


class AlgebraicRule(Object):

    def __init__(self):
        super().__init__()
        self.variable = ""
        self.math = ""

    def add_to_SBML_model(self, name, scope, model):

        fullname = scope.get_fullname(name)

        # We have to pass the variable to the other equation side.
        math = f"{self.variable} - ({self.math})"
        math_fullname = math_2_fullname(math, scope)
        math_ast = parseL3Formula(math_fullname)

        r = model.createAlgebraicRule()

        check(
            r, 
            f"create algebraic rule {fullname}"
        )

        check(
            r.setIdAttribute(fullname), 
            f"set algebraic rule id {fullname}"
        )

        check(
            r.setMath(math_ast),
            f"set math on algebraic rule {fullname}"
        )
