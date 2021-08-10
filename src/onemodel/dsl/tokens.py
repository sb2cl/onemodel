from enum import Enum, auto
from dataclasses import dataclass
from onemodel.dsl.position import Position

class TokenType(Enum):
    """ This class defines all the token types available for the lexer.

    """
    NUMBER        = auto()
    STRING        = auto()
    IDENTIFIER    = auto()
    KEYWORD       = auto()
    MATH_OPERATOR = auto() # '+' '-' '*' '/' '^'
    EQUAL         = auto() # '='
    EQUALITY      = auto() # '=='
    ASSIGN        = auto() # ':='
    L_PAREN       = auto() # '('
    R_PAREN       = auto() # ')'
    L_SQUARE      = auto() # '['
    R_SQUARE      = auto() # ']'
    L_BRACKET     = auto() # '{'
    R_BRACKET     = auto() # '}'
    COMMA         = auto() # ','
    NEW_LINE      = auto()
    END_OF_FILE   = auto()

@dataclass
class Token:
    """ This class implements a Token for the Lexer.

    """
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        """ __INIT__
        @brief: Constructor of Token class.
        
        @param: type_: TokenType TokenType of the token.
              : value: Any The value of the token.
              : pos_start: Positon The start position of the token.
              : pos_end: Positon The end position of the token.
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
        if other == None: 
            return False

        if self.value == None and other.value == None:
            if self.type == other.type:
                return True

        return self.type == other.type and str(self.value) == str(other.value) 
