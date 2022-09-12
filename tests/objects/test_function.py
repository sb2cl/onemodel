from onemodel.objects.function import Function
from onemodel.onemodel import OneModel
from onemodel.objects.object import Object
from onemodel.objects.parameter import Parameter
from onemodel.scope import Scope
from onemodel.namespace import Namespace

def test_init():
    result = Function()

    assert isinstance(result, Function)

def get_value(scope):
    value = scope["parameter"]["value"]

    return value

def test_call():
    
    m = OneModel()
    
    m["foo"] = Parameter()

    m["get"] = Function()
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
    m["foo"]["increase"] = Function()
    m["foo"]["increase"]["argument_names"] = ["self"]
    m["foo"]["increase"]["body"] = method_increase

    m["foo"]["increase"].call(m, [m["foo"]])
    m["foo"]["increase"].call(m, [m["foo"]])
    m["foo"]["increase"].call(m, [m["foo"]])

    result = m["foo"]["bar"]["value"]

    assert result == 3
