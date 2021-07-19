from dataclasses import dataclass
from position import Position

class NumberNode:
    """ NUMBERNODE

    Definition of NumberNode.
    """

    def __init__(self,token):
        """ __INIT__
        @brief: Constructor of NumberNode.
        
        @param: token Number token.
                
        @return: NumberNode.
        """
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        """ __REPR__
        @brief: Representaion method.
                
        @return: str 
        """
        return f"{self.token.value}"

    def __eq__(self,other):
        """ __EQ__
        @brief: Override equality operator to only take into account type and value.
        
        @param: other Token
                
        @return: True if they are equal.
        """
        if other == None: 
            return False

        return self.token == other.token

class StringNode:
    """ STRINGNODE

    Definition of StringNode.
    """

    def __init__(self,token):
        """ __INIT__
        @brief: Constructor of StringNode.
        
        @param: token Number token.
                
        @return: NumberNode.
        """
        self.token = token
        self.pos_start = self.token.pos_start
        self.pos_end = self.token.pos_end

    def __repr__(self):
        """ __REPR__
        @brief: Representaion method.
                
        @return: str 
        """
        return f"{self.token.value}"

class ListNode:
    """ LISTNODE

    Definition of ListNode.
    """
    def __init__(self, element_nodes, pos_start, pos_end):
        """ __INIT__
        @brief: Constructor of ListNode.
        
        @param: element_nodes Nodes in the list.
                
        @return: ListNode
        """
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end
    
class VarAccessNode:
    """ VARACCESSNODE

    Access the value of a variable.
    """
    def __init__(self,var_name_tok):
        """ __INIT__
        @brief: Constructor of VarAccessNode
        
        @param: var_name_tok Name of the variable to access.
                
        @return: VarAccessNode
        """
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarAssignNode:
    """ VARASSIGNNODE

    Assign the value of a variable.
    """
    def __init__(self,var_name_tok,value_node):
        """ __INIT__
        @brief: Constructor of VarAssignNode.
        
        @param: var_name_tok Name of the varible.
              : value_node   Value to assign.
                
        @return: VarAssignNode
        """
        self.var_name_tok = var_name_tok
        self.value_node = value_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class BinaryOperationNode:
    """ BINARYOPERATIONNODE

    Definition of a generic binary operation node.
    """
    def __init__(self,left_node,operation_token,right_node):
        """ __INIT__
        @brief: Constructor of BinaryOperationNode.
        
        @param: node_a          First operation node.
              : operation_token Operation token.
              : node_b          Second operation node.
                
        @return: BinaryOperationNode
        """
        self.left_node = left_node
        self.operation_token = operation_token
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.operation_token}, {self.right_node})'

    def __eq__(self,other):
        """ __EQ__
        @brief: Override equality operator to only take into account type and value.
        
        @param: other Token
                
        @return: True if they are equal.
        """
        if other == None: 
            return False

        return self.left_node == self.left_node and self.operation_token == other.operation_token and self.right_node == other.right_node

class UnaryOperationNode:
    """ UNARYOPERATIONNODE

    Definition of a generic unary operation node.
    """
    def __init__(self,operation_token,node):
        """ __INIT__
        @brief: Constructor of UnaryOperationNode.
        
        @param: operation_token 
              : node
                
        @return: UnaryOperationNode
        """
        self.operation_token = operation_token
        self.node = node

        self.pos_start = self.operation_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.operation_token}, {self.node})'

    def __eq__(self,other):
        """ __EQ__
        @brief: Override equality operator to only take into account type and value.
        
        @param: other Token
                
        @return: True if they are equal.
        """
        if other == None: 
            return False

        return self.operation_token == other.operation_token and self.node == other.node

class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1])[0].pos_end

class ForNode:
    def __init__(self,var_name_tok,start_value_node,end_value_node,step_value_node,body_node,should_return_null):
        """ __INIT__
        @brief: Constructor of ForNode.
        
        @param: var_name_tok        Variable used to count the loops.
              : start_value_node    Start value for the loop.
              : end_value_node      End value for the loop.
              : step_value_node     Step for increasing the variable.
              : body_node           Commands to execute.
              : should_return_null  Should the node return null?
                
        @return: ForNode
        """
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null
                
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

class WhileNode:
    def __init__(self,condition_node,body_node,should_return_null):
        """ __INIT__
        @brief: Constructor of WhileNode.
        
        @param: condition_node      Condition for the while loop.
              : body_node           Commands to execute.
              : should_return_null  Should the node return null?
                
        @return: WhileNode
        """
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

class FuncDefNode:
    def __init__(self,var_name_tok,arg_name_toks,body_node,should_return_null):
        """ __INIT__
        @brief: Constructor of FuncDefNode.
        
        @param: var_name_tok        Name of the function.
              : arg_name_toks       Arguments of the function.
              : body_node           Commands to execute.
              : should_return_null  Should the node return null?
                
        @return: FuncDefNode
        """
        self.var_name_tok = var_name_tok
        self.arg_name_toks = arg_name_toks
        self.body_node = body_node
        self.should_return_null = should_return_null

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_name_toks) > 0:
            self.pos_start = self.arg_name_toks[0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self,node_to_call,arg_nodes):
        """ __INIT__
        @brief: Constructor of CallNode.
        
        @param: node_to_call Node to be called.
              : arg_nodes    Arguments for calling the node.
                
        @return: CallNode
        """
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes)-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
