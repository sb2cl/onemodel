from onemodel.dsl.values.function_base import FunctionBase

class FunctionBuiltin(FunctionBase):
    """ FunctionBuiltin are funtions loaded in the root context by default.
    """
    def __init__(self, name):
        """ Initialize built-in function.
        """
        super().__init__(name)

    def __call__(self, walker, args):
        calling_context = walker.current_context

        execution_context = self.generate_execution_context(calling_context)

        method_name = f'call_{self.name}'
        method = getattr(self, method_name, None)

        self.check_and_populate_args(
            method.arg_names, 
            args,
            execution_context
        )

        result = method(execution_context)

        return result

    def __str__(self):
        return f'<built-in function {self.name}>'

    def __repr__(self):
        return self.__str__()

    ### Definition of built-in functions as methods ###

    def call_print(self, exec_context):
        """ Print value into stdout.
        """
        value = exec_context.get('value')
        print(value)

    call_print.arg_names = ['value']

    def call_showContext(self, exec_context):
        """ Show current context.
        """
        context = exec_context.parent
        context.print()

    call_showContext.arg_names = []

    def call_strcmp(self, exec_context):
        """ Show current context.
        """
        str_1 = exec_context.get('str_1')
        str_2 = exec_context.get('str_2')

        return str_1.value == str_2.value

    call_strcmp.arg_names = ['str_1', 'str_2']
