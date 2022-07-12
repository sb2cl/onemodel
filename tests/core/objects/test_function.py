from onemodel.core.objects.function import Function
from onemodel.core.onemodel import OneModel
from onemodel.core.objects.object import Object
from onemodel.core.objects.parameter import Parameter
from onemodel.core.scope import Scope
from onemodel.core.namespace import Namespace

def test_init():
    result = Function()

    assert isinstance(result, Function)

def get_value(scope):
    value = scope["parameter"].value

    return value

def test_call():
    
    m = OneModel()
    
    m["foo"] = Parameter()

    m["get"] = Function()
    m["get"].argument_names = ["parameter"]
    m["get"].body = get_value

    result = m["get"].call(m, ["foo"])

    expected = m["foo"].value

    assert result == expected

def method_increase(scope):

    parameter = scope["self"]["bar"]
    parameter.value = parameter.value + 1

def test_method():
    m = OneModel()
    
    m["foo"] = Object()

    m["foo"]["bar"] = Parameter()
    m["foo"]["increase"] = Function()
    m["foo"]["increase"].argument_names = ["self"]
    m["foo"]["increase"].body = method_increase

    m["foo"]["increase"].call(m, ["foo"])
    m["foo"]["increase"].call(m, ["foo"])
    m["foo"]["increase"].call(m, ["foo"])

    result = m["foo"]["bar"].value

    assert result == 3
