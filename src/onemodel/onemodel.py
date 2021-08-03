from onemodel.symbol import SymbolType

class OneModel:
    """ ONEMODEL

    This class implements OneModel models.
    """

    def __init__(self):
        """ Inits OneModel.

        """
        self.symbol_table = {}

    def get(self, name):
        """ Get a symbol by name.
        
        Look for a symbol in the symbol_table by its name.
        
        Args:
            name: str
                Symbol name to return.
                
        Returns:
            Symbol
            None if the symbol does not exist.
        """
        # Find the symbol in the symbol_table.
        symbol = self.symbol_table.get(name, None)

        return symbol
    
    def add(self, symbol):
        """ Add a symbol in the symbol_table.
        
        Add a new symbol in the symbol_table. It the name of that symbol was
        already been used in the symbol_table, it will overwrite the old symbol with the new one.
        
        Args:
            symbol:
                New symbol to add into the symbol_table.
                
        Returns:
            None
        """
        self.symbol_table[symbol.name] = symbol

    def remove(self, name):
        """ Remove a symbol from the symbol_table.
        
        Remove a symbol by its name from the symbol_table.
        
        Args:
            name: str
                The name of the symbol to be removed.
        """
        del self.symbol_table[name]

    @property
    def parameters(self):
        """ Return a list with all the parameters of the model.
        
        Returns:
            A List with all the parameters.
        """
        params = []

        for name, symbol in self.symbol_table.items():
            if symbol.type == SymbolType.PARAMETER:
                params.append(symbol) 

        return params
    
    @property
    def parameters_name(self):
        """ Return a list with the names of all the parameters.
        
        Returns:
            List(str)
        """
        params_name = []
        params = self.parameters

        for param in params:
            params_name.append(param.name)

        return params_name

    @property
    def parameters_value(self):
        """ Return a list with the values of all the parameters.
        
        Returns:
            List(str)
        """
        params_value = []
        params = self.parameters

        for param in params:
            params_value.append(param.value)

        return params_value
