from onemodel.objects.module import Module
from onemodel.objects.module import find_module

def test_init():
    result = Module()
    assert isinstance(result, Module)

def test_find_module():
    module_name = "ex01_simple_gene_expression"
    result = find_module(module_name)
    expected = "/home/nobel/Sync/projects/python/onemodel/examples/ex01_simple_gene_expression.one" 

    assert result == expected
