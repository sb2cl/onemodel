from tokens import TokenType
from nodes import *
from errors import *

class ParseResult:
    """ PARSERESULT

    ParseResult handles the results and error of the parsing process.
    """
    def __init__(self):
        """ __INIT__
        @brief: Constructor of ParseResult.
        
        @return: ParseResult
        """
        # Keep track of error and node generated
        self.error = None 
        self.node = None

        self.last_registered_advance_count = 0
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        """ REGISTER_ADVANCEMENT
        @brief: Call this method before each time parse.advance() is called.
        
        @return: void
        """
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self,res):
        """ REGISTER
        @brief: TODO
        
        @param: res ParseResult to register.
                
        @return: res.node
        """
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count

        # If there is an error, save it.
        if res.error: self.error = res.error

        return res.node

    def try_register(self,res):
        """ TRY_REGISTER
        @brief: Register res if there is no error.
        
        @param: 
                
        @return: void
        """
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self,node):
        """ SUCCESS
        @brief: TODO
        
        @param: node
                
        @return: void
        """
        self.node = node
        return self

    def failure(self,error):
        """ FAILURE
        @brief: TODO
        
        @param: error
                
        @return: void
        """
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self

class Parser:
    """ PARSER

    The parser converts a Token list into an Abstract Syntax Tree (AST). 
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

    def parse(self):
        """ PARSE
        @brief: Parse self.tokens into an AST.
        
        @return: ParseResult Result of the parser (AST and error)
        """
        res = self.factor()

        if not res.error and self.current_tok.type != TokenType.END_OF_FILE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Token cannot appear after previous tokens"
            ))

        return res

    def factor(self):
        """ FACTOR
        @brief: Find a factor.
        
        @return: node
        """
        res = ParseResult()
        tok = self.current_tok

        if tok.type == TokenType.PLUS:
            res.register_advancement()
            self.advance()

            factor = res.register(self.factor())

            if res.error: return res
            return res.success(PlusNode(factor))

        elif tok.type == TokenType.MINUS:
            res.register_advancement()
            self.advance()

            factor = res.register(self.factor())

            if res.error: return res
            return res.success(MinusNode(factor))

        elif tok.type == TokenType.NUMBER:
            res.register_advancement()
            self.advance()

            return res.success(NumberNode(tok))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected number"
        ))
