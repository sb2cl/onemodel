import sys

from onemodel.objects.builtin_function import BuiltinFunction


builtin_functions = {}

def add_builtin_function(name, argument_names, body):
    func = BuiltinFunction()
    func["argument_names"] = argument_names
    func["body"] = body

    builtin_functions[name] = func

def load_builtin_functions(namespace):
    """ Load all the built-in functions into a given namespace.
    """

    for function_name, function in builtin_functions.items():
        namespace[function_name] = function

### Definition of built-in functions. ###

def exit_(scope):
    scope.namespaces[0]["__exit__"] = 1

add_builtin_function("exit", [], exit_)

def print_(scope):
    print(scope["value"])
    return None
add_builtin_function("print", ["value"], print_)

def globals_(scope):
    namespace = scope.namespaces[0]

    from tabulate import tabulate
    
    data = []
    
    for name in reversed(list(namespace.keys())):

        value = repr(namespace[name])
    
        if isinstance(namespace[name], dict):
            doc = namespace[name]['__doc__']
        else:
            doc =""
    
        row = [name, value, doc]
        data.append(row)

    result = tabulate(data, headers=['Name', 'Value', 'Documentation'])

    print(result)
    print()
 
    return None

add_builtin_function("globals", [""], globals_)

def locals_(scope):

    namespace = scope.namespaces[-2]

    from tabulate import tabulate
    
    data = []
    
    for name in reversed(list(namespace.keys())):

        value = repr(namespace[name])
    
        if isinstance(namespace[name], dict):
            doc = namespace[name]['__doc__']
        else:
            doc =""
    
        row = [name, value, doc]
        data.append(row)

    result = tabulate(data, headers=['Name', 'Value', 'Documentation'])

    print(result)
    print()
    
    return None

add_builtin_function("locals", ["value"], locals_)

def show(scope):
    value = scope["value"]

    if value and isinstance(value, dict):
        namespace = value
    else:
        print(value)
        print()

        return None

    from tabulate import tabulate
    
    data = []
    
    for name in reversed(list(namespace.keys())):

        value = repr(namespace[name])
    
        if isinstance(namespace[name], dict):
            doc = namespace[name]['__doc__']
        else:
            doc =""
    
        row = [name, value, doc]
        data.append(row)

    result = tabulate(data, headers=['Name', 'Value', 'Documentation'])

    print(result)
    print()
    
    return None

add_builtin_function("show", ["value"], show)
