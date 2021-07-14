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

class BinaryOperationNode:
    """ BINARYOPERATIONNODE

    Definition of a generic binary operation node.
    """
    def __init__(self,node_a,operation_token,node_b):
        """ __INIT__
        @brief: Constructor of BinaryOperationNode.
        
        @param: node_a          First operation node.
              : operation_token Operation token.
              : node_b          Second operation node.
                
        @return: BinaryOperationNode
        """
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

        def __repr__(self):
            return f'({self.node_a}, {self.operation_token}, {self.node_b})'

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
