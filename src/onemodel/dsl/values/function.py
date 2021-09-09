from onemodel.dsl.values.value import Value

class BaseFunction(Value):
    """ Base function class for defining builting functions and user defined
    functions.
    """
    def __init__(self, name = '<anonymous>'):
        """ Initialize BaseFunction.
        """
        super().__init__()
        self.name = name

class BuiltInFunction(BaseFunction):
    """ BuiltInFunctions are functions loaded into the symbol_table.
    """
    def __init__(self, name):
        """ Initialize BuiltInFunction.
        """
        super().__init__(name)

    def __str__(self):
        return f'<built-in function {self.name}>'

    def __repr__(self):
        return self.__str__()

    def __call__(self, *args):
        method_name = f'call_{self.name}'
        method = getattr(self, method_name, None)

        result = method(None)

        return result

    ### Definition of built-in functions as methods ###

    def call_hello_world(self, context):
        """ Hello world built-in function.
        """
        print('Hello world!')

        return None

    call_hello_world.arg_names = []
