from onemodel.symbol import Symbol, SymbolType

class Equation(Symbol):
    """ This class defines a onemodel equation.

    A onemodel equation are two mathematical expressions joined by an '=='.
    You can define algebraic equations or first order derivative equations.

    Attributes:
        value: TODO:
            The mathematical expression of the equation.
    """

    def __init__(self, name):
        """ Inits Equation.
        
        Args:
            name: str
                Equation name
        """
        super().__init__(name)
        self.type = SymbolType.EQUATION
                
    @Symbol.value.setter
    def value(self, value):
        """ Set value for an equation:
        
        Set value and check if it is valid.
        
        Args:
            value: str
                
        Raises:
            Error: An error.
        """
        # TODO: Check valid type.
        self._value = value
