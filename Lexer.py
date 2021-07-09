from enum import Enum, auto
from Position import Position

class TokenType(Enum):
    """ TOKENTYPE

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

# Keywords reserved for tokens.
KEYWORDS = [
        'VAR',
        'AND',
        'OR',
        'NOT',
        'IF',
        'ELIF',
        'ELSE',
        'FOR',
        'TO',
        'STEP',
        'WHILE',
        'FUN',
        'THEN',
        'END',
        'RETURN',
        'CONTINUE',
        'BREAK',
        ]

class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        return self.type == type_ and self.value == value
  
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    """ LEXER

    This class takes input text and generates a list of tokens.
    """

    def __init__(self,fn,text):
        """
        @brief: Constructor of Lexer.
        
        @param: fn   Filename of the text (used in error generation).
              : text Input text to convert into tokens.
        """
        self.fn = fn
        self.text = text
        # Init the position
        self.pos = Position(-1,0,-1,fn,text)
        # Current char to be processed by the Lexer.
        self.current_char = None
        # Advance to the first char of the input text.
        self.advance()

    def advance(self):
        """ ADVANCE
        @brief: Update self.current_char with the next char to be processed.
        
        @return: None
        """
        # Keep track of the position in the file
        self.pos.advance(self.current_char)
        # Update current_char
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        """ MAKE_TOKENS
        @brief: Process all the input text and make the corresponding tokens.
        
        @return: tokens Array with the tokens.
               : error  ExpectedCharError, IllegalCharError, or None
        """
        tokens = []

        # Process all the chars one by one
        while self.current_char != None:
            # Remove white space
            if self.current_char in ' \t':
                self.advance()

            elif self.current_char == '+':
                tokens.append(Token(TokenType.PLUS, pos_start=self.pos))
                self.advance()

        # Add end of file token.
        tokens.append(Token(TokenType.END_OF_FILE, pos_start=self.pos))
        return tokens, None



                
        

                
        
                
        

    
