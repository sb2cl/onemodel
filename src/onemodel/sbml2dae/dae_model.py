from enum import Enum, auto
from math import isnan
import re

from libsbml import *

class StateType(Enum):
    """ Enum for the different states types.
    """
    ODE = auto()
    ALGEBRAIC = auto()
    ASSIGMENT = auto()
    UNKOWN = auto()

    def __repr__(self):
        return self.name

class DefinitionType(Enum):
    """ Enum for the different ways a state can be defined.
    """
    # Only reactions define the equation of the state.
    REACTION = auto()
    # Reactions or rules can define the equation of the state, but no both.
    REACTION_OR_RULE = auto()
    # Only rules define the equation of the state.
    RULE = auto()

    def __repr__(self):
        return self.name

class DaeModel:
    """ Takes a SBML model as input and creates a DAE model.
    """
    def __init__(self, filename):
        """ Intialize DaeModel.
        
        Args:
            filename: srt
                Path to the SBML model file.
        """
        self.filename = filename
        self.reader = SBMLReader()
        self.document = self.reader.readSBML(self.filename)

        if self.document.getNumErrors():
            print('SBML model has the following errors:')
            self.document.printErrors()
            exit()

        self.model = self.document.getModel()

    def getModelName(self):
        """ Return the SBML model name.
        """
        return self.model.getId()

    def getParameters(self):
        """ Return a list with the constant parameters.
        """
        parameters = []

        # Assign properties.
        for item in self.model.getListOfParameters():
            # Skip not constant parameters.
            if item.getConstant() == False: continue

            # Skip dunder parameters.
            if item.id.startswith('__') == True: continue

            parameter = {}
            parameter['id'] = item.id
            parameter['value'] = item.value

            parameters.append(parameter)
            
        return parameters

    def getStates(self):
        """ Return a list with the states of the model.
        """
        states = []

        # Get species that can be a state.
        i = 0
        for species in self.model.getListOfSpecies():
            state = {}
            state['id'] = species.id
            ind = species.id.rfind('__')
            if ind > 0:
                state['context'] = species.id[0:ind]
            else:
                state['context'] = ''
            state['initialCondition'] = species.getInitialConcentration()
            state['type'] = StateType.UNKOWN

            constant = species.getConstant()
            boundary = species.getBoundaryCondition()

            if constant == False and boundary == False:
                state['definitionType'] = DefinitionType.REACTION_OR_RULE
                state['type'] = StateType.ODE

            elif constant == False and boundary == True:
                state['definitionType'] = DefinitionType.RULE

            state['equation'] = ''
            state['ind'] = i

            # When the initial condition is not defined, it returns nan.
            # Check if initial condition is nan.
            if isnan(state['initialCondition']):
                # If so, set default initial condition to zero.
                state['initialCondition'] = 0

            states.append(state)
            i += 1

        # Get parameters that are states (parameters that change over time).
        for parameter in self.model.getListOfParameters():
            # Skip constant parameters.
            if parameter.getConstant() == True: continue

            state = {}
            state['id'] = parameter.id
            ind = paremeter.id.rfind('__')
            if ind > 0:
                state['context'] = paremeter.id[0:ind]
            else:
                state['context'] = ''
            state['initialCondition'] = parameter.getValue()
            state['type'] = StateType.UNKOWN
            state['definitionType'] = DefinitionType.RULE
            state['equation'] = ''
            state['ind'] = i

            # When the initial condition is not defined, it returns nan.
            # Check if initial condition is nan.
            if isnan(state['initialCondition']):
                # If so, set default initial condition to zero.
                state['initialCondition'] = 0

            states.append(state)
            i += 1

        # Assign equation property from reactions.
        for reaction in self.model.getListOfReactions():
            ast = reaction.getKineticLaw().getMath()
            equation = formulaToL3String(ast)

            for state in states:
                # Skip states that only are defined by rules.
                if state['definitionType'] == DefinitionType.RULE:
                    continue

                for product in reaction.getListOfProducts():
                    if state['id'] == product.getSpecies():
                        state['equation'] += '+ (' + equation + ')'
                            
                        # Once the species is found in a reacion.
                        if state['definitionType'] == DefinitionType.REACTION_OR_RULE:
                            # Set the species to be only defined by reactions.
                            state['definitionType'] = DefinitionType.REACTION

                for reactant in reaction.getListOfReactants():
                    if state['id'] == reactant.getSpecies():
                        state['equation'] += '- (' + equation + ')'

                        # Once the species is found in a reacion.
                        if state['definitionType'] == DefinitionType.REACTION_OR_RULE:
                            # Set the species to be only defined by reactions.
                            state['definitionType'] = DefinitionType.REACTION


        # Assign equation to algebraic states:
        for state in states:
            # All reactions are set, so states can only be defined now by rules.
            if state['definitionType'] == DefinitionType.REACTION_OR_RULE:
                state['definitionType'] = DefinitionType.RULE

            # Skip not rule definiton states..
            if state['definitionType'] != DefinitionType.RULE: 
                continue

            # Check all algebraic rules.
            for rule in self.model.getListOfRules():
                # Algebraic rules.
                if rule.isAlgebraic():
                
                    ast = rule.getMath()
                    equation = formulaToL3String(ast)

                    # Get the first variable of the equation.
                    p = re.compile('((?!\d)\w+)')
                    m = p.search(equation)
                    
                    # Check if the first variable match the state id.
                    if state['id'] == m.groups()[0]:
                        # Then, it is the equation of this state.
                        state['equation'] = equation
                        state['type'] = StateType.ALGEBRAIC

                # Rate rules. 
                if rule.isRate():
                    # Check if the state is the variable of the rate rule.
                    if state['id'] == rule.getVariable():

                        ast = rule.getMath()
                        equation = formulaToL3String(ast)

                        state['equation'] = equation
                        state['type'] = StateType.ODE

                # Assigment rules.
                if rule.isAssignment():
                    # Check if the state is the variable of the rate rule.
                    if state['id'] == rule.getVariable():
                        ast = rule.getMath()
                        equation = formulaToL3String(ast)

                        state['equation'] = equation
                        state['type'] = StateType.ASSIGMENT

        # Check if a state has an empty equation.
        for item in states:
            if item['equation'] == '':
                # Set the state constant.
                item['equation'] = '0'

        return states

    def getOptions(self):
        """ Return a list with the simulatior options.
        """
        options = {}

        # Default options value.
        options['t_end']  = 10.0
        options['t_init'] = 0.0

        # Assign properties.
        for item in self.model.getListOfParameters():
            # Skip non-dunder parameters.
            if item.id.startswith('__') == False: continue

            options[item.id[2:]] = item.value

        return options

if __name__ == '__main__':
    dae = DaeModel(
        '/home/nobel/Sync/python/workspace/onemodel/libraries/multiscale/build/continous.xml'
    )

    print(dae.getModelName())

    print('### PARAMETERS ###')
    for item in dae.getParameters():
        print(item)

    print()
    print('### STATES ###')
    for item in dae.getStates():
        print(item)
