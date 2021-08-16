import click
import os

import onemodel

from onemodel.dsl.repl import Repl


@click.group()
def cli():
    """ onemodel-cli (Command line interface for onemodel)

    Onemodel-cli reads the INPUT model file, which is defined with the onemodel
    syntax preferabily, and exports the model information into a file (or set of 
    files) for being executed in other programming language (i.e. MATLAB).
    """

@cli.command(short_help='Run REPL')
def repl():
    """ Run an interactive REPL (Read Evaluate Print Loop)

    """
    repl = Repl()
    repl.run()

@cli.command(short_help='Export the model')
@click.argument('input_file', type=click.File('r'))
@click.option('-o','--output', 
        type=click.Path(exists=True), 
        help="Set the output path for the exported model.")
def export(input_file, output):
    """ Export the INPUT_FILE model into an implementation of it in other language.

    By default the exported model will be saved in the 'build' directory of the
    current path (if 'build' dir doesn't exist, it will be created).
    """

    # Default value of output is './build/'
    if output == None:
        output = './build/'

    output = os.path.abspath(output)

    # Check if output dir doesn't exists.
    if not os.path.isdir(output):
        print(f'Created output directory "{output}".')
        os.mkdir(output)
    

    print(input_file)
    print(output)



if __name__ == '__main__':
    cli(obj={})
