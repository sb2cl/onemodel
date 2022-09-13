from onemodel.objects.builtin_function import BuiltinFunction
from onemodel.onemodel import OneModel
from onemodel.objects.object import Object
from onemodel.objects.parameter import Parameter
from onemodel.scope import Scope
from onemodel.namespace import Namespace

def test_init():
    result = BuiltinFunction()

    assert isinstance(result, BuiltinFunction)

def get_value(scope):
    value = scope["parameter"]["value"]

    return value

def test_call():
    
    m = OneModel()
    
    m["foo"] = Parameter()

    m["get"] = BuiltinFunction()
    m["get"]["argument_names"] = ["parameter"]
    m["get"]["body"] = get_value

    result = m["get"].call(m, [m["foo"]])

    expected = m["foo"]["value"]

    assert result == expected

def method_increase(scope):

    parameter = scope["self"]["bar"]
    parameter["value"] = parameter["value"] + 1

def test_method():
    m = OneModel()
    
    m["foo"] = Object()

    m["foo"]["bar"] = Parameter()
    m["foo"]["increase"] = BuiltinFunction()
    m["foo"]["increase"]["argument_names"] = ["self"]
    m["foo"]["increase"]["body"] = method_increase

    m["foo"]["increase"].call(m, [m["foo"]])
    m["foo"]["increase"].call(m, [m["foo"]])
    m["foo"]["increase"].call(m, [m["foo"]])

    result = m["foo"]["bar"]["value"]

    assert result == 3
