from onemodel.dsl.symbols.symbol import Symbol
from onemodel.dsl.symbols.variable_symbol import VariableSymbol
from onemodel.dsl.context import Context

class BaseFunctionSymbol(Symbol):
    """ Base function class for defining builting functions and user defined
    functions.
    """
    def __init__(self, name, context):
        """ Initialize BaseFunctionSymbol.
        """
        super().__init__(name, context)

    def generate_execution_context(self, calling_context):
        """ Generate the execution context where the function will be
        evaluated.
        """
        execution_context = Context(
            f'{self.name}',
            calling_context
        )

        return execution_context
    
    def check_arguments(self, arg_names, args):
        """ Check the amount of arguments passed.
        """
        if len(args) > len(arg_names):
            raise Exception(
                f'{len(args) - len(arg_names)} too many arguments passed to {self}'
                )

        if len(args) < len(arg_names):
            raise Exception(
                f'{len(args) - len(arg_names)} too few arguments passed to {self}'
                )

    def populate_args(self, arg_names, args, execution_context):
        """ Populate the arguments into the execution context.
        """
        for i in range(len(args)):
            arg_name = arg_names[i] 
            arg_value = args[i]

            print(isinstance(arg_value, Symbol))
            if isinstance(arg_value, Symbol) == False:
                arg_value = VariableSymbol(
                    arg_name,
                    execution_context,
                    arg_value
                )

            print(isinstance(arg_value, Symbol))
            execution_context.set(arg_value)

    def check_and_populate_args(self, arg_names, args, execution_context):
        """ Check and populate arguments.
        """
        self.check_arguments(arg_names, args)
        self.populate_args(arg_names, args, execution_context)
