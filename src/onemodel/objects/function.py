from onemodel.objects.object import Object
from onemodel.scope import Scope
from onemodel.namespace import Namespace


class Function(Object):
    """A code that will be executed in a separate namespace. 

    Parameters
    ----------
    argument_names : :obj:`list` of :obj:`str`
        Names of the arguments.
    body : :obj:`function`
        A Python function object.
    """

    def __init__(self):
        super().__init__()

        self["argument_names"] = []
        self["body"] = None

    def call(self, scope, parameter_names):
        """Execute the function body. 

        Parameters
        ----------
        scope : :obj:`Scope`
            The scope where the function is called.
        parameter_names : :obj:`list` of :obj:`str`
            The names of the parameters passed to the function.
        """

        func_namespace = self.create_function_namespace(scope, parameter_names)

        scope.push(func_namespace)
        result = self["body"](scope)
        scope.pop()

        return result

    def create_function_namespace(self, scope, parameter_names):
        """Create the local namespace for the execution of the function.

        Parameters
        ----------
        scope : :obj:`Scope`
            The scope where the function is called.
        parameter_names : :obj:`list` of :obj:`str`
            The names of the parameters passed to the function.
        """

        result = Namespace()

        if parameter_names is None:
            return result

        for arg_name, param_name in zip(self["argument_names"], parameter_names):
            result[arg_name] = scope[param_name]

        return result
