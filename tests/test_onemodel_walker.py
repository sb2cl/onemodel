from onemodel.onemodel_walker import OneModelWalker
from onemodel.objects.parameter import Parameter
from onemodel.objects.species import Species
from onemodel.objects.reaction import Reaction
from onemodel.objects.assignment_rule import AssignmentRule
from onemodel.objects.algebraic_rule import AlgebraicRule
from onemodel.objects.rate_rule import RateRule
from onemodel.objects.model import Model

def test_init():
    result = OneModelWalker()

    assert isinstance(result, OneModelWalker)
    assert result.parser

def test_walk_Parameter():
    model = '''
    parameter a0 = 1 "This is a parameter"
    parameter a1 = 3, a2 

    parameter a3 
    """foo

    bar
    """

    a3.value = 10

    parameter
        a4 = 1, a5
    end
    
    parameter a0.a1 = 10
    '''

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
    assert result["a3"]["__doc__"] == "foo\n\nbar\n"
    assert result["a4"]["value"] == 1
    assert result["a5"]["value"] == 0
    assert result["a0"]["a1"]["value"] == 10

def test_walk_Species():
    model = '''
    species a0 = 1 
    """This is a species"""

    species
        a1=2
        a2=3
    end
    '''

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    print(ast)
    print(result)

    result = walker.onemodel.root

    assert isinstance(result["a0"], Species)
    assert result["a0"]["initialConcentration"] == 1
    assert result["a0"]["__doc__"] == "This is a species"
    assert result["a1"]["initialConcentration"] == 2
    assert result["a2"]["initialConcentration"] == 3

def test_walk_Reaction():
    model = '''
    reaction J1: foo.A + B -> C + D; k*foo.A*B
    reaction
        0 -> A; foo
        B -> A; foo*bar
    end
    '''

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    result = walker.onemodel.root

    assert isinstance(result["J1"], Reaction)
    assert result["J1"]["reactants"] == ["foo.A", "B"]
    assert result["J1"]["products"] == ["C", "D"]
    assert result["J1"]["kinetic_law"] == "k*foo.A*B"
    assert isinstance(result["_J0"], Reaction)
    assert isinstance(result["_J1"], Reaction)


def test_walk_AccessName():
    model = """
    parameter foo = 1
    foo
    parameter foo.bar = 10
    foo.bar 
    """

    walker = OneModelWalker()  
    result, ast = walker.run(model)

    print(ast)
    print(result)

    expected = walker.onemodel["foo"].__repr__()
    assert str(result[1]) == expected

    expected = walker.onemodel["foo"]["bar"].__repr__()
    assert str(result[3]) == expected


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
    1E+3
    """
    walker = OneModelWalker()  
    result, ast = walker.run(model)
    expected = [0.0, 1.0, 0.9, 1.5, 0.001, 1e2, 1e3, 1e-2, 1e3]
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

def test_walk_String():
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

def test_walk_Assignment_Rule():
    model = """
    rule bar := foo
    rule bar := foo
    rule R2: bar := 100 + foo^2
    rule
        a := b
        R3: c := a*a
    end
    """

    walker = OneModelWalker()

    result, ast = walker.run(model)

    result = walker.onemodel.root

    assert isinstance(result["_R0"], AssignmentRule)
    assert result["_R0"]["variable"] == "bar"
    assert result["_R0"]["math"] == "foo"

    assert isinstance(result["_R1"], AssignmentRule)
    assert result["_R1"]["variable"] == "bar"
    assert result["_R1"]["math"] == "foo"

    assert isinstance(result["R2"], AssignmentRule)
    assert result["R2"]["variable"] == "bar"
    assert result["R2"]["math"] == "100 + foo^2"

    assert isinstance(result["_R2"], AssignmentRule)
    assert result["_R2"]["variable"] == "a"
    assert result["_R2"]["math"] == "b"

    assert isinstance(result["R3"], AssignmentRule)
    assert result["R3"]["variable"] == "c"
    assert result["R3"]["math"] == "a*a"

def test_walk_Algebraic_Rule():
    model = """
    rule bar == foo
    rule bar == foo
    rule R2: bar == 100 + foo^2
    rule
        a == b
        R3: c == a*a
    end
    """

    walker = OneModelWalker()

    result, ast = walker.run(model)

    result = walker.onemodel.root

    assert isinstance(result["_R0"], AlgebraicRule)
    assert result["_R0"]["variable"] == "bar"
    assert result["_R0"]["math"] == "foo"

    assert isinstance(result["_R1"], AlgebraicRule)
    assert result["_R1"]["variable"] == "bar"
    assert result["_R1"]["math"] == "foo"

    assert isinstance(result["R2"], AlgebraicRule)
    assert result["R2"]["variable"] == "bar"
    assert result["R2"]["math"] == "100 + foo^2"

    assert isinstance(result["_R2"], AlgebraicRule)
    assert result["_R2"]["variable"] == "a"
    assert result["_R2"]["math"] == "b"

    assert isinstance(result["R3"], AlgebraicRule)
    assert result["R3"]["variable"] == "c"
    assert result["R3"]["math"] == "a*a"

def test_walk_Rate_Rule():
    model = """
    rule der(bar) := foo
    rule der(bar) := foo
    rule R2: der(bar) := 100 + foo^2
    rule
        der(a) := b
        R3: der(c) := a*a
    end
    """

    walker = OneModelWalker()

    result, ast = walker.run(model)

    result = walker.onemodel.root

    assert isinstance(result["_R0"], RateRule)
    assert result["_R0"]["variable"] == "bar"
    assert result["_R0"]["math"] == "foo"

    assert isinstance(result["_R1"], RateRule)
    assert result["_R1"]["variable"] == "bar"
    assert result["_R1"]["math"] == "foo"

    assert isinstance(result["R2"], RateRule)
    assert result["R2"]["variable"] == "bar"
    assert result["R2"]["math"] == "100 + foo^2"

    assert isinstance(result["_R2"], RateRule)
    assert result["_R2"]["variable"] == "a"
    assert result["_R2"]["math"] == "b"

    assert isinstance(result["R3"], RateRule)
    assert result["R3"]["variable"] == "c"
    assert result["R3"]["math"] == "a*a"

def test_walk_Call():
    model = """
    function increase( param )
      param.value = param.value + 1
    end

    parameter foo = 1
    increase(foo)
    foo.value
    """

    walker = OneModelWalker()

    result, ast = walker.run(model)

    assert result[-1] == 2

def test_walk_ModelDefinition():
    model = """
    model MyModel
        parameter foo = 10
        species bar = 0
        rule R1: der(bar) := foo - bar
    end

    m = MyModel()
    """

    walker = OneModelWalker()

    result, ast = walker.run(model)

    result = walker.onemodel.root
    
    assert isinstance(result["MyModel"], Model)
    assert result["m"]["foo"]["value"] == 10
    assert result["m"]["bar"]["initialConcentration"] == 0
    assert result["m"]["R1"]["math"] == "foo - bar"

def test_walk_Standalone():
    model = """
    standalone
        1
    end
    """
    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == 1

    model = """
    standalone
        1
    end
    """
    walker = OneModelWalker()
    walker.isImporting = True
    result, ast = walker.run(model)
    assert result == None
    
def test_walk_Addition():
    model = """
    1 + 2
    """

    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == 3

def test_walk_Subtraction():
    model = """
    1 - 2
    """

    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == -1

def test_walk_Multiplication():
    model = """
    2 * 3
    """

    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == 6

def test_walk_Division():
    model = """
    6 / 3
    """

    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == 2

def test_Factor():
    model = """
    +2
    -2
    """
    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == [2,-2]

def test_walk_Power():
    model = """
    2^3
    """
    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == 8

def test_walk_Parentheis():
    model = """
    6/(3+2)
    6+(3+9)
    """

    walker = OneModelWalker()
    result, ast = walker.run(model)
    assert result == [1.2,18]
