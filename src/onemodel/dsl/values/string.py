from onemodel.dsl.values.value import Value

class String(Value):
    def __init__(self, value):
        """ Initialize string.
        
        Args:
            value: str
                String value.
        """
        super().__init__()
        self.value = value
                
    def add_value_to_model(self, name, model):
        # String are not added to SBML models.
        pass

    def __str__(self): 
        return f"'{self.value}'"

    def __repr__(self):
        return self.__str__()
