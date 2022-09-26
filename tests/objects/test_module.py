import os
import pytest
from distutils.dir_util import copy_tree
from pathlib import Path

from onemodel.objects.module import Module
from onemodel.objects.module import find_module
from onemodel.objects.module import load_module
from onemodel.onemodel_walker import OneModelWalker


@pytest.fixture
def tmp_examples_dir(tmpdir):
    result = Path(tmpdir)
    copy_example_files_into(result)
    return result

def copy_example_files_into(path):
    copy_tree("./", str(path))

def test_init():
    result = Module()
    assert isinstance(result, Module)

def test_find_module(tmp_examples_dir):
    os.chdir(tmp_examples_dir)

    module_name = "ex01_simple_gene_expression"
    result = find_module(module_name)
    expected = tmp_examples_dir / "ex01_simple_gene_expression.one" 

    assert result == str(expected)

def test_load_module(tmp_examples_dir):
    os.chdir(tmp_examples_dir)
    walker = OneModelWalker()

    import_name = None
    module_name = "ex01_simple_gene_expression"
    assign_name = None

    result = load_module(
            walker,
            module_name, 
            import_name=import_name,
            assign_name=assign_name
            )

    assert isinstance(result, Module)
    assert result["__name__"] == module_name
    assert result["__file__"] == find_module(module_name)
    assert result["k_m"]["value"] == 1


