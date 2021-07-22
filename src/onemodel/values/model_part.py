from onemodel.values.value import Value

class ModelPart(Value):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def is_true(self):
        return self.value != 0

    def copy(self):
        copy = ModelPart(self.name)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return f"{self.name}"
