from onemodel.core.namespace import Namespace


def test_init_namespace():
    result = Namespace()
    assert isinstance(result, Namespace)


def test_set_and_get():
    ns = Namespace()

    ns["a"] = 1
    result = ns["a"]

    assert result == 1


def test_delete():
    ns = Namespace()

    ns["a"] = 1
    del ns["a"]
    result = ns["a"]

    assert result == None


def test_names():
    ns = Namespace()

    ns["a"] = 1
    ns["b"] = 2
    ns["c"] = 3

    result = ns.names()
    expected = ["a", "b", "c"]

    assert result == expected


def test_items():
    ns = Namespace()

    ns["a"] = 1
    ns["b"] = 2
    ns["c"] = 3

    result = ns.items()
    expected = [("a", 1), ("b", 2), ("c", 3)]

    assert result == expected

def test_is_empty():
    root = Namespace()

    assert root.is_empty() == True

def test_has_name():
    ns = Namespace()
    ns["foo"] = 1

    assert ns.has_name("foo") == True
    assert ns.has_name("bar") == False

