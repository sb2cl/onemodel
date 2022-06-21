import os

import pytest
from onemodel.cli import cli
from sbml2dae.dae_model import DaeModel
from sbml2dae.matlab import Matlab

examples = [
    "ex01_simple_gene_expression",
    "ex02_two_genes_expression",
    "ex03_protein_constitutive",
    "ex04_two_genes_expression",
    "ex05_protein_induced",
    "ex06_antithetic_controller",
]


@pytest.mark.parametrize("example_name", examples)
def test_examples(tmpdir, example_name: str) -> None:
    """Test that the example SBML files are corretly exported into MATLAB."""

    examples_dir = os.path.dirname(os.path.abspath("README.md")) + "/examples/"

    cli.onemodel2sbml(
        examples_dir + example_name + ".one",
        example_name,
        str(tmpdir)
    )

    example_filepath = str(tmpdir) + "/" + example_name + ".xml"

    matlab = load_example(example_filepath, tmpdir)
    exported_files = export_files(matlab)

    assert exported_files == expected_files(examples_dir, example_name)


def load_example(example_filepath, output_dir):
    dae = DaeModel(example_filepath)
    matlab = Matlab(dae, output_dir)

    return matlab


def export_files(matlab):
    filepath = matlab.export_example()
    example_file = read_file_contents(filepath)

    filepath = matlab.export_class()
    class_file = read_file_contents(filepath)

    return [example_file, class_file]


def expected_files(examples_dir, example_name):
    filepath = examples_dir + example_name + "_example.m"
    example_file = read_file_contents(filepath)

    filepath = examples_dir + example_name + ".m"
    class_file = read_file_contents(filepath)

    return [example_file, class_file]


def read_file_contents(filepath):
    file = open(filepath, "r")
    result = file.read()
    file.close()

    return result
