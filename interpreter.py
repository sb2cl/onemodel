from nodes import *
from values import Number
from lexer import Lexer
from parser_ import Parser

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None

class SymbolTable:
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent

    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
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
        return Number(node.value)

    def visit_AddNode(self,node,context):
        """ VISIT_ADDNODE
        @brief: Vist an add node.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        return Number(self.visit(node.node_a,context).value + self.visit(node.node_b,context).value)

    def visit_SubtractNode(self,node,context):
        """ VISIT_SUBTRACTNODE
        @brief: Vist a subtract node.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        return Number(self.visit(node.node_a,context).value - self.visit(node.node_b,context).value)

    def visit_MultiplyNode(self,node,context):
        """ VISIT_MULTIPLYNODE
        @brief: Vist a multiply node.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        return Number(self.visit(node.node_a,context).value * self.visit(node.node_b,context).value)

    def visit_DivideNode(self,node,context):
        """ VISIT_DIVIDENODE
        @brief: Vist a divide node.
        
        @param: node    Node to visit.
              : context Context for executing the node.
                
        @return: value  Execution result.
        """
        try:
            return Number(self.visit(node.node_a,context).value / self.visit(node.node_b,context).value)
        except:
            raise Exception("Runtime math error")


global_symbol_table = SymbolTable()

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

    # TODO: return the error of the interpreter.
    return result, None
