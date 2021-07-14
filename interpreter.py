from nodes import *
from values import Number
from lexer import Lexer
from parser_ import Parser

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

class RTResult:
  def __init__(self):
    self.reset()

  def reset(self):
    self.value = None
    self.error = None
    self.func_return_value = None
    self.loop_should_continue = False
    self.loop_should_break = False

  def register(self, res):
    self.error = res.error
    self.func_return_value = res.func_return_value
    self.loop_should_continue = res.loop_should_continue
    self.loop_should_break = res.loop_should_break
    return res.value

  def success(self, value):
    self.reset()
    self.value = value
    return self

  def success_return(self, value):
    self.reset()
    self.func_return_value = value
    return self

  def success_continue(self):
    self.reset()
    self.loop_should_continue = True
    return self

  def success_break(self):
    self.reset()
    self.loop_should_break = True
    return self

  def failure(self, error):
    self.reset()
    self.error = error
    return self

  def should_return(self):
    # Note: this will allow you to continue and break outside the current function
    return (
      self.error or
      self.func_return_value or
      self.loop_should_continue or
      self.loop_should_break
    )


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
