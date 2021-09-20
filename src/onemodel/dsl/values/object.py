from onemodel.dsl.values.value import Value
from onemodel.dsl.context import Context

class Object(Context, Value):
    """ Definition of Object.
    """
    def __init__(self, name, parent_context):
        """ Initialize Object
        """
        Context.__init__(self, name, parent_context)
        Value.__init__(self)
                
    def set(self, name, value):
        # Call only set from Context, and not from Value.
        Context.set(self, name, value)

    def get(self, name):
        # Call only get from Context, and not from Value.
        return Context.get(self, name)

    def __str__(self): 
        #self.print()
        string = f'<object {self.name}>\n'
        string += f'{self.parent}\n'
        string += f'attributes: {self.symbols}\n'
        return string

    def __repr__(self):
        return self.__str__()
