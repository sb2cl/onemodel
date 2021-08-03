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
    
    def set(self, symbol):
        """ Set a symbol in the symbol_table.
        
        Set a new symbol in the symbol_table. It the name of that symbol was
        already been used, it will overwrite the old symbol with the new one.
        
        Args:
            symbol:
                New symbol to add into the symbol_table.
                
        Returns:
            None
        """
        self.symbol_table[symbol.name] = symbol
