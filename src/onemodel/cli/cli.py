import os
import sys

import click
import tatsu

import onemodel
from onemodel.dsl.repl import Repl
from onemodel.dsl.onemodel_walker import OneModelWalker
from onemodel.dsl.context import Context
from sbml2dae.dae_model import DaeModel
from sbml2dae.matlab import Matlab

@click.group()
def cli():
    """ OneModel Command Line Interface (onemodel-cli).
    
    onemodel-cli is a command line interface for onemodel toolbox. You can
    define sythetic biology models using onemodel syntax and later on you can
    export an implementation of it in SBML or Matlab.
    """

@cli.command(short_help='Run an interactive onemodel session')
def repl():
    """ Run an interactive onemodel REPL (Read Evaluate Print Loop) session.
    """
    repl = Repl()
    repl.run()

@cli.command(short_help='Run a onemodel file')
@click.argument('input_file', 
        type=click.Path(exists=True))
def run(input_file):
    """ Run the INPUT_FILE with onemodel repl.
    """
    # Get the filename (without extension) and the extension.
    base = os.path.basename(input_file)
    (filename, extension) = os.path.splitext(base)

    # Read text from input_file.
    f = open(input_file)
    text = input_file.read()
    f.close()

    # Load the AST model walker.
    walker = OneModelWalker(filename)

    # Run.
    walker.run(text, input_file)

@cli.command(short_help='Export model')
@click.argument('input_file', 
        type=click.Path(exists=True))
@click.option('-o','--output', 
        type=click.Path(exists=True), 
        help="Set the output path to export files.")
@click.option('-f','--from-syntax', 
        type=click.Choice(['onemodel', 'sbml'], case_sensitive=False),
        help="Set the syntax for interpreting INPUT_FILE.")
@click.option('-t','--to-syntax', 
        type=click.Choice(['sbml', 'matlab'], case_sensitive=False),
        default='matlab',
        help="Set the syntax for exporting INPUT_FILE.")
def export(input_file, output, from_syntax, to_syntax):
    """ Export the INPUT_FILE model into an implementation of it in other language.

    By default, INPUT_FILE will be interpreted automatically based on its
    extension:

        \b
        .one -> onemodel syntax
        .xml -> SBML (Synthetic Biology Markup Language)

    By default, export output syntax will be Matlab.

    By default, the exported files will be saved in the 'build' directory of the
    current path (if 'build' dir doesn't exist, it will be created).
    """

    # Get the filename (without extension) and the extension.
    base = os.path.basename(input_file)
    (filename, extension) = os.path.splitext(base)

    # If from_syntax is not set.
    if from_syntax == None:
        # Automatically set from_syntax based on file extension.
        if extension == '.onemodel' or extension == '.one':
            from_syntax = 'onemodel'
        elif extension == '.xml':
            from_syntax = 'sbml'
        else:
            print(f'Error: File extension "{extension}" is not reconized.')
            print('Please use ".onemodel" or ".xml".')
            sys.exit()

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

    if from_syntax == 'onemodel' and to_syntax == 'matlab':
        sbml_filename = onemodel2sbml(input_file, filename, output)
        sbml2matlab(sbml_filename, output)

    elif from_syntax == 'onemodel' and to_syntax == 'sbml':
        sbml_filename = onemodel2sbml(input_file, filename, output)

    elif from_syntax == 'sbml' and to_syntax == 'matlab':
        sbml2matlab(input_file, output)

    else:
        print(f'Error: exporting from "{from_syntax}" to "{to_syntax}" in not supported.')
        sys.exit()

def onemodel2sbml(input_file, filename, output):
    """ Convert a onemodel file into sbml.
    """
    print('### Convert onemodel into sbml ###')


    # Read input file.
    file = open(input_file)
    text = file.read()
    file.close()
    print('\tRead input file.')

    # Load the AST model walker.
    walker = OneModelWalker(filename)
    print('\tOneModel interpreter initialized.')

    # Walk the AST model.
    result = walker.run(text, input_file)
    print('\tRun input_file.')

    # Get SBML representation.
    sbml = walker.getSBML()
    print('\tExport to SBML.')

    # Save SBML.
    sbml_filename = f'{output}/{filename}.xml' 
    f = open(sbml_filename, 'w')
    f.write(sbml)
    f.close()
    print(f'\tGenerated {sbml_filename}')

    return sbml_filename

def sbml2matlab(sbml_filename, output):
    """ Convert a sbml file into matlab.
    """
    print('### Convert sbml into matlab ###')

    # Generate dae model representaion.
    dae = DaeModel(sbml_filename)
    print('\tExtract DAE model from sbml model.') 

    # Export into matlab files.
    matlab = Matlab(dae, output)

    filepath = matlab.export_example()
    print(f'\tGenerated {filepath}')

    filepath = matlab.export_class()
    print(f'\tGenerated {filepath}')

def main():
    cli(obj={})

if __name__ == '__main__':
    main()
