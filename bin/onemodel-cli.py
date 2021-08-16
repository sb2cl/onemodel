import os

import click
import tatsu

import onemodel
from onemodel.dsl.repl import Repl
from onemodel.dsl.onemodel_model import OneModelWalker
from onemodel.export.matlab.matlab import Matlab

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
        output = './build'
    
    # Create build dir if it doesn't exist.
    if not os.path.isdir(output):
        os.mkdir(output)
        print(f'Created dir "{output}"')

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

    # Parse the data into an AST model.
    model = parser.parse(open(input_file).read())
    print('Parsed input file into an AST model.')

    # Load the AST model walker.
    walker = OneModelWalker(filename, output)
    print('AST model walker initialized for "onemodel" syntax.')

    # Walk the AST model.
    result = walker.walk(model)
    print('Walk the AST model.')

    # Expor the model into Matlab.
    matlab = Matlab(walker.onemodel)
    print('Load MATLAB export module.')

    filepath = matlab.generate_param()
    print(f'Generated "{filepath}"')
    filepath = matlab.generate_ode()
    print(f'Generated "{filepath}"')
    filepath = matlab.generate_driver()
    print(f'Generated "{filepath}"')
    filepath = matlab.generate_states()
    print(f'Generated "{filepath}"')

if __name__ == '__main__':
    cli(obj={})
