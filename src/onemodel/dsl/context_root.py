from onemodel.dsl.context import Context
# from onemodel.dsl.values.builtin_function import BuiltInFunction

class ContextRoot(Context):
    """ The root evaluation context.
    """
    def __init__(self):
        super().__init__()

    #    self.addBuiltInFunction('print')
    #    self.addBuiltInFunction('printSbml')
    #    self.addBuiltInFunction('exit')
    #    self.addBuiltInFunction('showContext')
    #    self.addBuiltInFunction('showValueContext')
    #    self.addBuiltInFunction('run')
    #    self.addBuiltInFunction('getFullName')

    #    self.namespace = 'std_'

    #def addBuiltInFunction(self, name):
    #    self.set(name, BuiltInFunction(name))
