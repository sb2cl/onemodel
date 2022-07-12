from onemodel.core.namespace import Namespace


def test_init_namespace():
    result = Namespace()
    assert isinstance(result, Namespace)

def test_is_empty():
    root = Namespace()
    assert root.is_empty() == True
    root['foo'] = 1
    assert root.is_empty() == False
