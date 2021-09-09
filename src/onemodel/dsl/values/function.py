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
    """ BuiltInFunctions are functions hardcoded into the symbol table.
    """
    def __init__(self, name):
        """ Initialize BuiltInFunction.
        """
        super().__init__(name)

    def __str__(self):
        return f'<built-in function {self.name}>'

    def __repr__(self):
        return self.__str__()
