from onemodel.core.objects.function import Function

from onemodel.core.onemodel import OneModel
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
