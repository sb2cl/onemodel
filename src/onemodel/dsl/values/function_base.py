from onemodel.dsl.values.value import Value
from onemodel.dsl.context import Context

class FunctionBase(Value):
    """ FunctionBase class for defining builting functions and user defined
    functions.
    """
    def __init__(self, name):
        """ Initialize FunctionBase.
        """
        super().__init__()
        self.name = name

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
            execution_context.set(arg_name, arg_value, False)

    def check_and_populate_args(self, arg_names, args, execution_context):
        """ Check and populate arguments.
        """
        self.check_arguments(arg_names, args)
        self.populate_args(arg_names, args, execution_context)

    def add_value_to_model(self, name, model):
        # Functions are not added to SBML models.
        pass
