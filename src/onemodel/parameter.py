from onemodel.symbol import Symbol, SymbolType

class Parameter(Symbol):
    """ This class defines a onemodel parameter.

    A onemodel parameter is a real number which is constant during simulation
    time. Pararameter can be used to define variables and equations.

    Attributes:
        value: num
            Value of the parameter.
    """

    def __init__(self, name):
        """ Inits Parameter.
        
        Args:
            name: str
                Parameter name
        """
        super().__init__(name)
        self.type = SymbolType.PARAMETER
