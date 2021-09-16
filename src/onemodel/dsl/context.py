class Context:
    """ Context for executing functions and keep track of symbol tables.
    """
    def __init__(self, display_name, parent=None):
        """ Initialize context.
        """
        self.display_name = display_name
        self.parent = parent
        self.symbol_table = None
        self.walker = None

    def getMainParent(self):
        context = self

        while context.parent != None:
            context = context.parent

        return context

    def set(self, name, value):
        value.set_definition_context(self)

        self.symbol_table.set(name, value)

    def get(self, name):
        value = self.symbol_table.get(name)

        return value

    def getValueFullName(self, name):
        # TODO: Hacer esto.
        pass
