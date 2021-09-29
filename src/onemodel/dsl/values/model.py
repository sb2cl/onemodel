from onemodel.dsl.values.function_base import FunctionBase
from onemodel.dsl.values.object import Object

class Model(FunctionBase):
    """ Definiton of Model.
    """
    def __init__(self, name, body_node, parent_model):
        """ Initialize Model.
        """
        super().__init__(name)
        self.body_node = body_node
        self.parent_model = parent_model

    def execute(self, walker):
        """ Initialize the new object by executing self.body_node in the new
        object context. Also it executes previously the code from parent_model.
        """
        # If model has a parent_model.
        if self.parent_model != None:
            # Excecute first the parent.
            parent = walker.current_context.get(self.parent_model)
            parent.execute(walker)

        # Then execute this model.
        walker.walk(self.body_node)
                
    def __str__(self):
        return f"<model {self.name}>"

    def __repr__(self):
        return self.__str__()

    def __call__(self, walker, args):
        calling_context = walker.current_context

        obj = Object(self.name, calling_context)

        walker.current_context = obj 

        self.execute(walker)

        walker.current_context = calling_context

        return obj 

    def add_value_to_model(self, name, model):
        # Models are not added to SBML models.
        pass
