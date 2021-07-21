from onemodel.errors import *

from onemodel.tokens import TokenType
from onemodel.nodes import *

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
                
        @return: self
        """
        self.node = node
        return self

    def failure(self,error):
        """ FAILURE
        @brief: TODO
        
        @param: error
                
        @return: self
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
        self.update_current_token()
        return self.current_token
    
    def reverse(self, amount=1):
        """ REVERSE
        @brief: Reverse to the previous token.

        @param: amount Amount to reverse back.
        
        @return: Token Previous token.
        """
        self.tok_idx -= 1
        self.update_current_token()
        return self.current_token

    def update_current_token(self):
        """ UPDATE_CURRENT_TOKEN
        @brief: Update self.current_token to the current one defined by self.tok_idx
        
        @return: None
        """
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]

    def parse(self):
        """ PARSE
        @brief: Parse self.tokens into an AST.
        
        @return: ParseResult Result of the parser (AST and error)
        """
        res = self.statements()

        if not res.error and self.current_token.type != TokenType.END_OF_FILE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Token cannot appear after previous tokens"
            ))

        return res

    def statements(self):
        """ STATEMENTS
        @brief: Find statements.
        
        @return: ParseResult
        """
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()

        while self.current_token.type == TokenType.NEW_LINE:
            res.register_advancement()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True

        while True:
            newline_count = 0
            while self.current_token.type == TokenType.NEW_LINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_token.pos_end.copy()
            ))

    def statement(self):
        """ STATEMENT
        @brief: Find statement.
        
        @return: ParseResult
        """
        res = ParseResult()
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.matches(TokenType.KEYWORD, 'RETURN'):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_token.pos_start.copy()))

        if self.current_token.matches(TokenType.KEYWORD, 'CONTINUE'):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_token.pos_start.copy()))

        if self.current_token.matches(TokenType.KEYWORD, 'BREAK'):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_token.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(expr)
        
    def expr(self):
        """ EXPR
        @brief: Find a expr.
        
        @return: ParseResult
        """
        res = ParseResult()

        if self.current_token.matches(TokenType.KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_token.type != TokenType.IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected identifier"
                ))

            var_name = self.current_token
            res.register_advancement()
            self.advance()

            if self.current_token.type != TokenType.EQUAL:
                return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.binary_operation(
            self.comp_expr,
            ((TokenType.KEYWORD, 'AND'), (TokenType.KEYWORD, 'OR'))
            ))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(node)

    def comp_expr(self):
        """ COMP_EXPR
        @brief: Find a comparison expression.
        
        @return: ParseResult
        """
        res = ParseResult()

        if self.current_token.matches(TokenType.KEYWORD, 'NOT'):
            op_tok = self.current_token
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOperationNode(op_tok, node))

        node = res.register(self.binary_operation(
            self.arith_expr,
            (
                TokenType.IS_EQUAL,
                TokenType.NOT_EQUAL,
                TokenType.LESS_THAN,
                TokenType.GREATER_THAN,
                TokenType.LESS_EQUAL_THAN,
                TokenType.GREATER_EQUAL_THAN
                )
            ))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                "Expected int, float, identifier, '+', '-', '(', '[', 'IF', 'FOR', 'WHILE', 'FUN' or 'NOT'"
                ))

        return res.success(node)

    def arith_expr(self):
        """ ARITH_EXPR
        @brief: Find arithmetic expression.
        
        @return: ParseResult
        """
        return self.binary_operation(
                self.term, 
                (
                    TokenType.PLUS, 
                    TokenType.MINUS
                )
            )

    def term(self):
        """ TERM
        @brief: Find a term.
        
        @return: ParseResult
        """
        return self.binary_operation(
                self.factor, 
                (
                    TokenType.MULTIPLICATION, 
                    TokenType.DIVISION
                )
            )

    def factor(self):
        """ FACTOR
        @brief: Find a factor.
        
        @return: ParseResult
        """
        res = ParseResult()
        token = self.current_token
        
        if token.type in (TokenType.PLUS, TokenType.MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOperationNode(token, factor))

        return self.power()

    def power(self):
        """ POWER
        @brief: Find a power expression.
        
        @return: ParseResult
        """
        return self.binary_operation(
                self.call, 
                (TokenType.POWER, ), 
                self.factor
                )

    def call(self):
        """ CALL
        @brief: Find a call expression.
        
        @return: ParseResult
        """
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res

        if self.current_token.type == TokenType.LEFT_PAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []

            if self.current_token.type == TokenType.RIGHT_PAREN:
                res.register_advancement()
                self.advance()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(' or 'NOT'"
                    ))

                while self.current_token.type == TokenType.COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res

                if self.current_token.type != TokenType.RIGHT_PAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)

    def atom(self):
        """ ATOM
        @brief: Find an atom expression.
        
        @return: ParseResult
        """
        res = ParseResult()
        tok = self.current_token

        if tok.type == TokenType.NUMBER:
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TokenType.STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TokenType.IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TokenType.LEFT_PAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if self.current_token.type != TokenType.RIGHT_PAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ')'"
                ))
            res.register_advancement()
            self.advance()
            if res.error: return res
            return res.success(expr)

        elif tok.type == TokenType.LEFT_SQUARE:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)

        elif tok.matches(TokenType.KEYWORD, "IF"):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TokenType.KEYWORD, "FOR"):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TokenType.KEYWORD, "WHILE"):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TokenType.KEYWORD, "FUN"):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', IF', 'FOR', 'WHILE', 'FUN'"
        ))

    def list_expr(self):
        """ LIST_EXPR
        @brief: Find a list expression.
        
        @return: ParseResult
        """
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()

        if self.current_token.type != TokenType.LEFT_SQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '['"
                ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.RIGHT_SQUARE:
            res.register_advancement()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUN', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
                    ))

            while self.current_token.type == TokenType.COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_token.type != TokenType.RIGHT_SQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected ',' or ']'"
                    ))

            res.register_advancement()
            self.advance()
        
        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.current_token.pos_end.copy()
            ))

    def if_expr(self):
        """ IF_EXPR
        @brief: Find a if expression.
        
        @return: ParseResult
        """
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('IF'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))
    
    def if_expr_b(self):
        return self.if_expr_cases('ELIF')
    
    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_token.matches(TokenType.KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            if self.current_token.type == TokenType.NEW_LINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_token.matches(TokenType.NEW_LINE, 'END'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                            self.current_token.pos_start, self.current_token.pos_end,
                            "Expected 'END'"
                            ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)

    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_token.matches(TokenType.KEYWORD, 'ELIF'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
    
        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        """ IF_EXPR_CASES
        @brief: Generic if_expr searcher
        
        @param: case_keyword Keyword to look for.
                
        @return: ParseResult
        """
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_token.matches(TokenType.KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '{case_keyword}'"
                ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(TokenType.KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.NEW_LINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_token.matches(TokenType.KEYWORD, 'END'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))

    def for_expr(self,):
        """ FOR_EXPR
        @brief: Find a for expression.
        
        @return: ParseResult
        """
        res = ParseResult()

        if not self.current_token.matches(TokenType.KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected identifier"
            ))

        var_name = self.current_token
        res.register_advancement()
        self.advance()

        if self.current_token.type != TokenType.EQUAL:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '='"
            ))
        
        res.register_advancement()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(TokenType.KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'TO'"
            ))
        
        res.register_advancement()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res

        if self.current_token.matches(TokenType.KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_token.matches(TokenType.KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.NEW_LINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(TokenType.KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'END'"
                    ))

            res.register_advancement()
            self.advance()
    
            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))

    def while_expr(self):
        res = ParseResult()

        if not self.current_token.matches(TokenType.KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_token.matches(TokenType.KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.NEW_LINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_token.matches(TokenType.KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected 'END'"
                    ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))
    
        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))
    
    def func_def(self):
        res = ParseResult()

        if not self.current_token.matches(TokenType.KEYWORD, 'FUN'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'FUN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.IDENTIFIER:
            var_name_tok = self.current_token
            res.register_advancement()
            self.advance()
            if self.current_token.type != TokenType.LEFT_PAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected '('"
                ))
        else:
            var_name_tok = None
            if self.current_token.type != TokenType.LEFT_PAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected identifier or '('"
                ))
        
        res.register_advancement()
        self.advance()
        arg_name_toks = []

        if self.current_token.type == TokenType.IDENTIFIER:
            arg_name_toks.append(self.current_token)
            res.register_advancement()
            self.advance()
            
            while self.current_token.type == TokenType.COMMA:
                res.register_advancement()
                self.advance()

                if self.current_token.type != TokenType.IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_token.pos_start, self.current_token.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_token)
                res.register_advancement()
                self.advance()
            
            if self.current_token.type != TokenType.RIGHT_PAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_token.type != TokenType.RIGHT_PAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_token.pos_start, self.current_token.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_token.type == TokenType.ARROW:
            res.register_advancement()
            self.advance()
            node_to_return = res.register(self.expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                node_to_return,
                True
            ))

        if self.current_token.type != TokenType.NEW_LINE:
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected '->' or NEWLINE"
                ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_token.matches(TokenType.KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_token.pos_start, self.current_token.pos_end,
                f"Expected 'END'"
                ))

        res.register_advancement()
        self.advance()
    
        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
            ))

    def binary_operation(self, func_a, ops, func_b = None):
        """ BINARY_OPERATION
        @brief: Generic operation with two elements.
        
        @param: func_a First parser function to look for the first element.
              : ops    Operaton token.
              : func_b Second parser function to look for the second element.
                
        @return: ParseResult
        """
        # If func_b is not passed.
        if func_b == None:
            # Use func_a as func_b.
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            operation_token = self.current_token

            res.register_advancement()
            self.advance()

            right = res.register(func_b())

            if res.error: return res
            left = BinaryOperationNode(left, operation_token, right)

        return res.success(left)

if __name__ == '__main__':
    from onemodel.lexer import Lexer
    from onemodel.utils.setup_input_history import setup_input_history

    setup_input_history()

    while True:
        text = input('parser > ')
        if text.strip() == "": continue

        # Generate tokens
        lexer = Lexer('<stdin>', text)
        tokens, error = lexer.generate_tokens()

        # Generate AST
        parser = Parser(tokens)
        ast = parser.parse()

        if ast.error:
            print(ast.error.as_string())
        elif ast.node:
            print(ast.node.element_nodes)
