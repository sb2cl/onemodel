from onemodel.symbol import Symbol, SymbolType

class Variable(Symbol):
    """ This class defines a onemodel variable.

    A onemodel varible is a real number which can change during simulation
    time. The value property is the start value at the beggining of the
    simulation. 

    Attributes:
        value: num
            Value of the variable at the start of simlation.
    """

    def __init__(self, name):
        """ Inits Variable.
        
        Args:
            name: str
                Variable name
        """
        super().__init__(name)
        self.type = SymbolType.VARIABLE
    
    @Symbol.value.setter
    def value(self, value):
        """ Set value for a variable:
        
        Set value and check if it is valid.
        
        Args:
            value: str
                
        Raises:
            Error: An error.
        """
        # TODO: Check valid type.
        self._value = value
                
