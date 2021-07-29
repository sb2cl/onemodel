from dataclasses import dataclass

from onemodel.onemodel import OneModel
   
@dataclass
class Symbol:
    """ Base class for model objects like: parameters, variables or equations.

    This class is the base for defining the rest of the model objects that
    populate onemodel models. Symbol defines the basic attributes for 
    identifing a symbol in the model (name, namebase) and also extra
    about the symbol itself like: comment, description, reference, etc.

    Attributes:
        name: str
            Symbol name with the namespace.
        namebase: str
            Symbol name without the namespace.
    """

    def __init__(self, om, name):
        """ Inits Symbol.

        Args:
            om: OneModel
                Parent OneModel object where this Symbol is included.
            name: str
                Symbol name (the namespace is added in name.setter).
        """
        self.om = om
        self.name = name  

    @property
    def name(self):
        """ Symbol name.

        The name associated to the Symbol, the name must be unique in the model
        because it will be used to find the Symbol in the symbol table in the
        onemodel model.
        """
        return self._name

    @name.setter
    def name(self, n):
        """
        @brief: Setter for name.

        @param: n New name to set.
        """
        if(type(n) != str):
            raise ValueError("'%s' is not a valid type for the name. Use string type instead." % str(n))

        if(n == ""):
            raise ValueError("The name of the ModelPart is empty.") 

        # Check if the name already has an namespace.
        if n.find("::")==-1:
            # If not, add it.
            self._name = self.om.namespace + n
        else:
            self._name = n

    @property
    def namebase(self):
        """
        @brief: The name without the namespace.
        """

        ind = self._name.rfind("::")

        if ind != -1:
            namebase = self._name[ind+2:]
        else:
            namebase = self._name

        return namebase

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
