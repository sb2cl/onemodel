class ModelPart:
    """ MODELPART

    This class is the base implementacion for the Variable, Parameter and Equation classes.
    """

    def __init__(self,om):
        """
        @brief: Constructor of ModelPart.
        
        @param: om OneModel object.
        """

        # String name of the ModelPart.
        self.name = "null"
        # The namespace of the ModelPart.
        self.namespace = om.namespace 
        # The OneModel object which this ModelPart is included.
        self.om = om

    @property
    def name(self):
        """
        @brief: Getter for name.
        """

        return self._name

    @name.setter
    def name(self, n):
        """
        @brief: Setter for name.

        @param: n New name to set.
        """

        if(type(n) != str):
            raise ValueError("'%s' has not a valid type for the name. Use string type instead." % str(n))

        if(n == ""):
            raise ValueError("The name of the ModelPart empty.") 

        self._name = n



