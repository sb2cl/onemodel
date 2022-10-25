import os

from onemodel.objects.object import Object

def find_module(walker, module_name, qualifiers=None, dots_number=0):
    """Find the absolute path of a module."""

    filepath = walker.onemodel["__file__"]

    if os.path.isdir(filepath):
        dirpath = filepath
    else:
        dirpath = os.path.dirname(filepath)

    dots_number = dots_number - 1

    if dots_number < 0:
        dots_number = 0

    for i in range(dots_number):
        dirpath = os.path.dirname(dirpath)
    
    if qualifiers:
        module_name = "/".join(qualifiers) + "/" +  module_name 

    filename = dirpath + "/" + module_name + '.one'
    
    if os.path.isfile(filename):
        result = os.path.abspath(filename)
        return result

    module_name = module_name.split("/", 1)
    module_name = module_name[0] + "/src/" + module_name[1]

    libpath = os.path.abspath(os.getcwd()) + "/lib"
    filename = libpath + "/" + module_name + '.one'
    result = os.path.abspath(filename)
    return result

def load_module(walker, module_name, import_name=None, assign_name=None, qualifiers=None, dots_number=0):
    """Load the code of a module into a Module object. """

    filename = find_module(walker, module_name, qualifiers, dots_number)

    module = Module()
    module["__name__"] = module_name
    module["__file__"] = filename

    file = open(filename)
    text = file.read()
    file.close()
    
    walker.onemodel.push(module)
    walker.run(text)
    walker.onemodel.pop()

    if assign_name is None and import_name:
        assign_name = import_name

    if assign_name is None:
        assign_name = module_name

    namespace = walker.onemodel

    if qualifiers is not None:
        for qualifier in qualifiers:
            namespace[qualifier] = Module()
            namespace = namespace[qualifier]

    namespace = walker.onemodel

    if import_name:
        namespace[assign_name] = module[import_name]
    else:
        namespace[assign_name] = module

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

    def __repr__(self):
        result = "<module"
        result += ">"

        return result
