class ModelPart:
    """ MODELPART

    This class is the base implementacion for the Variable, Parameter and Equation classes.
    """

    def __init__(self,om,name):
        """
        @brief: Constructor of ModelPart.
        
        @param: om   OneModel object.
                name String Name for the Symbol.
        """

        # The OneModel object which this ModelPart is included.
        self.om = om
        # The name of the ModelPart with namespace.
        # (the namespace is added in name.setter).
        self.name = name  

    @property
    def name(self):
        """
        @brief: The name fow the ModelClass. It must be unique in all the ModelParts defined in the model. It will be use to identify the ModelPart.
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
    def namespace(self):
        """
        @brief: The namespace of the name.
        """

        ind = self._name.rfind("::")

        if ind != -1:
            namespace = self._name[0:ind+2]
        else:
            namespace = ""

        return namespace

