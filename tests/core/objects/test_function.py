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
    
    m.root["foo"] = Parameter()

    m.root["get"] = Function()
    m.root["get"].argument_names = ["parameter"]
    m.root["get"].body = get_value

    scope = Scope()
    scope.push(m.root)
    result = m.root["get"].call(scope, ["foo"])

    expected = m.root["foo"].value

    assert result == expected

def method_increase(scope):

    parameter = scope["self"]["bar"]
    parameter.value = parameter.value + 1

def test_method():
    m = OneModel()
    
    m.root["foo"] = Object()

    m.root["foo"]["bar"] = Parameter()
    m.root["foo"]["increase"] = Function()
    m.root["foo"]["increase"].argument_names = ["self"]
    m.root["foo"]["increase"].body = method_increase

    scope = Scope()
    scope.push(m.root)
    m.root["foo"]["increase"].call(scope, ["foo"])
    m.root["foo"]["increase"].call(scope, ["foo"])
    m.root["foo"]["increase"].call(scope, ["foo"])

    result = m.root["foo"]["bar"].value

    assert result == 3
