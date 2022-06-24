class Value:
    """ Define the base Value object.
    """
    def __init__(self):
        """ Initialize Value.
        """
        # The name used to store this value in a context.
        self.symbol_name = ''

        # The context where the value was defined (and also where it is saved
        # as a symbol).
        self.definition_context = None

    def set_context(self, name, context):
        self.symbol_name = name
        self.definition_context = context

    def getFullname(self):
        fullname = self.definition_context.getFullname(self.symbol_name)
        return fullname

    def add_value_to_model(self, name, model):
        """ Add this value to a SBML model.
        """
        raise Exception(
            f'Class "{type(self).__name__}" has not defined add_value_to_model method.'
        )

    def set(self, name, value):
        raise Exception(
            f'Class "{type(self).__name__}" has no attributes.'
        )

    def get(self, name):
        raise Exception(
            f'Class "{type(self).__name__}" has no attributes.'
        )

    def __str__(self):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __str__ method.'
        )

    def __repr__(self):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __repr__ method.'
        )

    def __call__(self, *args):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __call__ method.'
        )

    def __add__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __add__ method.'
        )

    def __radd__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __radd__ method.'
        )

    def __sub__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __sub__ method.'
        )

    def __rsub__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __rsub__ method.'
        )

    def __mul__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __mul__ method.'
        )

    def __rmul__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __rmul__ method.'
        )

    def __truediv__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __truediv__ method.'
        )

    def __rtruediv__(self, other):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined __rtruediv__ method.'
        )
