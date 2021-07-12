from tokens import TokenType
from nodes import *

class Parser:
    """ PARSER

    The parser converts a Token list it into an Abstract Syntax Tree (AST). 
    """

    def __init__(self,tokens):
        """
        @brief: Constructor of Parser.
        
        @param: tokens Tokens list to be processed.
        """
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        """ ADVANCE
        @brief: Advance to the next token.
        
        @return: Token Current token.
        """
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok
    
    def reverse(self, amount=1):
        """ REVERSE
        @brief: Reverse to the previous token.

        @param: amount Amount to reverse back.
        
        @return: Token Previous token.
        """
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        """ UPDATE_CURRENT_TOK
        @brief: Update self.current_tok to the current one defined by self.tok_idx
        
        @return: None
        """
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        else:
            self.current_tok = None

    def parse(self,param):
        """ PARSE
        @brief: Parse self.tokens into an AST.
        
        @param: param
                
        @return: ParseResult Result of the parser (AST and error)
        """
        res = self.statements()

        if not res.error and self.current_tok.type != TokenType.END_OF_FILE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))

        return res
