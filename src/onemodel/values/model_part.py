from onemodel.values.value import Value

class ModelPart(Value):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return f"{self.name}"
