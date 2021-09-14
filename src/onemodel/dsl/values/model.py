from onemodel.dsl.values.base_function import BaseFunction
from onemodel.dsl.values.python_value import PythonValue

class Model(BaseFunction):
    """ Definition of OneModel models.
    """
    def __init__(self, name, body_node):
        """ Initialize Model.
        """
        super().__init__(name)
        self.body_node = body_node

    def __str__(self):
        return f"<model {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker

        exec_context = self.generate_new_context()

        walker = OneModelWalker('repl', exec_context)
        walker.walk(self.body_node)

        result = PythonValue(exec_context.symbol_table)

        return result
