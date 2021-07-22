from onemodel.interpreter import SymbolTable
from onemodel.values.number import Number
from onemodel.values.function import BuiltInFunction
from onemodel.interpreter import Context
from onemodel.lexer import Lexer
from onemodel.parser_ import Parser
from onemodel.interpreter import Interpreter
from onemodel.utils.setup_input_history import setup_input_history

class Repl:
    """ REPL

    REPL implements the Read-Evaluate-Print-Loop for onemodel.
    """
    def __init__(self):
        """ __INIT__
        @brief: Init REPL
        
        @return: REPL
        """
        self.init_global_symbol_table()
    
    def init_global_symbol_table(self):
        """ INIT_GLOBAL_SYMBOL_TABLE
        @brief: Inits the symbol table
        
        @return: SymbolTable
        """
        self.global_symbol_table = SymbolTable()
        self.global_symbol_table.set("NULL", Number.null)
        self.global_symbol_table.set("FALSE", Number.false)
        self.global_symbol_table.set("TRUE", Number.true)
        self.global_symbol_table.set("MATH_PI", Number.math_PI)
        self.global_symbol_table.set("PRINT", BuiltInFunction.print)
        self.global_symbol_table.set("PRINT_RET", BuiltInFunction.print_ret)
        self.global_symbol_table.set("INPUT", BuiltInFunction.input)
        self.global_symbol_table.set("INPUT_INT", BuiltInFunction.input_int)
        self.global_symbol_table.set("CLEAR", BuiltInFunction.clear)
        self.global_symbol_table.set("CLS", BuiltInFunction.clear)
        self.global_symbol_table.set("IS_NUM", BuiltInFunction.is_number)
        self.global_symbol_table.set("IS_STR", BuiltInFunction.is_string)
        self.global_symbol_table.set("IS_LIST", BuiltInFunction.is_list)
        self.global_symbol_table.set("IS_FUN", BuiltInFunction.is_function)
        self.global_symbol_table.set("APPEND", BuiltInFunction.append)
        self.global_symbol_table.set("POP", BuiltInFunction.pop)
        self.global_symbol_table.set("EXTEND", BuiltInFunction.extend)
        self.global_symbol_table.set("LEN", BuiltInFunction.len)
        self.global_symbol_table.set("RUN", BuiltInFunction.run)

    def run(self):
        """ RUN
        @brief: Run the REPL 

        @return: result Result value. 
        """

        setup_input_history()
        continue_loop = True

        while continue_loop:
            # 1. READ

            text = input('onemodel > ')
            if text.strip() == "": continue

            # 2. EVALUATE

            # Generate tokens
            lexer = Lexer('<stdin>', text)
            tokens, error = lexer.generate_tokens()
            if error: return None, error

            # Generate AST
            parser = Parser(tokens)
            ast = parser.parse()
            if ast.error: return None, ast.error

            # Run program
            interpreter = Interpreter()
            context = Context('<program>')
            context.symbol_table = self.global_symbol_table
            result = interpreter.visit(ast.node, context)

            # 3. PRINT

            if result.error:
                print(result.error.as_string())
            elif result.value:
                if len(result.value.elements) == 1:
                    print(repr(result.value.elements[0]))
                else:
                    print(repr(result.value))

            # 4. LOOP
            continue_loop = True
