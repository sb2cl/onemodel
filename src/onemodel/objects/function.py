from onemodel.objects.base_function import BaseFunction

class Function(BaseFunction):
    """ Functions that are implemented with OneModel code.

    Parameters
    ----------
    argument_names : :obj:`list` of :obj:`str`
        Names of the arguments.
    body : :obj:`ast`
        The abstract syntax tree of the OneModel function.
    """

    def execute(self, scope):
        """ Run the builtin function given the scope. """
        result = self.walker.walk(self["body"])
        return result

    def __repr__(self):
        result = "<function"
        result += ">"

        return result
