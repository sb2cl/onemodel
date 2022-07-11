from onemodel.core.objects.object import Object
from onemodel.core.scope import Scope
from onemodel.core.namespace import Namespace


class Function(Object):

    def __init__(self):
        self.argument_names = []
        self.body = None

    def call(self, scope, parameter_names):

        func_namespace = self.create_function_namespace(scope, parameter_names)

        scope.push(func_namespace)
        result = self.body(scope)
        scope.pop()

        return result

    def create_function_namespace(self, scope, parameter_names):
        result = Namespace()

        for arg_name, param_name in zip(self.argument_names, parameter_names):
            result[arg_name] = scope[param_name]

        return result
