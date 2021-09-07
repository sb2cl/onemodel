from enum import Enum, auto
from math import isnan
import re

from libsbml import *

class StateType(Enum):
    """ Enum for the different states types.
    """
    ODE = auto()
    ALGEBRAIC = auto()

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
        return 'model'
        return self.model.getId()

    def getParameters(self):
        """ Return a list with the constant parameters.
        """
        parameters = []

        # Assign properties.
        for item in self.model.getListOfParameters():
            if item.getConstant() == True:
                parameter = {}
                parameter['id'] = item.id
                parameter['value'] = item.value

                parameters.append(parameter)
            
        return parameters

    def getStates(self):
        """ Return a list with the states of the model.
        """
        states = []

        # Assign properties.
        i = 0
        for item in self.model.getListOfSpecies():
            state = {}
            state['id'] = item.id
            state['initialCondition'] = item.getInitialConcentration()

            constant = item.getConstant()
            boundary = item.getBoundaryCondition()
            if constant == False and boundary == False:
                state['type'] = StateType.ODE
            elif constant == False and boundary == True:
                state['type'] = StateType.ALGEBRAIC

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

                for product in reaction.getListOfProducts():
                    if state['id'] == product.getSpecies():
                        state['equation'] += '+ (' + equation + ')'

                for reactant in reaction.getListOfReactants():
                    if state['id'] == reactant.getSpecies():
                        state['equation'] += '- (' + equation + ')'

        # Assign equation to algebraic states:
        for state in states:
            # Skip non algebraic states.
            if state['type'] != StateType.ALGEBRAIC: continue

            # Check all algebraic rules.
            for rule in self.model.getListOfRules():
                # Skip not algebraic rules.
                if not rule.isAlgebraic(): continue
                
                ast = rule.getMath()
                equation = formulaToL3String(ast)

                # Get the first variable of the equation.
                p = re.compile('((?!\d)\w+)')
                m = p.search(equation)
                
                # Check if the first variable match the state id.
                if state['id'] == m.groups()[0]:
                    # Then, it is the equation of this state.
                    state['equation'] = equation

        # Check if a state has an empty equation.
        for item in states:
            if item['equation'] == '':
                # Set the state constant.
                item['equation'] = '0'

        return states

if __name__ == '__main__':
    dae = DaeModel(
        '/home/nobel/Sync/python/workspace/onemodel/examples/model.xml'
    )

    print(dae.getModelName())

    print('### PARAMETERS ###')
    for item in dae.getParameters():
        print(item)

    print()
    print('### STATES ###')
    for item in dae.getStates():
        print(item)
