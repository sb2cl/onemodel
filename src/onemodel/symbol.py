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
    def name(self, name):
        """ Set the symbol name.
        
        Set the symbol name and check that it its a valid name.
        
        Args:
            name: str
                New name to set.

        Raises:
            ValueError: The passed name is not valid.
        """
        # Name must be a str
        if(type(name) != str):
            raise ValueError("""'%s' is not a valid type for the name. Use string
                    type instead.""" % str(name))

        # Name cannot be an empty st
        if(name == ""):
            raise ValueError("The name of the ModelPart is empty.") 

        # Check if the name already has an namespace.
        if name.find("::")==-1:
            # If not, add it.
            self._name = self.om.namespace + name
        else:
            self._name = name

    @property
    def namebase(self):
        """ The symbol name without the namespace

        Example: the namebase of "std::my_var" is "my_var".
        """
        # Find where the namespace ends
        ind = self._name.rfind("::")

        # Remove the namespace
        if ind != -1:
            namebase = self._name[ind+2:]
        else:
            namebase = self._name

        return namebase

    @property
    def nametex(self):
        """ The name used for LaTeX generation.

        """

        # Check if nametex is not defined.
        try:
            self._nametex
        except AttributeError:
            # If not defined, just return the name.
            return self._name
        else:
            # Otherwise, return the nametex.
            return self._nametex
                
    @nametex.setter
    def nametex(self, nametex):
        """
        @brief: Setter for nametex.

        @param: nametex New nametex to set.
        """

        if(type(nametex) != str):
            raise ValueError("""'%s' is not a valid type for the 'nametex'
                    property of '%s'. Use string type instead."""
                    % (str(nametex),self._name))

        self._nametex = nametex

    @property
    def units(self):
        """ Units of the symbol.

        The units related to the symbol. For parameters and variables is the
        unit of its value. Units is not defined in equations.
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
        """ Set the units.

        Set the units of the symbol and check they are valid.

        Args:
            units: str
                New units to set.

        Raises:
            ValueError: The units are not valid.
        """
        # Units must be an str
        if(type(units) != str):
            raise ValueError("""'%s' is not a valid type for the 'units' property
                    of '%s'. Use string type instead."""
                    % (str(units),self._name))

        self._units = units

    @property
    def comment(self):
        """ One-line comment for the symbol.

        One-line comment which explains what is this symbol.
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
        """ Set the comment.

        Set the comment and check it is valid.

        Args:
            comment: str
                New comment to set.

        Raises:
            ValueError: The comment is not valid.
        """
        # Must be an str
        if(type(comment) != str):
            raise ValueError("""'%s' is not a valid type for the 'comment'
                    property of '%s'. Use string type instead."""
                    % (str(comment),self._name))

        # TODO: Check that the comment is one-line.

        self._comment = comment

    @property
    def description(self):
        """ Multi-line description of the symbol.

        Multi-line description of the symbol which explains in depth all the
        information realted to the symbol.
        """
        # Check if description is not defined.
        try:
            self._description
        except AttributeError:
            # If not defined, just return and empty string.
            return ""
        else:
            # Otherwise, return the description.
            return self._description
                
    @description.setter
    def description(self, description):
        """ Set the description.

        Set the description and check it is valid.

        Args:
            description: str
                New description to set.

        Raises:
            ValueError: The description is not valid.
        """
        # Must be an str
        if(type(description) != str):
            raise ValueError("""'%s' is not a valid type for the 'description'
                    property of '%s'. Use string type instead."""
                    % (str(description),self._name))

        self._description = description

    @property
    def reference(self):
        """ The reference of the symbol.

        The reference of the symbol is a multi-line str with all the
        information to track the reference of the value or the definition of
        the symbol.

        It could be the reference to a paper, to a bionumber or a book.
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
        """ Set the reference.

        Set the reference and check if it is valid.

        Args:
            reference: str
                New reference to set.

        Raises:
            ValueError: The reference is not valid.
        """

        if(type(reference) != str):
            raise ValueError("""'%s' is not a valid type for the 'reference'
            property of '%s'. Use string type instead.""" % (str(reference),self._name))

        self._reference = reference
    
    def __repr__(self):
        """ Representation method.
        
        """
        out = f'{self.name}\n'
        out += f'\tname = {self.name}\n'
        out += f'\tnamebase = {self.namebase}\n'
        out += f'\tnametex = {self.nametex}\n'
        out += f'\tunits = {self.units}\n'
        out += f'\tcomment = {self.comment}\n'
        out += f'\tdescription = {self.description}\n'
        out += f'\treference = {self.reference}\n'
        return out
                
        
