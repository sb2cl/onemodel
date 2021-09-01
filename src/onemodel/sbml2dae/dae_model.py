from enum import Enum, auto

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
        return 'Antithetic'

    def getParameters(self):
        """ Return a list with the constant parameters.
        """
        parameters = []

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

        for item in self.model.getListOfSpecies():
            state = {}
            state['id'] = item.id
            state['initialCondition'] = item.getInitialConcentration()
            state['type'] = StateType.ODE

            states.append(state)

        return states

    def getStatesDae(self):
        """ Return a list of the equation which evaluate each of the states.
        """
        dae = {}

        for state in self.getStatesId():
            dae[state] = ''

        for reaction in self.model.getListOfReactions():
            ast = reaction.getKineticLaw().math
            equation = formulaToL3String(ast)

            for state in self.getStatesId():
                for product in reaction.getListOfProducts():
                    if state == product.getSpecies():
                        dae[state] += equation
        return dae

if __name__ == '__main__':
    dae = DaeModel(
        '/home/nobel/Sync/python/workspace/onemodel/examples/antithetic.xml'
    )

    print(dae.getParameters())
    print(dae.getParameters()[0]['id'])
    print(dae.getParameters()[0]['value'])

    print()
    print(dae.getStates())
    print(dae.getStates()[0]['id'])
    print(dae.getStates()[0]['initialCondition'])

    # print(dae.getStatesId())
    # print(dae.getStatesInitialCondition())
    # print(dae.getStatesDae())
