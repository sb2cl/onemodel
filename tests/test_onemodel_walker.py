from onemodel.onemodel_walker import OneModelWalker
from onemodel.objects.parameter import Parameter

def test_init():
    result = OneModelWalker()

    assert isinstance(result, OneModelWalker)
    assert result.parser

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

def test_walk_string():
    model = """
    \"This is a string\"
    \'This is other string\'
    """

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    expected = [
        "This is a string",
        "This is other string"
    ]

    assert result == expected

def test_walk_Docstring():
    model = '''
"""Hello world!
hola
"""
    '''

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    expected = "Hello world!\nhola\n"

    assert result == expected

    model = """
'''Hello world!
hola
'''
    """

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    expected = "Hello world!\nhola\n"

    assert result == expected


def test_walk_Parameter():
    model = """
    parameter a0 = 1 "This is a parameter"
    parameter a1 = 3, a2 
    parameter a3

    a3.value = 10

    parameter
        a4 = 1, a5
    end
    
    parameter a0.a1 = 10
    """

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    print(ast)
    print(result)

    result = walker.onemodel.root

    assert result["a0"]["value"] == 1
    assert result["a0"]["__doc__"] == "This is a parameter"
    assert result["a1"]["value"] == 3
    assert result["a2"]["value"] == 0
    assert result["a3"]["value"] == 10
    assert result["a4"]["value"] == 1
    assert result["a5"]["value"] == 0
    assert result["a0"]["a1"]["value"] == 10

def test_walk_AccessIdentifier():
    model = """
    parameter foo = 1
    foo
    """

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    print(ast)
    print(result)

    result = str(result[1])
    expected = walker.onemodel["foo"].__repr__()

    assert result == expected
