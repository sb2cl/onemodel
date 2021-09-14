from libsbml import parseL3Formula

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check

class AlgebraicRule(Value):
    """ SBML Algebraic Rule.
    """
    def __init__(self):
        self.variable = ''
        self.math = ''

    def add_value_to_model(self, name, model):
        # We have to pass the variable to the other equation side.
        math = f'{self.variable} - ({self.math})'

        math_ast = parseL3Formula(math)

        r = model.createAlgebraicRule ()

        check(
            r,
            f'create algebraic rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set algebraic rule id {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on algebraic rule {name}'
        )
