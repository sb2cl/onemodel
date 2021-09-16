from onemodel.dsl.symbols.symbol import Symbol

class VariableSymbol(Symbol):
    def __init__(self, name, context, value):
        super().__init__(name, context)
        self.value = value

    def __str__(self):
        return f'<variable {self.name} = {self.value}>'

    def __repr__(self):
        return self.__str__()
