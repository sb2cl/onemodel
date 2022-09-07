from onemodel.objects.function import Function


builtin_functions = {}

def add_builtin_function(name, argument_names, body):
    func = Function()
    func["argument_names"] = argument_names
    func["body"] = body

    builtin_functions[name] = func

def load_builtin_functions(namespace):
    """ Load all the built-in functions into a given namespace.
    """

    for function_name, function in builtin_functions.items():
        namespace[function_name] = function

### Definition of built-in functions. ###

def hello(scope):
    print('Hello message')
    return None
add_builtin_function("hello", [], hello)

def exit_(scope):
    exit()
add_builtin_function("exit", [], exit_)
