from onemodel.dsl.values.base_function import BaseFunction

class Function(BaseFunction):
    """ User-defined function.
    """
    def __init__(self, name, arg_names, body_node):
        """ Initialize Function.
        """
        super().__init__(name)
        self.arg_names = arg_names
        self.body_node = body_node

    def __str__(self):
         return f"<function {self.name}>"

    def __repr__(self):
         return self.__str__()

    def __call__(self, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker

        exec_context = self.generate_new_context()

        self.check_and_populate_args(
            self.arg_names, 
            args,
            exec_context
        )

        walker = OneModelWalker('repl', exec_context)
        result = walker.walk(self.body_node)

        return result

