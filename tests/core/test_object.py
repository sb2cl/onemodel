from onemodel.core.object import Object


def test_init():
    result = Object()

    assert isinstance(result, Object)
