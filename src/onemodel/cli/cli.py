import os
import sys
from importlib_resources import files

import click
import tatsu

import onemodel
from onemodel.dsl.repl import Repl
from onemodel.dsl.onemodel_walker import OneModelWalker
from onemodel.dsl.tellurium_extended import algebraic2tellurium, tellurium2sbml

from onemodel.sbml2dae.dae_model import DaeModel
from onemodel.sbml2dae.matlab import Matlab

import tellurium as te
import roadrunner

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
        if extension == '.one':
            from_syntax = 'onemodel'
        elif extension == '.xml':
            from_syntax = 'sbml'
        else:
            print(f'Error: File extension "{extension}" is not reconized.')
            print('Please use ".one" or ".xml".')
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

    ## Load the grammar.
    #grammar = files('onemodel.dsl').joinpath('onemodel.ebnf').read_text()

    ## Load the parser with the grammar.
    #parser = tatsu.compile(grammar, asmodel=True)
    #print('\tParser initialized with "onemodel" syntax.')

    ## Parse the data into an AST model.
    #model = parser.parse(open(input_file).read())
    #print('\tParsed input file into an AST model.')

    ## Load the AST model walker.
    #walker = OneModelWalker(filename)
    #print('\tAST model walker initialized for "onemodel" syntax.')

    ## Walk the AST model.
    #result = walker.walk(model)
    #print('\tWalk the AST model.')

    ## Get SBML representation.
    #sbml = walker.getSBML()
    #print('\tExport SBML.')

    # Read file model.
    model_ext_str = open(input_file).read()

    # Convert from tellurium_extended into tellurium.
    model_str = algebraic2tellurium(model_ext_str)

    # Convert tellurium into sbml
    r = te.loada(model_str)
    sbml = r.getSBML()
    sbml = tellurium2sbml(sbml)

    # Convert form tellurium sbml into tellurium-extended sbml.
    sbml = tellurium2sbml(sbml)

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

    filepath = matlab.exportDefaultParameters()
    print(f'\tGenerated {filepath}')

    filepath = matlab.exportOde()
    print(f'\tGenerated {filepath}')

    filepath = matlab.exportStates()
    print(f'\tGenerated {filepath}')

    filepath = matlab.exportDriver()
    print(f'\tGenerated {filepath}')


if __name__ == '__main__':
    cli(obj={})
