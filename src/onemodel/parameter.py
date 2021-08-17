import sympy as sym

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

    @Symbol.value.setter
    def value(self, value):
        """ Set value for a parameter.
        
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

        # Just save the evaluation value.
        self._value = value_sym.evalf()

    def __add__(self, other):
        """ Define __add__ method.
        """
        return sym.sympify(self.name) + other

    def __radd__(self, other):
        """ Define __radd__ method.
        """
        return self.__add__(other)

    def __sub__(self, other):
        """ Define __sub__ method.
        """
        return sym.sympify(self.name) - other

    def __rsub__(self, other):
        """ Define __rsub__ method.
        """
        return self.__sub__(other)

    def __mul__(self, other):
        """ Define __mul__ method.
        """
        return sym.sympify(self.name) * other

    def __rmul__(self, other):
        """ Define __rmul__ method.
        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """ Define __div__ method.
        """
        return sym.sympify(self.name) / other

    def __rtruediv__(self, other):
        """ Define __rtruediv__ method.
        """
        return other / sym.sympify(self.name)

    def __pow__(self, other):
        """ Define __pow__ method.
        """
        return sym.sympify(self.name) ** other

    def __rpow__(self, other):
        """ Define __rpow__ method.
        """
        return other ** sym.sympify(self.name)

 
