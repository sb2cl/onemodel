from enum import Enum, auto

class TokenType(Enum):
    """ Token types defined.

    This class defines all the token types available for the lexer.
    """
    INTEGER             = auto()
    FLOAT               = auto()
    STRING              = auto()
    IDENTIFIER          = auto()
    KEYWORD             = auto()
    PLUS                = auto()
    MINUS               = auto()
    MULTIPLY            = auto()
    DIVIDE              = auto()
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


     

