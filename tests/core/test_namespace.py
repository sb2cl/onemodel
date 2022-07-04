from onemodel.core.namespace import Namespace


def test_init_namespace():
    result = Namespace(None)
    assert isinstance(result, Namespace)


def test_set_and_get():
    ns = Namespace(None)

    ns["a"] = 1
    result = ns["a"]

    assert result == 1


def test_delete():
    ns = Namespace(None)

    ns["a"] = 1
    del ns["a"]
    result = ns["a"]

    assert result == None


def test_names():
    ns = Namespace(None)

    ns["a"] = 1
    ns["b"] = 2
    ns["c"] = 3

    result = ns.names()
    expected = ["a", "b", "c"]

    assert result == expected


def test_items():
    ns = Namespace(None)

    ns["a"] = 1
    ns["b"] = 2
    ns["c"] = 3

    result = ns.items()
    expected = [("a", 1), ("b", 2), ("c", 3)]

    assert result == expected


def test_nested_namespaces():
    root = Namespace(None)

    root["a"] = 1
    root["ns"] = Namespace(root)
    assert root["ns"]["a"] == 1

    root["ns"]["a"] = 2
    assert root["ns"]["a"] == 2

    del root["ns"]["a"]
    assert root["ns"]["a"] == 1

    root["a"] = 3
    assert root["ns"]["a"] == 3

    del root["a"]
    assert root["ns"]["a"] == None

def test_is_empty():
    root = Namespace(None)

    assert root.is_empty() == True

