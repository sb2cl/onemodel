import os

import click
import tatsu

import onemodel
from onemodel.dsl.repl import Repl
from onemodel.dsl.onemodel_model import OneModelWalker

@click.group()
def cli():
    """ onemodel-cli (Command line interface for onemodel)

    Onemodel-cli reads the INPUT model file, which is defined with the onemodel
    syntax preferabily, and exports the model information into a file (or set of 
    files) for being executed in other programming language (i.e. MATLAB).
    """

@cli.command(short_help='Run REPL')
def repl():
    """ Run an interactive REPL (Read Evaluate Print Loop) session.

    """
    repl = Repl()
    repl.run()

@cli.command(short_help='Export the model')
@click.argument('input_file', 
        type=click.Path(exists=True))
@click.option('-o','--output', 
        type=click.Path(exists=True), 
        help="Set the output path for the exported model.")
def export(input_file, output):
    """ Export the INPUT_FILE model into an implementation of it in other language.

    By default the exported model will be saved in the 'build' directory of the
    current path (if 'build' dir doesn't exist, it will be created).
    """

    # Get the filename (without extension) and the extension.
    base = os.path.basename(input_file)
    (filename, extension) = os.path.splitext(base)

    # Default value of output is './build/'
    if output == None:
        output = './build/'

    output = os.path.abspath(output)

    # Check if output dir doesn't exists.
    if not os.path.isdir(output):
        print(f'Created output directory "{output}".')
        os.mkdir(output)
    
    # Load the grammar.
    grammar = open('/home/nobel/Sync/python/workspace/onemodel/src/onemodel/dsl/onemodel_model.ebnf').read()

    # Load the parser with the grammar.
    parser = tatsu.compile(grammar, asmodel=True)
    print('Parser initialized with "onemodel" syntax.')

    # Load the Semantic Model.
    walker = OneModelWalker(filename)
    print('Semantic model intialized for "onemodel" syntax.')

    # Parse the data into an AST model.
    model = parser.parse(open(input_file).read())
    print('Parsed input file into an AST model.')

    # Walk the AST model.
    result = walker.walk(model)
    print('Walk the AST model.')

    matlab = Matlab(walker.onemodel)


if __name__ == '__main__':
    cli(obj={})
