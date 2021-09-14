from libsbml import parseL3Formula

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check

class RateRule(Value):
    """ SBML Rate Rule.
    """
    def __init__(self):
        self.variable = ''
        self.math = ''

    def add_value_to_model(self, name, model):

        math_ast = parseL3Formula(self.math)

        r = model.createRateRule()

        check(
            r,
            f'create rate rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set rate rule id {name}'
        )

        check(
            r.setVariable(self.variable),
            f'set variable on rate rule {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on rate rule {name}'
        )

    def __str__(self):
        return '<rate rule>'

    def __repr__(self):
        return self.__str__()
