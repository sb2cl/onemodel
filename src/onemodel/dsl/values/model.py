from onemodel.dsl.values.function_base import FunctionBase
from onemodel.dsl.values.object import Object

class Model(FunctionBase):
    """ Definiton of Model.
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

    def __call__(self, calling_context, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker

        obj = Object(self.name, calling_context)

        walker = OneModelWalker('repl_2', obj)

        #import pdb
        #pdb.set_trace()

        #walker.walk(self.body_node)

        return obj 
