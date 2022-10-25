from onemodel.objects.base_function import BaseFunction

class BuiltinFunction (BaseFunction):
    """ Built-in functions that are implemented with Python
    functions.

    Parameters
    ----------
    argument_names : :obj:`list` of :obj:`str`
        Names of the arguments.
    body : :obj:`function`
        A Python function object.
    """

    def __init__(self):
        super().__init__()

        self["body"] = None

    def execute(self, scope):
        """ Run the builtin function given the scope. """
        result = self["body"](scope)
        return result

    def __repr__(self):
        result = "<builtin-function"
        result += ">"

        return result
