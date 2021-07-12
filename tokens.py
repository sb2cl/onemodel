from enum import Enum, auto
from dataclasses import dataclass

class TokenType(Enum):
    """ TOKENTYPE

    This class defines all the token types available for the lexer.
    """
    NUMBER              = auto()
    STRING              = auto()
    IDENTIFIER          = auto()
    KEYWORD             = auto()
    PLUS                = auto()
    MINUS               = auto()
    MULTIPLICATION      = auto()
    DIVISION            = auto()
    POWER               = auto()
    EQUAL               = auto()
    LEFT_PAREN          = auto()
    RIGHT_PAREN         = auto()
    LEFT_SQUARE         = auto()
    RIGHT_SQUARE        = auto()
    IS_EQUAL            = auto()
    NOT_EQUAL           = auto()
    LESS_THAN           = auto()
    GREATER_THAN        = auto()
    LESS_EQUAL_THAN     = auto()
    GREATER_EQUAL_THAN  = auto()
    COMMA               = auto()
    ARROW               = auto()
    NEW_LINE            = auto()
    END_OF_FILE         = auto()

@dataclass
class Token:
    """ TOKEN

    This class implements a Token.
    """
    # The token type
    type: TokenType   
    # The token value
    value: any = None

    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        """ __INIT__
        @brief: Constructor of Token class.
        
        @param: type_      TokenType of the token.
              : value=None The value of the token.
              : pos_start  The start position of the token.
              : pos_end    The end position of the token.
        """
        self.type = type_
        self.value = value

        # If pos_start is passed
        if pos_start:
            # Save a copy of it
            self.pos_start = pos_start.copy()
            # And save it as the position end (in case it is a one-char token)
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        # If pos_end is passed
        if pos_end:
            # Save a copy of it
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        """ MATCHES
        @brief: Check it the token matches type_ and value passed.
        
        @param: type_ TokenType
              : value Value of the token.
                
        @return: True if Token matches the type_ and value.
        """
        return self.type == type_ and self.value == value
  
    def __repr__(self):
        """ __REPR__
        @brief: Returns a string representation of the Token.
        
        @return: string
        """
        return self.type.name + (f":{self.value}" if self.value != None else "")

    def __eq__(self,other):
        """ __EQ__
        @brief: Override equality operator to only take into account type and value.
        
        @param: other Token
                
        @return: True if the have equal type and value
        """
        return self.type == other.type and str(self.value) == str(other.value) 
