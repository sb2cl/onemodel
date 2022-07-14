from onemodel.onemodel_walker import OneModelWalker
from onemodel.objects.parameter import Parameter

def test_init():
    result = OneModelWalker()

    assert isinstance(result, OneModelWalker)
    assert result.parser

def test_walk_Integer():
    model = """
    0
    10
    420
    """
    walker = OneModelWalker()  
    result, ast = walker.run(model)

    expected = [0, 10, 420]
    assert result == expected

def test_walk_Float():
    model = """
    0.0
    1.0
    .9
    01.50
    0.001
    1e2
    0.1e+4
    1e-2
    """
    walker = OneModelWalker()  
    result, ast = walker.run(model)
    expected = [0.0, 1.0, 0.9, 1.5, 0.001, 1e2, 1e3, 1e-2]
    assert result == expected

def test_walk_Parameter():
    model = """
    parameter a0 = 1
    parameter a1 = 3, a2 
    parameter a3
    """

    walker = OneModelWalker()  
    ast = walker.run(model)
    result = walker.onemodel.root

    assert result["a0"]["value"] == 1
    assert result["a1"]["value"] == 3
    assert result["a2"]["value"] == 0
    assert isinstance(result["a3"], Parameter)
