from onemodel.dsl.values.value import Value

class PythonValue(Value):
    """ PythonValue holds the value of a regular python object.
    """
    def __init__(self, value):
        """ Initialize PythonValue
        """
        self.value = value
    
    def __str__(self):
        return str(self.value)
        
    def __repr__(self):
        return repr(self.value)
