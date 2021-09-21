from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check

class Parameter(Value):
    """ SBML Parameter.
    """
    def __init__(self):
        super().__init__()
        self.constant = True
        self.value = 0
        self.units = 'per_second'

    def add_value_to_model(self, name, model):
        """ Add this value to the SBML model.

        Arguments:
            name: str
                Name of this value.
            model: LibSBML model
                Model to include this value.
        """
        p = model.createParameter()

        check(
            p,
            f'create parameter {name}'
        )

        check(
            p.setId(name),
            f'set parameter {name} id'
        )

        check(
            p.setConstant(self.constant),
            f'set parameter {name} "constant"'
        )

        check(
            p.setValue(self.value),
            f'set parameter {name} value'
        )

        check(
            p.setUnits(self.units),
            f'set parameter {name} units'
        )
 
    def __str__(self):
        return f'<parameter>'
    
    def __repr__(self):
        return self.__str__()
