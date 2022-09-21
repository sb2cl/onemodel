import os
import pytest
from distutils.dir_util import copy_tree
from pathlib import Path

from onemodel.objects.module import Module
from onemodel.objects.module import find_module


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
