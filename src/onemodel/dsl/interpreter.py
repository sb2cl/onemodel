from onemodel.dsl.errors import *
from onemodel.dsl.values import *

from onemodel.dsl.nodes import *
from onemodel.dsl.tokens import TokenType
from onemodel.dsl.values import *
from onemodel.dsl.lexer import Lexer
from onemodel.dsl.parser_ import Parser
from onemodel.dsl.runTimeResult import RunTimeResult

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

    def visit_StringNode(self,node,context):
        """ VISIT_STRINGNODE
        @brief: Vist a StrinNode
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: RunTimeResult
        """
        return RunTimeResult().success(
                String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end)
                )
    def visit_ListNode(self,node,context):
        """ VISIT_LISTNODE
        @brief: Visit a ListNode.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: RunTimeResult
        """
        res = RunTimeResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): return res

        return res.success(
                List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
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

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Number.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            expr_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Number.null if should_return_null else expr_value)

        return res.success(Number.null)

    def visit_ForNode(self, node, context):
        res = RunTimeResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
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

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
                Number.null if node.should_return_null else
                List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
                )

    def visit_WhileNode(self, node, context):
        res = RunTimeResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res

            if not condition.is_true(): break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res

            if res.loop_should_continue:
                continue

            if res.loop_should_break:
                break

            elements.append(value)

        return res.success(
                Number.null if node.should_return_null else
                List(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
                )

    def visit_FuncDefNode(self, node, context):
        res = RunTimeResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_toks]
        func_value = Function(func_name, body_node, arg_names, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)
        
        if node.var_name_tok:
            context.symbol_table.set(func_name, func_value)

        return res.success(func_value)

    def visit_CallNode(self, node, context):
        res = RunTimeResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)

        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start,node.pos_end).set_context(context)
        return res.success(return_value)

    def visit_ReturnNode(self, node, context):
        res = RunTimeResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Number.null
    
        return res.success_return(value)

    def visit_ContinueNode(self, node, context):
        return RunTimeResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RunTimeResult().success_break()
