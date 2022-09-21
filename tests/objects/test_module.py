from onemodel.objects.module import Module

def test_init():
    result = Module()
    assert isinstance(result, Module)
