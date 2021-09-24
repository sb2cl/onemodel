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

    def set(self, name, symbol, isFirstDefinition=True):
        """ Set a symbol in self.symbols.
        """
        # If is is the first definiton of this symbol.
        if isFirstDefinition:
            # Set self as it context, and pass it its name.
            symbol.set_context(name, self)

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

    def getFullname(self, name):
        """ Get the fullname of symbol by its local name.
        """
        ## Check if name contains '__'.
        idx = name.find('__')
        if idx > 0:
            # Then the name has the following form: parentname__namelocal
            nameparent = name[:idx]
            namelocal = name[idx+2:]

            parent = self.symbols.get(nameparent, None)
            return parent.getFullname(namelocal)

        # Try to find the symbols in self.symbols
        value = self.symbols.get(name, None)

        # If we found the symbol here.
        if value != None:
            fullname = name
            context = self
            while context.parent != None:
                if context.symbol_name != '':
                    fullname = context.symbol_name + '__' + fullname
                context = context.parent

        elif self.parent:
            return self.parent.getFullname(name)

        else:
            # Raise an error.
            raise NameError(f"NameError: name '{name}' is not defined")

        return fullname

    def print(self):
        print(f'### Context ###')
        print(f'name: {self.name}')
        if self.parent:
            print(f'parent: {self.parent.name}')
        else:
            print(f'parent: None')
        print('symbols:')
        for symbol in self.symbols:
            print('\t' + symbol)

        print(f'### End Context ###')
        print()
        
    def add_value_to_model(self, name, model):
        for symbol in self.symbols:
            value = self.get(symbol)
            fullname = self.getFullname(symbol)
            value.add_value_to_model(
                fullname, 
                model
            )
