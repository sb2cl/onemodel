from onemodel.core.objects.object import Object
from onemodel.core.scope import Scope
from onemodel.core.namespace import Namespace


class Function(Object):

    def __init__(self):
        self.argumentNames = []
        self.body = None

    def call(self, scope, argumentValues):

        function_namespace = Namespace()

        for name, value in zip(self.argumentNames, argumentValues):
            function_namespace[name] = scope[value]

        scope.push(function_namespace)
        result = self.body(scope)
        scope.pop()

        return result
