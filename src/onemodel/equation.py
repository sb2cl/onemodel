import sympy as sym
from enum import Enum, auto

from onemodel.symbol import Symbol, SymbolType

class EquationType(Enum):
    """ Enum for the different equation types.

    This enum is used for indetifing the type of the equations, we define two
    types of equations:

        1. EQUALITY: expr == expr
        
        The equality type is used when be want to express a relationship
        between expression (or variables) which introduce an algebraic loop.

        2. SUBSTITUTION: identifier := expr
        
        The substitution type is used when we just want to assign a expression to
        a variable, without intoducing more algebraic loops that have to be
        satisfied in simulation time.
    """
    EQUALITY = auto()
    SUBSTITUTION = auto()

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
        # The value must be a string.
        if type(value) != str:
            raise ValueError(f"'{value}' is not a valid type for the 'value' property of '{self._name}', use 'str' type instead.")

        # Check the type of the equation.
        try:
            left, right = value.split('==')

        except: 
            raise ValueError(f"'{value}' must have just one equality sign '==' for the 'value' property of '{self._name}'.")

        # Sympyfy the value and check it is a real number.
        left = sym.sympify(left)
        right = sym.sympify(right)
        eq = sym.Eq(left, right)

        # Just save the evaluation value.
        self._value = eq

    @property
    def left(self):
        """ Get left side of the equation.
        """
        return self.value.lhs
                
    @property
    def right(self):
        """ Get right side of the equation.
        """
        return self.value.rhs
