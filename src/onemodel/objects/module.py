import os

from onemodel.objects.object import Object

def find_module(module_name):
    """Find the absolute path of a module."""

    filename = module_name + '.one'
    result = os.path.abspath(filename)
    return result

def load_module(module_name):
    """Load the code of a module into a Module object. """
    module = Module()
    module["__name__"] = module_name
    module["__file__"] = find_module(module_name)
    return module

class Module(Object):
    """A module is where is saved the execution of a OneModel script.

    Parameters
    ----------
    __name__ : :obj:`str`
        Name of the module.
    __file__ : :obj:`str`
        Absolute path to the file which contains the module.
    """

    def __init__(self):
        super().__init__()
        self["__name__"] = ""
        self["__file__"] = ""
