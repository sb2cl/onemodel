import string
from enum import Enum, auto

WHITESPACE = ' \t'
DIGITS = '0123456789'
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
OPERATORS = '+-*/^'

class MathTokenType(Enum):
    """ Math token types that compose a math expression in onemodel.

    This class defines the valid math token types that can be used to form
    mathematical expression in onemodel.
    """
    NUMBER = auto()
    OPERATOR = auto()
    IDENTIFIER = auto()

class MathToken:
    """ This class defines the propeties of MathTokens.

    TODO: Long description.

    Attributes:
        variable: type
    """
    type: MathTokenType
    value: str

    def __init__(self, type_, value=None):
        """ Constructor of MathToken.
        
        Args:
            type_: MathTokenType
                The type of this MathToken.

            value: str
                The value associated to this MathToken. The value of a NUMBER
                will be its numerical respresentation as a string, the value of
                a IDENTIFIER or a FUNCTION is its name.
        """
        self.type = type_
        self.value = value

    def __repr__(self):
        """ REPR method
        """
        if self.value != None:
            return self.type.name + f':{self.value}'
        else:
            return self.type.name

class MathLexer:
    """ MathLexer process a string math expression into MathTokens.

    This class is a lexer that converts string representations of mathematical
    expressions into a list of MathTokens.
    """

    def __init__(self, math_expr):
        """ Constructor of MathLexer.
        
        Args:
            math_expr: str
                String math equation representation .
        """
        self.math_expr = math_expr
        # Init the position.
        self.pos = -1
        # Current char to be processed by the MathLexer.
        self.current_char = None
        # Advance to the first char of the math expression.
        self.advance()
    
    def advance(self):
        """ Advance one char in the math_expr and update current_char.
        """
        # Update the position.
        self.pos += 1
        # Update current_char.
        if self.pos < len(self.math_expr):
            self.current_char = self.math_expr[self.pos]
        else:
            self.current_char = None

    def generate_tokens(self):
        """ Process the math_expr and make the corresponding MathTokens list.
        
        Returns:
            A list of MathToken.
        """
        tokens = []

        # Process all teh chars one by one.
        while self.current_char != None:
            # Remove whitespace.
            if self.current_char in WHITESPACE:
                self.advance()

            elif self.current_char == '.' or self.current_char in DIGITS:
                tokens.append(self.generate_number())

            elif self.current_char in OPERATORS:
                tokens.append(MathToken(MathTokenType.OPERATOR, self.current_char))
                self.advance()

        return tokens

    def generate_number(self):
        """ Generate a number (float).
        
        Generate a NUMBER type MathToken with the value of the number.
                
        Returns:
            A MathToken.
        """
        decimal_point_count = 0
        number_str = self.current_char

        self.advance()

        while self.current_char != None and (self.current_char in (DIGITS+'.')):

            if self.current_char == '.':
                decimal_point_count += 1
                if decimal_point_count > 1:
                    raise ValueError(f"'{self.math_expr}' numbers cannot have two decimal points")

            number_str += self.current_char
            self.advance()

        if number_str.startswith('.'):
            number_str = '0' + number_str
        if number_str.endswith('.'):
            number_str = number_str + '0'

        return MathToken(MathTokenType.NUMBER, number_str)
