from onemodel.dsl.values.function_base import FunctionBase

class Function(FunctionBase):
    def __init__(self, name, arg_names, body_node):
        super().__init__(name)
        self.arg_names = arg_names
        self.body_node = body_node

    def __call__(self, calling_context, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker

        execution_context = self.generate_execution_context(calling_context)

        self.check_and_populate_args(
            self.arg_names,
            args,
            execution_context
        )
        
        walker = OneModelWalker(
            'repl', 
            execution_context
        )

        result = walker.walk(self.body_node)

        return result

    def __str__(self):
        return f'<function {self.name}>'

    def __repr__(self):
        return self.__str__()
