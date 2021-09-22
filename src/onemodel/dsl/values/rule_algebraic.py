from libsbml import parseL3Formula

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check, math_2_fullname

class RuleAlgebraic(Value):
    """ SBML Algebraic Rule.
    """
    def __init__(self):
        super().__init__()
        self.variable = ''
        self.math = ''

    def add_value_to_model(self, name, model):
        # We have to pass the variable to the other equation side.
        math = f'{self.variable} - ({self.math})'

        aux = math_2_fullname(math, self.definition_context)
        math_ast = parseL3Formula(aux)

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

    def __str__(self):
        return '<algebraic rule>'

    def __repr__(self):
        return self.__str__()
