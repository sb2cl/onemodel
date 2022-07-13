from onemodel.onemodel_walker import OneModelWalker
from onemodel.objects.parameter import Parameter

def test_init():
    result = OneModelWalker()

    assert isinstance(result, OneModelWalker)
    assert result.parser

def test_walk_Parameter():
    model = """
    parameter a0 = 1
    parameter a1 = 3, a2 
    parameter a3
    """

    walker = OneModelWalker()  
    walker.run(model)
    result = walker.onemodel.root

    assert result["a0"]["value"] == 1
    assert result["a1"]["value"] == 3
    assert result["a2"]["value"] == 0
    assert isinstance(result["a3"], Parameter)
