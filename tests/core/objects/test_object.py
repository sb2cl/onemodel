from onemodel.core.objects.object import Object


def test_init():
    result = Object()

    assert isinstance(result, Object)
