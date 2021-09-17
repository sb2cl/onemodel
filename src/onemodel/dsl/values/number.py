from onemodel.dsl.values.value import Value

class Number(Value):
    def __init__(self, value):
        """ Initialize number.
        
        Args:
            value: int or float
                Value to set number.
        """
        super().__init__()
        self.value = value
                
    def __str__(self): 
        return f'{self.value}'

    def __repr__(self):
        return self.__str__()
