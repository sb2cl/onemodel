from onemodel.scope import Scope
from onemodel.namespace import Namespace


def test_init():
    result = Scope()
    assert isinstance(result, Scope)

def test_push():
    scope = Scope()
    namespace = Namespace()

    scope.push(namespace)

    assert scope.namespaces[-1] == namespace

def test_pop():
    scope = Scope()
    n1 = Namespace()
    n2 = Namespace()

    scope.push(n1)
    scope.push(n2)
    scope.pop()

    assert scope.namespaces[-1] == n1

def test_peek():
    scope = Scope()
    namespace = Namespace()

    scope.push(namespace)

    assert scope.peek() == namespace

    scope.pop()

    assert scope.peek() == None

def test_set():
    scope = Scope()
    namespace = Namespace()
    
    scope.push(namespace)
    scope["foo"] = 1

    assert scope.peek()["foo"] == 1

def test_get():
    scope = Scope()
    namespace = Namespace()
    
    scope.push(namespace)
    scope["foo"] = 1

    assert scope["foo"] == 1

def test_nested_get():
    scope = Scope()
    n1 = Namespace()
    n2 = Namespace()
    
    scope.push(n1)
    scope["foo"] = 1
    scope["bar"] = 1

    scope.push(n2)
    scope["bar"] = 2

    assert scope["foo"] == 1
    assert scope["bar"] == 2

    scope.pop()

    assert scope["bar"] == 1

def test_get_fullname():
    scope = Scope()
    n0 = Namespace()
    n1 = Namespace()
    n2 = Namespace()
 
    scope.push(n0, "")
    scope["foo"] = 1
    scope.push(n1, "n1")
    scope["bar"] = 1
    scope.push(n2, "n2")
    scope["baz"] = 1

    assert scope.get_fullname("foo") == "foo"
    assert scope.get_fullname("bar") == "n1__bar"
    assert scope.get_fullname("baz") == "n1__n2__baz"
