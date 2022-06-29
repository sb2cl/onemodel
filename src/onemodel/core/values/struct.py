from onemodel.core.context import Context
from onemodel.core.values.value import Value


class Struct(Context, Value):
    """Definition of Struct."""

    def __init__(self):
        """Initialize Struct"""
        Context.__init__(self)
        Value.__init__(self)

    def set(self, name, value):
        # Call only set from Context, and not from Value.
        Context.set(self, name, value)

    def get(self, name):
        # Call only get from Context, and not from Value.
        return Context.get(self, name)

    def __str__(self):
        string = f"<struct>\n"
        string += f"fields:\n"
        for symbol in self.symbols:
            value = self.get(symbol)
            string += f"\t{symbol}: {value}\n"
        return string

    def __repr__(self):
        return self.__str__()
