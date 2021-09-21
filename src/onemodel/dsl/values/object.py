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

    def add_value_to_model(self, name, model):
        # Call only set from Context, and not from Value.
        Context.add_value_to_model(self, name, model)
                
    def set(self, name, value):
        # Call only set from Context, and not from Value.
        Context.set(self, name, value)

    def get(self, name):
        # Call only get from Context, and not from Value.
        return Context.get(self, name)

    def __str__(self): 
        string = f'{repr(self)} with attributes:\n'

        for symbol in self.symbols:
            value = self.get(symbol)
            string += '  %+10s: %s\n' % (symbol, repr(value))

        return string

    def __repr__(self):
        return f'<object {self.name}>'
