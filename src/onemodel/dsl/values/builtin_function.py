from onemodel.dsl.values.base_function import BaseFunction

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

    def __call__(self, args):
        exec_context = self.generate_new_context()

        method_name = f'call_{self.name}'
        method = getattr(self, method_name, None)

        self.check_and_populate_args(
            method.arg_names, 
            args,
            exec_context
        )

        result = method(exec_context)

        return result

    ### Definition of built-in functions as methods ###

    def call_print(self, exec_context):
        """ Print the argument into stdout.
        """
        value = exec_context.symbol_table.get('value')
        print(value)

    call_print.arg_names = ['value']

    def call_printSbml(self, exec_context):
        """ Print in stdout the sbml representation of the model.
        """
        from libsbml import writeSBMLToString

        document = exec_context.walker.document
        print(writeSBMLToString(document))

        return None
    call_printSbml.arg_names = []

    def call_exit(self, exec_context):
        """ Exit onemodel.
        """
        import sys
        sys.exit()
        
        return
    call_exit.arg_names = []

