from nodes import *
from errors import RunTimeError
from tokens import TokenType
from values import *
from lexer import Lexer
from parser_ import Parser
from runTimeResult import RunTimeResult

import math

class Context:
    """ CONTEXT

    This class keep track of the context where the node is executed (symbol table, context name, ect.)
    """

    def __init__(self,display_name,parent=None,parent_entry_pos=None):
        """ __INIT__
        @brief: Constructo of Context.
        
        @param: display_name     Name of this context.
              : parent           Parent context of this context.
              : parent_entry_pos Position of the parent context.
                
        @return: Context
        """
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class SymbolTable:
    """ SYMBOLTABLE

    SymbolTable keeps track of the worspace variables and functions.
    """
    def __init__(self,parent=None):
        """ __INIT__
        @brief: Constructor of SymbolTable.
        
        @param: parent  Parent SymbolTable.
                
        @return: SymbolTable
        """
        # Dictionary where all symbols are saved by name.
        self.symbols = {}
        self.parent = parent

    def get(self,name):
        """ GET
        @brief: Return symbol value by name.
        
        @param: name Symbol name.
                
        @return: value Symbol value.
        """
        # Find the symbol in this SymbolTable.
        value = self.symbols.get(name, None)

        # If the symbol is not found.
        if value == None and self.parent:

            # Look for it in parent SymbolTable (this is recursive).
            return self.parent.get(name)

        return value

    def set(self,name,value):
        """ SET
        @brief: Set the value of a symbol in current SymbolTable.
        
        @param: name  Symbol name.
              : value Symbol value.
                
        @return: None
        """
        self.symbols[name] = value

    def remove(self,name):
        """ REMOVE
        @brief: Remove symbol from current SymbolTable.
        
        @param: name Symbol name.
                
        @return: None
        """
        del self.symbols[name]
                
class Interpreter:
    """ INTERPRETER

    The interpreter visits each node of the AST and execute it.
    """
    
    def __init__(self):
        """ __INIT__
        @brief: Constructor of Interpreter
        
        @return: Interpreter
        """
        pass

    def visit(self,node,context):
        """ VISIT
        @brief: Visit a node and execute it taking into account the context.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
        
    def no_visit_method(self,node,context):
        """ NO_VISIT_METHOD
        @brief: This method call when the corresponding visit_ method is not defined
        
        @param: node
              : context
                
        @return: None
        """
        raise Exception(f'No visit_{type(node).__name__} method defined')


    def visit_NumberNode(self,node,context):
        """ VISIT_NUMBERNODE
        @brief: Vist a number node.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """

        return RunTimeResult().success(
            Number(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_VarAccessNode(self,node,context):
        """ VISIT_VARACCESSNODE
        @brief: Visit a VarAccessNode.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)

    def visit_VarAssignNode(self,node,context):
        """ VISIT_VARASSIGNNODE
        @brief: Visit a VarAssignNode.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        res = RunTimeResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinaryOperationNode(self, node, context):
        res = RunTimeResult()

        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res

        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.operation_token.type == TokenType.PLUS:
            result, error = left.added_to(right)

        elif node.operation_token.type == TokenType.MINUS:
            result, error = left.subbed_by(right)

        elif node.operation_token.type == TokenType.MULTIPLICATION:
            result, error = left.multed_by(right)

        elif node.operation_token.type == TokenType.DIVISION:
            result, error = left.dived_by(right)

        elif node.operation_token.type == TokenType.POWER:
            result, error = left.powed_by(right)

        elif node.operation_token.type == TokenType.IS_EQUAL:
            result, error = left.get_comparison_eq(right)

        elif node.operation_token.type == TokenType.NOT_EQUAL:
            result, error = left.get_comparison_ne(right)

        elif node.operation_token.type == TokenType.LESS_THAN:
            result, error = left.get_comparison_lt(right)

        elif node.operation_token.type == TokenType.GREATER_THAN:
            result, error = left.get_comparison_gt(right)

        elif node.operation_token.type == TokenType.LESS_EQUAL_THAN:
            result, error = left.get_comparison_lte(right)

        elif node.operation_token.type == TokenType.GREATER_EQUAL_THAN:
            result, error = left.get_comparison_gte(right)

        elif node.operation_token.matches(TokenType.KEYWORD, 'AND'):
            result, error = left.anded_by(right)

        elif node.operation_token.matches(TokenType.KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOperationNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        error = None

        if node.operation_token.type == TokenType.MINUS:
            number, error = number.multed_by(Number(-1))
        elif node.operation_token.matches(TokenType.KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))

    def visit_IfNode(self, node, context):
        res = RunTimeResult()

        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RunTimeResult()

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Number(1)

        i = start_value.value

        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value

        while condition():
            context.symbol_table.set(node.var_name_tok.value, Number(i))
            i += step_value.value

            res.register(self.visit(node.body_node, context))
            if res.error: return res

        return res.success(None)

    def visit_WhileNode(self, node, context):
        res = RunTimeResult()

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res

            if not condition.is_true(): break

            res.register(self.visit(node.body_node, context))
            if res.error: return res

        return res.success(None)

    def visit_FuncDefNode(self, node, context):
        res = RunTimeResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RunTimeResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res

        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return res.success(return_value)

global_symbol_table = SymbolTable()
global_symbol_table.set("NULL", Number.null)
global_symbol_table.set("FALSE", Number.false)
global_symbol_table.set("TRUE", Number.true)
global_symbol_table.set("MATH_PI", Number.math_PI)

class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def added_to(self, other):
        return None, self.illegal_operation(other)

    def subbed_by(self, other):
        return None, self.illegal_operation(other)

    def multed_by(self, other):
        return None, self.illegal_operation(other)

    def dived_by(self, other):
        return None, self.illegal_operation(other)

    def powed_by(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)

    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)

    def anded_by(self, other):
        return None, self.illegal_operation(other)

    def ored_by(self, other):
        return None, self.illegal_operation(other)

    def notted(self):
        return None, self.illegal_operation()

    def execute(self, args):
        return RTResult().failure(self.illegal_operation())

    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if not other: other = self
        return RunTimeError(
                self.pos_start, other.pos_end,
                'Illegal operation',
                self.context
                )

class Number(Value):

    def __init__(self, value):
        super().__init__()
        self.value = float(value)

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RunTimeError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                    )

            return Number(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def get_comparison_eq(self, other):
        if isinstance(other, Number):
            return Number(self.value == other.value).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other, Number):
            return Number(self.value != other.value).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other, Number):
            return Number(self.value < other.value).set_context(self.context), None

    def get_comparison_gt(self, other):
        if isinstance(other, Number):
            return Number(self.value > other.value).set_context(self.context), None

    def get_comparison_lte(self, other):
        if isinstance(other, Number):
            return Number(self.value <= other.value).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other, Number):
            return Number(self.value >= other.value).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Number):
            return Number(self.value and other.value).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Number):
            return Number(self.value or other.value).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __repr__(self):
        return f"{self.value}"

Number.null    = Number(0)
Number.false   = Number(0)
Number.true    = Number(1)
Number.math_PI = Number(math.pi)

class Function(Value):
    def __init__(self, name, body_node, arg_names):
        super().__init__()
        self.name = name or "<anonymous>"
        self.body_node = body_node
        self.arg_names = arg_names

    def execute(self, args):
        res = RunTimeResult()
        interpreter = Interpreter()
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = SymbolTable(new_context.parent.symbol_table)

        if len(args) > len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(args) - len(self.arg_names)} too many args passed into '{self.name}'",
                self.context
            ))
        
        if len(args) < len(self.arg_names):
            return res.failure(RunTimeError(
                self.pos_start, self.pos_end,
                f"{len(self.arg_names) - len(args)} too few args passed into '{self.name}'",
                self.context
            ))

        for i in range(len(args)):
            arg_name = self.arg_names[i]
            arg_value = args[i]
            arg_value.set_context(new_context)
            new_context.symbol_table.set(arg_name, arg_value)

        value = res.register(interpreter.visit(self.body_node, new_context))
        if res.error: return res
        return res.success(value)

    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"



def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.generate_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
