from onemodel.objects.object import Object


def test_init():
    result = Object()

    assert isinstance(result, Object)

def test_attributes():
    obj = Object()

    obj['a'] = 1

    assert obj['a'] == 1
