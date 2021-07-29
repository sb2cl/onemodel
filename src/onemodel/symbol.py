from onemodel.model_part import ModelPart

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

    @property
    def comment(self):
        """
        @brief: Comment of the symbol.
        """

        # Check if comment is not defined.
        try:
            self._comment
        except AttributeError:
            # If not defined, just return and empty string.
            return ""
        else:
            # Otherwise, return the comment.
            return self._comment
                
    @comment.setter
    def comment(self, comment):
        """
        @brief: Setter for comment.

        @param: comment New comment to set.
        """

        if(type(comment) != str):
            raise ValueError("'%s' is not a valid type for the 'comment' property of '%s'. Use string type instead." % (str(units),self._name))

        self._comment = comment

    @property
    def reference(self):
        """
        @brief: Reference of the symbol value.
        """

        # Check if reference is not defined.
        try:
            self._reference
        except AttributeError:
            # If not defined, just return and empty string.
            return ""
        else:
            # Otherwise, return the reference.
            return self._reference
                
    @reference.setter
    def reference(self, reference):
        """
        @brief: Setter for reference.

        @param: reference New reference to set.
        """

        if(type(reference) != str):
            raise ValueError("'%s' is not a valid type for the 'reference' property of '%s'. Use string type instead." % (str(reference),self._name))

        self._reference = reference
