import sympy as sym

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
        # The value must be a string.
        if type(value) != str:
            raise ValueError(f"'{value}' is not a valid type for the 'value' property of '{self._name}', use 'str' type instead.")

        # Sympyfy the value and check it is a real number.
        value_sym = sym.sympify(value)

        if not value_sym.is_real:
            raise ValueError(f"'{value}' must be a real number for the 'value' property of '{self._name}'.")

        self._value = value_sym
