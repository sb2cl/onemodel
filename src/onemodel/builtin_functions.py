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
    exit()
add_builtin_function("exit", [], exit_)

def print_(scope):
    print(scope["value"])
    return None
add_builtin_function("print", ["value"], print_)

def globals_(scope):
    global_namespace = scope.namespaces[0]
    print('{')
    for name in global_namespace:
        print(f"    {name} : {global_namespace[name]}")
    print('}')
    return None
add_builtin_function("globals", [""], globals_)

def list_namespace(scope):
    namespace = scope.namespaces[-2]
    print('{')
    for name in namespace:
        print(f"    {name} : {namespace[name]}")
    print('}')
    return None
add_builtin_function("list_namespace", [""], list_namespace)

