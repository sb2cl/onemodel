import os
import pytest
from distutils.dir_util import copy_tree
from pathlib import Path


from onemodel.package_manager import PackageManager

@pytest.fixture
def tmp_examples_dir(tmpdir):
    result = Path(tmpdir)
    copy_example_files_into(result)
    return result

def copy_example_files_into(path):
    path_test_module = os.path.dirname(__file__) + "/test_package_manager"
    copy_tree(path_test_module, str(path))

def test_init():
    pm = PackageManager()
    assert isinstance(pm, PackageManager)

def test_load_toml_file(tmp_examples_dir):
    os.chdir(tmp_examples_dir)

    pm = PackageManager()
    pm.load_toml_file()

    expected = {
        "onemodel-blueprint": "https://github.com/fernandonobel/onemodel-blueprint"
    }

    assert pm.dependencies == expected

