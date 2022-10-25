import os
import pytest
from distutils.dir_util import copy_tree
from pathlib import Path


from onemodel.package_manager import PackageManager
from onemodel.onemodel_walker import OneModelWalker, load_file

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
        "onemodel_blueprint": "https://github.com/fernandonobel/onemodel_blueprint"
    }

    assert pm.dependencies() == expected

def test_install_dependencies(tmp_examples_dir):
    os.chdir(tmp_examples_dir)

    pm = PackageManager()
    pm.load_toml_file()
    pm.install_dependencies()

    assert os.path.isdir("lib/onemodel_blueprint")
    assert os.path.isfile("lib/onemodel_blueprint/src/add.one")

def test_run(tmp_examples_dir):
    os.chdir(tmp_examples_dir)

    pm = PackageManager()
    pm.load_toml_file()
    pm.install_dependencies()

    walker = OneModelWalker()

    onemodel = load_file("src/main.one") 

    assert onemodel["onemodel_blueprint"]["add"]["add"] != None
