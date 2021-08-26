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
    ODE = auto()
    ALGEBRAIC = auto()
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
        self.variable = None
        self.equation_type = None
                
    @Symbol.value.setter
    def value(self, value):
        """ Set value for an equation:
        
        Set value and check if it is valid.
        
        Args:
            value: str
                
        Raises:
            Error: An error.
        """

        # Check if value is already a sympy expression.
        if isinstance(value, sym.Expr):
            self._value = value
            return

        # If the value is a str.
        if type(value) in (int, float, str):
            # Convert it into a sympy value.
            self._value = sym.sympify(value)
            return

        raise ValueError(f"'{value}' is not a valid type for the 'value' property of '{self._name}', use 'sympy.Expr', 'int', 'float' or 'str' instead.")

    @property
    def variable_name(self):
        """ The name of the varible which is calculated with this equation.

        """
        return self._variable_name

    @variable_name.setter
    def variable_name(self, variable_name):
        """ Setter for variable_name
        
        Args:
            variable_name: str
        """
        self._variable_name = variable_name

    @property
    def equation_type(self):
        """ The type of the equation.

        """
        return self._equation_type

    @equation_type.setter
    def equation_type(self, equation_type):
        """ Setter for equation_type
        
        Args:
            equation_type: EquationType
        """
        self._equation_type = equation_type
