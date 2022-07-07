from onemodel.core.utils.check import check
from onemodel.core.objects.object import Object


class Parameter(Object):

    def __init__(self):
        super().__init__()

        self.isConstant = True
        self.value = 0
        self.units = "per_second"

    def add_to_SBML_model(self, name, scope, model):
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
            p.setConstant(self.isConstant), 
            f'set parameter {fullname} "constant"'
        )

        check(
            p.setValue(self.value), 
            f"set parameter {fullname} value"
        )

        check(
            p.setUnits(self.units), 
            f"set parameter {fullname} units"
        )
