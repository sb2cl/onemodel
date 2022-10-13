from onemodel.objects.object import Object
from onemodel.objects.base_function import BaseFunction

class Model(BaseFunction):
    """ Models defined with onemodel syntax.

    Parameters
    ----------
    body : :obj:`ast`
        The abstract syntax tree of the body of a model.
    """

    def execute(self, scope):
        """ Run the builtin function given the scope. """

        scope["self"] = Object()
        scope.push(scope["self"])

        self.walker.walk(self["body"])

        scope.pop()
        result = scope["self"]

        return result

    def extend(self):
        """Execute the model into current namespace. """
        self.walker.walk(self["body"])

    def __repr__(self):
        result = "<model"
        result += ">"

        return result
