from libsbml import parseL3Formula

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check, math_2_fullname

class RuleRate(Value):
    """ SBML Rate Rule.
    """
    def __init__(self):
        super().__init__()
        self.variable = ''
        self.math = ''

    def add_value_to_model(self, name, model):
        variable = self.definition_context.getFullname(self.variable)

        aux = math_2_fullname(self.math, self.definition_context)
        math_ast = parseL3Formula(aux)

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
            r.setVariable(variable),
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
