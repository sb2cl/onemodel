from onemodel.dsl.context import Context
from onemodel.dsl.values.function_builtin import FunctionBuiltin

class ContextRoot(Context):
    """ The root evaluation context.
    """
    def __init__(self):
        super().__init__('root')

        self.addFunctionBuiltin('print')
        self.addFunctionBuiltin('showContext')
        self.addFunctionBuiltin('strcmp')

    def addFunctionBuiltin(self, name):
        self.set(name, FunctionBuiltin(name))
