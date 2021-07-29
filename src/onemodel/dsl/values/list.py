from onemodel.dsl.values.value import Value
from onemodel.dsl.errors import *
from onemodel.dsl.values.number import Number

class List(Value):
    """ LIST(VALUE)

    Definition of List
    """
    def __init__(self, elements):
        """ __INIT__
        @brief: Constructor of List
        
        @param: elements Elements in the list, can be any type.
                
        @return: List
        """
        super().__init__()
        self.elements = elements

    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None

    def subbed_by(self, other):
        if isinstance(other, Number):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RunTimeError(
                        other.pos_start, other.pos_end,
                        'Element at this index could not be removed from list because index is out of bounds',
                        self.context
                        )
            else:
                return None, Value.illegal_operation(self, other)

    def multed_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)

    def dived_by(self, other):
        if isinstance(other, Number):
            try:
                return self.elements[int(other.value)], None
            except:
                return None, RunTimeError(
                        other.pos_start, other.pos_end,
                        'Element at this index could not be retrieved from list because index is out of bounds',
                        self.context
                        )
        else:
            return None, Value.illegal_operation(self, other)
  
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __str__(self):
        return f'{", ".join([str(x) for x in self.elements])}'

    def __repr__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'
