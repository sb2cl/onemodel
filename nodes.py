from dataclasses import dataclass
from position import Position

@dataclass
class NumberNode:
    value: float

    pos_start: Position
    pos_end: Position

    def __repr__(self):
        return f"{self.value}"

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
