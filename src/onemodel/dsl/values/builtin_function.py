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

        print(result)

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

        main_context = exec_context.getMainParent() 

        walker = main_context.walker
        sbml = walker.getSBML()
        print(sbml)

        return None
    call_printSbml.arg_names = []

    def call_exit(self, exec_context):
        """ Exit onemodel.
        """
        import sys
        sys.exit()
        
        return None
    call_exit.arg_names = []

    def call_showContext(self, exec_context):
        """ Show the context and symbol table.
        """
        context = exec_context.parent

        if context.parent == None:
            parent_name = 'None'
        else:
            parent_name = context.parent.display_name

        symbol_table = context.symbol_table

        print('### Context ###')
        print(f'%-25s %s' % ('name', context.display_name))
        print(f'%-25s %s' % ('parent_name', parent_name))
        print()
        print('### Symbol table ###')
        for symbol in symbol_table.symbols:
            name = symbol
            value = symbol_table.get(name)
            print(f'%-25s %s' % (name, value))

        return
    call_showContext.arg_names = []

    def call_run(self, exec_context):
        """ Run a file.
        """
        # We will execute the file commands in parent context.
        # This way, all values will be loaded into the parent.
        context = exec_context.parent

        filename = exec_context.symbol_table.get('filename').value
        text = open(filename).read()

        print(text)
        
        return None
    call_run.arg_names = ['filename']


