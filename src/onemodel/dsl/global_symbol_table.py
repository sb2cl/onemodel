from onemodel.dsl.symbol_table import SymbolTable
from onemodel.dsl.values.builtin_function import BuiltInFunction

class GlobalSymbolTable(SymbolTable):
    def __init__(self):
        super().__init__()

        self.addBuiltInFunction('print')
        self.addBuiltInFunction('printSbml')
        self.addBuiltInFunction('exit')
        self.addBuiltInFunction('showContext')
        self.addBuiltInFunction('run')

    def addBuiltInFunction(self, name):
        self.set(name, BuiltInFunction(name))
