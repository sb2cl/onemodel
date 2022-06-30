from onemodel.core.utils.check import check
from onemodel.core.objects.object import Object


class Parameter(Object):
    def __init__(self):
        super().__init__()

        self.isConstant = True
        self.value = 0
        self.units = "per_second"

    def add_to_SBML_model(self, name, model):
        p = model.createParameter()

        check(p, f"create parameter {name}")

        check(p.setId(name), f"set parameter {name} id")

        check(p.setConstant(self.isConstant), f'set parameter {name} "constant"')

        check(p.setValue(self.value), f"set parameter {name} value")

        check(p.setUnits(self.units), f"set parameter {name} units")
