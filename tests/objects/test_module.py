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
    path_test_module = os.path.dirname(__file__) + "/test_module"
    copy_tree(path_test_module, str(path))

def test_init():
    result = Module()
    assert isinstance(result, Module)

def test_find_module_1(tmp_examples_dir):
    os.chdir(tmp_examples_dir / "src")

    module_name = "module_1"
    result = find_module(module_name)
    expected = tmp_examples_dir / "src/module_1.one" 

    assert result == str(expected)

def test_find_module_2(tmp_examples_dir):
    os.chdir(tmp_examples_dir)

    module_name = "module_1"
    result = find_module(module_name)
    expected = tmp_examples_dir / "src/module_1.one" 

    assert result == str(expected)

def test_load_module_1(tmp_examples_dir):
    os.chdir(tmp_examples_dir / "src")
    walker = OneModelWalker()

    module_name = "module_1"
    import_name = None
    assign_name = None

    result = load_module(
            walker,
            module_name, 
            import_name,
            assign_name
            )

    assert isinstance(result, Module)
    assert result["__name__"] == module_name
    assert result["__file__"] == find_module(module_name)
    assert result["add"]["argument_names"] == ['a', 'b']
    assert walker.onemodel[module_name] == result  

def test_load_module_2(tmp_examples_dir):
    os.chdir(tmp_examples_dir / "src")
    walker = OneModelWalker()

    module_name = "module_1"
    import_name = None
    assign_name = "foo"

    result = load_module(
            walker,
            module_name, 
            import_name,
            assign_name
            )

    assert walker.onemodel[assign_name] == result

def test_load_module_3(tmp_examples_dir):
    os.chdir(tmp_examples_dir / "src")
    walker = OneModelWalker()

    module_name = "module_1"
    import_name = "add"
    assign_name = "foo"

    result = load_module(
            walker,
            module_name, 
            import_name,
            assign_name
            )

    assert walker.onemodel[assign_name] == result[import_name]

def test_load_module_4(tmp_examples_dir):
    os.chdir(tmp_examples_dir / "src")
    walker = OneModelWalker()

    module_name = "module_1"
    import_name = "add"
    assign_name = None

    result = load_module(
            walker,
            module_name, 
            import_name,
            assign_name
            )

    assert walker.onemodel[import_name] == result[import_name]
