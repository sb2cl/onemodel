from onemodel.core.objects.function import Function

from onemodel.core.onemodel import OneModel
from onemodel.core.objects.parameter import Parameter
from onemodel.core.scope import Scope
from onemodel.core.namespace import Namespace

def test_init():
    result = Function()

    assert isinstance(result, Function)

def my_print_function(scope):
    value = scope["value"].value

    return value

def test_call():
    
    m = OneModel()
    
    m.root["param"] = Parameter()

    m.root["func"] = Function()
    m.root["func"].argumentNames = ["value"]
    m.root["func"].body = my_print_function

    scope = Scope()
    scope.push(m.root)

    result = m.root["func"].call(scope, ["param"])

    assert result == 0.0
