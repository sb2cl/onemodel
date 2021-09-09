from onemodel.dsl.values.value import Value

class BaseFunction(Value):
    """ Base function class for defining builting functions and user defined
    functions.
    """
    def __init__(self, name = '<anonymous>'):
        """ Initialize BaseFunction.
        """
        super().__init__()
        self.name = name

class BuiltInFunction(BaseFunction):
    """ BuiltInFunctions are functions loaded into the symbol_table.
    """
    def __init__(self, name):
        """ Initialize BuiltInFunction.
        """
        super().__init__(name)

    def __str__(self):
        return f'<built-in function {self.name}>'

    def __repr__(self):
        return self.__str__()

    def __call__(self, exec_context):
        method_name = f'call_{self.name}'
        method = getattr(self, method_name, None)

        result = method(exec_context)

        return result

    ### Definition of built-in functions as methods ###

    def call_hello_world(self, exec_context):
        """ Hello world built-in function.
        """
        print('Hello world!')

        return None
    call_hello_world.arg_names = []    

    def call_printSbml(self, exec_context):
        """ printSbml built-in function.
        """
        from libsbml import writeSBMLToString

        document = exec_context.walker.document
        print(writeSBMLToString(document))

        return None
    call_printSbml.arg_names = []

    def call_exit(self, exec_context):
        """ exit built-in function.
        """
        import sys
        sys.exit()
        
        return
    call_exit.arg_names = []
