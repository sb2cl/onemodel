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
    def nameTex(self, n):
        """
        @brief: Setter for nameTex.

        @param: n New nameTex to set.
        """

        if(type(n) != str):
            raise ValueError("'%s' is not a valid type for the 'nameTex' property of '%s'. Use string type instead." % (str(n),self._name))

        self._nameTex = n
