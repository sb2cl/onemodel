from onemodel.core.objects.object import Object
from onemodel.core.scope import Scope
from onemodel.core.namespace import Namespace


class Function(Object):

    def __init__(self):
        self.argument_names = []
        self.body = None

    def call(self, scope, parameter_names):

        function_namespace = Namespace()

        for arg_name, param_name in zip(self.argument_names, parameter_names):
            function_namespace[arg_name] = scope[param_name]

        scope.push(function_namespace)
        result = self.body(scope)
        scope.pop()

        return result
