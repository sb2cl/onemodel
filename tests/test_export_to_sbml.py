import os

import pytest
from onemodel.dsl.onemodel_walker import OneModelWalker

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

    result = onemodel2sbml(
        examples_dir + example_name + ".one",
        example_name
    )

    expected = read_file_contents(f"./examples/{example_name}.xml")

    assert result == expected

def onemodel2sbml(input_file, filename):
    """ Convert a onemodel file into sbml.
    """
    print('### Convert onemodel into sbml ###')


    # Read input file.
    file = open(input_file)
    text = file.read()
    file.close()

    # Load the AST model walker.
    walker = OneModelWalker(filename)

    # Walk the AST model.
    result = walker.run(text, input_file)

    # Get SBML representation.
    sbml = walker.getSBML()

    return sbml

def read_file_contents(filepath):
    file = open(filepath, "r")
    result = file.read()
    file.close()

    return result
