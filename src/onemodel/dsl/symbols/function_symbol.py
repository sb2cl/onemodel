from onemodel.dsl.symbols.symbol import Symbol
from onemodel.dsl.context import Context

class FunctionSymbol(Symbol):
    def __init__(self, name, context, body_node):
        super().__init__(name, context)
        self.body_node = body_node

    def __call__(self, calling_context, args):
        from onemodel.dsl.onemodel_walker import OneModelWalker
        
        execution_context = Context(
            f'{self.name}',
            calling_context
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
