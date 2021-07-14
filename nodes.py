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

@dataclass
class AddNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}+{self.node_b})"

@dataclass
class SubtractNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}-{self.node_b})"

@dataclass
class MultiplyNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}*{self.node_b})"

@dataclass
class DivideNode:
    node_a: any
    node_b: any

    def __repr__(self):
        return f"({self.node_a}/{self.node_b})"

@dataclass
class PlusNode:
    node: any

    def __repr__(self):
        return f"(+{self.node})"
    
@dataclass
class MinusNode:
    node: any

    def __repr__(self):
        return f"(-{self.node})"
