from onemodel.dsl.values.function_base import FunctionBase
from onemodel.dsl.values.object import Object

class Model(FunctionBase):
    """ Definiton of Model.
    """
    def __init__(self, name, body_node, parent_class):
        """ Initialize Model.
        """
        super().__init__(name)
        self.body_node = body_node
        self.parent_class = parent_class
                
    def __str__(self):
        return f"<model {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, walker, args):
        calling_context = walker.current_context

        obj = Object(self.name, calling_context)

        walker.current_context = obj 

        parent_class = self.parent_class

        while parent_class != None:
            parent = calling_context.get(self.parent_class)
            walker.walk(parent.body_node)
            parent_class = parent.parent_class

        walker.walk(self.body_node)

        walker.current_context = calling_context

        return obj 

    def add_value_to_model(self, name, model):
        # Models are not added to SBML models.
        pass
