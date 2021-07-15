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


#@dataclass
#class AddNode:
#    node_a: any
#    node_b: any
#
#    def __repr__(self):
#        return f"({self.node_a}+{self.node_b})"
#
#@dataclass
#class SubtractNode:
#    node_a: any
#    node_b: any
#
#    def __repr__(self):
#        return f"({self.node_a}-{self.node_b})"
#
#@dataclass
#class MultiplyNode:
#    node_a: any
#    node_b: any
#
#    def __repr__(self):
#        return f"({self.node_a}*{self.node_b})"
#
#@dataclass
#class DivideNode:
#    node_a: any
#    node_b: any
#
#    def __repr__(self):
#        return f"({self.node_a}/{self.node_b})"
#
#@dataclass
#class PlusNode:
#    node: any
#
#    def __repr__(self):
#        return f"(+{self.node})"
#    
#@dataclass
#class MinusNode:
#    node: any
#
#    def __repr__(self):
#        return f"(-{self.node})"
