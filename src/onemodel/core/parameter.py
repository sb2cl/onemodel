from onemodel.core.object import Object


class Parameter (Object):

    def __init__(self):
        super().__init__()

        self.isConstant = True
        self.value = 0
        self.units = None

    def add_to_SBML_model(self):
        pass
