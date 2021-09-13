from onemodel.dsl.values.value import Value
from onemodel.dsl.context import Context
from onemodel.dsl.symbol_table import SymbolTable

class BaseFunction(Value):
    """ Base function class for defining builting functions and user defined
    functions.
    """
    def __init__(self, name = '<anonymous>'):
        """ Initialize BaseFunction.
        """
        super().__init__()
        self.name = name

    def generate_new_context(self):
        """ Generate a new context for executing the function.
        """
        new_context = Context(
            self.name, 
            self.context
        )

        new_context.symbol_table = SymbolTable(
            new_context.parent.symbol_table
        )

        return new_context

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

    def populate_args(self, arg_names, args, exec_context):
        """ Populate the arguments into the context symbol table.
        """
        for i in range(len(args)):
            arg_name = arg_names[i] 
            arg_value = args[i]
            arg_value.set_context(exec_context)
            exec_context.symbol_table.set(arg_name, arg_value)

    def check_and_populate_args(self, arg_names, args, exec_context):
        """ Check and populate arguments.
        """
        self.check_arguments(arg_names, args)
        self.populate_args(arg_names, args, exec_context)

    def add_value_to_model(self, name, model):
        # Functions are not included in SBML models.
        pass
