from onemodel.objects.object import Object
from onemodel.scope import Scope
from onemodel.namespace import Namespace


class BaseFunction(Object):
    """Base class for defining functions.

    Parameters
    ----------
    argument_names : :obj:`list` of :obj:`str`
        Names of the arguments.
    """

    def __init__(self):
        super().__init__()

        self["argument_names"] = []

    def call(self, scope, argument_values):
        """Execute the function body. 

        Parameters
        ----------
        scope : :obj:`Scope`
            The scope where the function is called.
        parameter_names : :obj:`list` of :obj:`str`
            The values of the arguments passed to the function.
        """

        func_namespace = self.create_function_namespace(
            scope, 
            argument_values
        )

        scope.push(func_namespace)
        result = self.execute(scope)
        scope.pop()

        return result

    def create_function_namespace(self, scope, argument_values):
        """Create the local namespace for the execution of the function.

        Parameters
        ----------
        scope : :obj:`Scope`
            The scope where the function is called.
        parameter_names : :obj:`list` of :obj:`str`
            The values of the arguments passed to the function.
        """

        result = Namespace()

        if argument_values is None:
            return result

        for name, value in zip(self["argument_names"], argument_values):
            result[name] = value

        return result

    def __repr__(self):
        result = "<base-function"
        result += ">"

        return result
