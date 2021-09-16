from onemodel.dsl.values.base_function import BaseFunction

class BuiltInFunction(BaseFunction):
    """ BuiltInFunctions are functions loaded into the root context.
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
        value = exec_context.get('value')
        print(value)

    call_print.arg_names = ['value']

    def call_printSbml(self, exec_context):
        """ Print in stdout the sbml representation of the model.
        """
        from libsbml import writeSBMLToString

        main_context = exec_context.getRootContext() 

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
        """ Show the context.
        """
        context = exec_context.parent

        if context.parent != None:
            parent_namespace = context.parent.namespace
        else:
            parent_namespace = 'None'

        print('### Context ###')
        print(f'%-25s %s' % ('namespace', f'"{context.namespace}"'))
        print(f'%-25s %s' % ('parent_namespace',f'"{parent_namespace}"'))
        # print()
        print('### Context.locals  ###')
        for local in context.locals:
            name = local
            value = context.get(name)
            print(f'%-25s %s' % (name, value))

        return
    call_showContext.arg_names = []

    def call_showValueContext(self, exec_context):
        """ Show the context a value.
        """
        object_ = exec_context.get('object')

        context = object_.context
        print(context.locals)
        print(context.parent.parent.locals)

        if context.parent.parent != None:
            parent_namespace = context.parent.parent.namespace
        else:
            parent_namespace = 'None'

        print('### Context ###')
        print(f'%-25s %s' % ('namespace', f'"{context.namespace}"'))
        print(f'%-25s %s' % ('parent_namespace',f'"{parent_namespace}"'))
        # print()
        print('### Context.locals ###')
        for local in context.locals:
            name = local
            value = context.get(name)
            print(f'%-25s %s' % (name, value))

        return
    call_showValueContext.arg_names = ['object']

    def call_run(self, exec_context):
        """ Run a file.
        """
        # We will execute the file commands in parent context.
        # This way, all values will be loaded into the parent.
        context = exec_context.parent

        filename = exec_context.get('filename').value
        text = open(filename).read()

        walker = context.walker

        walker.run(text)
        
        return None
    call_run.arg_names = ['filename']

    def call_getFullName(self, exec_context):
        """ Get the fullname of a value.
        """
        value = exec_context.get('name')

        print(value)

        return None
    call_getFullName.arg_names = ['name']


