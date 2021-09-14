from libsbml import parseL3Formula

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check

class AssignmentRule(Value):
    """ SBML Assignment Rule.
    """
    def __init__(self):
        self.variable = ''
        self.math = ''

    def add_value_to_model(self, name, model):

        math_ast = parseL3Formula(self.math)

        r = model.createAssignmentRule ()

        check(
            r,
            f'create assignment rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set assignment rule id {name}'
        )

        check(
            r.setVariable(self.variable),
            f'set variable on assignment rule {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on assignment rule {name}'
        )


    def __str__(self):
        return '<assignment rule xxx>'

    def __repr__(self):
        return self.__str__()
