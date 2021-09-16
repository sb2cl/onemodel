from onemodel.dsl.values.base_function import BaseFunction
from onemodel.dsl.values.python_value import PythonValue
from onemodel.dsl.values.object import Object

class Model(BaseFunction):
    """ Definition of OneModel models.
    """
    def __init__(self, name, body_node):
        """ Initialize Model.
        """
        super().__init__(name)
        self.body_node = body_node

    def add_value_to_model(self, name, model):
        # Models are not included in SBML models.
        pass

    def __str__(self):
        return f"<model {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker

        obj = Object()
        obj.context.parent = self.definition_context
        print('??????' + obj.context.parent.namespace)

        walker = OneModelWalker('repl', obj.context)
        walker.walk(self.body_node)

        return obj 
