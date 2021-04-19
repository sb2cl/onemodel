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
