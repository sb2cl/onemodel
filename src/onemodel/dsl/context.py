class Context:
    """ The evaluation context.
    """
    def __init__(self, name=None, parent=None):
        """ Initialize context.
        """
        # Context name.
        self.name = name

        # Parent context.
        self.parent = parent

        # Dictionary with local symbols.
        self.symbols = {}

    def getRootContext(self):
        """ Return root context.
        """
        context = self

        while context.parent != None:
            context = context.parent

        return context

    def set(self, name, symbol):
        """ Set a symbol in self.symbols.
        """
        # Save value in symbols.
        self.symbols[name] = symbol

    def get(self, name):
        """ Get a variable by its name.

        If the variable is not in self.symbols, we will look for in the parent
        context.
        """
        # Find value in self.symbols.
        value = self.symbols.get(name, None)
    
        # If didn't find the value, and there is a parent context.
        if value == None and self.parent:
            # Look recursively in parent context for the value.
            return self.parent.get(name)
      
        # If value is not found.
        if value == None:
            # Raise an error.
            raise NameError(f"NameError: name '{name}' is not defined")
      
        return value
