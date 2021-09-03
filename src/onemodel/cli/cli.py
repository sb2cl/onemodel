import os
import sys
from importlib_resources import files

import click
import tatsu

import onemodel
from onemodel.dsl.repl import Repl
from onemodel.dsl.onemodel_walker import OneModelWalker
from onemodel.export.matlab.matlab import Matlab

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

    ## Default value of output is './build/'
    #if output == None:
    #    output = './build'
    #
    ## Create build dir if it doesn't exist.
    #if not os.path.isdir(output):
    #    os.mkdir(output)
    #    print(f'Created dir "{output}"')

    #output = os.path.abspath(output)

    ## Check if output dir doesn't exists.
    #if not os.path.isdir(output):
    #    print(f'Created output directory "{output}".')
    #    os.mkdir(output)
    #
    ## Load the grammar.
    #grammar = files('onemodel.dsl').joinpath('onemodel.ebnf').read_text()

    ## Load the parser with the grammar.
    #parser = tatsu.compile(grammar, asmodel=True)
    #print('Parser initialized with "onemodel" syntax.')

    ## Parse the data into an AST model.
    #model = parser.parse(open(input_file).read())
    #print('Parsed input file into an AST model.')

    ## Load the AST model walker.
    #walker = OneModelWalker(filename, output)
    #print('AST model walker initialized for "onemodel" syntax.')

    ## Walk the AST model.
    #result = walker.walk(model)
    #print('Walk the AST model.')

    ## Get SBML representation.
    #sbml = walker.getSBML()
    #print('Export into SBML')

    ## Save file.
    #model_name = 'test'
    #filename = f'{output}/{model_name}.xml' 
    #f = open(filename, 'w')
    #f.write(sbml)
    #f.close()
    #print(f'Generated {filename}')



    ## Populate onemodel model.
    #walker.populate_model()
    #print('Populated OneModel model.')
    

    ## Export the model into Matlab.
    #matlab = Matlab(walker.onemodel)
    #print('Load MATLAB export module.')

    #filepath = matlab.generate_param()
    #print(f'Generated "{filepath}"')
    #filepath = matlab.generate_ode()
    #print(f'Generated "{filepath}"')
    #filepath = matlab.generate_driver()
    #print(f'Generated "{filepath}"')
    #filepath = matlab.generate_states()
    #print(f'Generated "{filepath}"')

if __name__ == '__main__':
    cli(obj={})

