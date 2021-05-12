from ModelPart import ModelPart

class Symbol(ModelPart):
    """ SYMBOL(MODELPART)

    This class is the base for the implementation of Parameters and Variables.
    """

    def __init__(self,om,name):
        """
        @brief: Constructor of Symbol.
        
        @param: om   OneModel object.
                name String Name for the Symbol.
        """

        # Call parent constructor.
        ModelPart.__init__(self,om,name)

    @property
    def nameTex(self):
        """
        @brief: Name used for LaTeX generation.
        """

        # Check if nameTex is not defined.
        try:
            self._nameTex
        except AttributeError:
            # If not defined, just return the name.
            return self._name
        else:
            # Otherwise, return the nameTex.
            return self._nameTex
                
    @nameTex.setter
    def nameTex(self, nameTex):
        """
        @brief: Setter for nameTex.

        @param: nameTex New nameTex to set.
        """

        if(type(nameTex) != str):
            raise ValueError("'%s' is not a valid type for the 'nameTex' property of '%s'. Use string type instead." % (str(nameTex),self._name))

        self._nameTex = nameTex

    @property
    def units(self):
        """
        @brief: Units of the symbol.
        """

        # Check if units is not defined.
        try:
            self._units
        except AttributeError:
            # If not defined, just return and empty string.
            return ""
        else:
            # Otherwise, return the units.
            return self._units
                
    @units.setter
    def units(self, units):
        """
        @brief: Setter for units.

        @param: units New units to set.
        """

        if(type(units) != str):
            raise ValueError("'%s' is not a valid type for the 'units' property of '%s'. Use string type instead." % (str(units),self._name))

        self._units = units
