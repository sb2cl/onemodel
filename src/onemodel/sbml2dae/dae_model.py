from enum import Enum, auto
from math import isnan

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
            state['type'] = StateType.ODE
            state['equation'] = ''
            state['ind'] = i

            # When the initial condition is not defined, it returns nan.
            # Check if initial condition is nan.
            if isnan(state['initialCondition']):
                # If so, set default initial condition to zero.
                state['initialCondition'] = 0

            states.append(state)
            i += 1

        # Assign equation property.
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

        # Check if a state has an empty equation.
        for item in states:
            if item['equation'] == '':
                # Set the state constant.
                item['equation'] = '0'

        return states

if __name__ == '__main__':
    dae = DaeModel(
        '/home/nobel/Sync/python/workspace/onemodel/examples/sbml/example_00.xml'
    )
    print(dae.getModelName())

    print(dae.getParameters())
    print(dae.getParameters()[0]['id'])
    print(dae.getParameters()[0]['value'])

    print()
    print(dae.getStates())
    print(dae.getStates()[0]['id'])
    print(dae.getStates()[0]['initialCondition'])
