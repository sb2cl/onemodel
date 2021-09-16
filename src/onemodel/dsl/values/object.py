from onemodel.dsl.values.value import Value

class Object(Value):
    """ OneModel Object.
    """
    def __init__(self, context):
        """ Initialize Object.
        """
        super().__init__()

        # In this context are the values associated of this object.
        self.context = context

    def add_value_to_model(self, name, model):
        """ Add this value to the SBML model.

        Arguments:
            name: str
                Name of this value.
            model: LibSBML model
                Model to include this value.
        """
        for symbol in self.context.symbol_table.symbols:
            value = self.context.symbol_table.get(symbol)
            value.namespace = f'{name}__'
            value.add_value_to_model(symbol, model)

    def __str__(self):
        return f"<object>"

    def __repr__(self):
        return self.__str__()
