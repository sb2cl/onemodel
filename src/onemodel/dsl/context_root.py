from onemodel.dsl.context import Context
from onemodel.dsl.values.function_builtin import FunctionBuiltin

class ContextRoot(Context):
    """ The root evaluation context.
    """
    def __init__(self):
        super().__init__()

        self.addFunctionBuiltin('print')

    def addFunctionBuiltin(self, name):
        self.set(name, FunctionBuiltin(name))
