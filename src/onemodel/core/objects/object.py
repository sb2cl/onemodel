from onemodel.core.namespace import Namespace

class Object(Namespace):

    def __init__(self):
        super().__init__(None)

    def add_to_SBML_model(self, name, model):
        raise Exception(f'Class "{type(self).__name__}" has not defined add_to_SBML method.')
