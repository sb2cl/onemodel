class Context:
    """ The evaluation context.
    """
    def __init__(self, parent=None):
        """ Initialize context.
        """
        # Parent context.
        self.parent = parent

        # Dictionary with local variables.
        self.locals = {}

        # Reference to the walker.
        self.walker = None

        # Namespace.
        self.namespace = ''

    def getRootContext(self):
        """ Return root context.
        """
        context = self

        while context.parent != None:
            context = context.parent

        return context

    def set(self, name, value):
        """ Set the value in self.locals as name.
        """
        # Add the definition context to the value.
        value.set_definition_context(self)

        # Save value in locals.
        self.locals[name] = value

    def get(self, name):
        """ Get a variable by its name.

        If the variable is not in self.locals, we will look for in the parent
        context.
        """
        # Find value in self.locals.
        value = self.locals.get(name, None)
    
        # If didn't find the value, and there is a parent context.
        if value == None and self.parent:
            # Look recursively in parent context for the value.
            return self.parent.get(name)
      
        # If value is not found.
        if value == None:
            # Raise an error.
            raise NameError(f"NameError: name '{name}' is not defined")
      
        return value

    def getLocal(self, name):
        """ Get a variable by its name, but only look for it in self.locals.
        """
        # Find value in self.locals.
        value = self.locals.get(name, None)

        return value

    def getFullName(self, name):
        # TODO: Hacer esto.
        pass
