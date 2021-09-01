from libsbml import *

class Sbml2Dae:
    """ Takes a SBML model as input and returns the data for defining a dae model.
    """
    def __init__(self, filename):
        """ Intialize Sbml2Dae.
        
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

    def getConstantParameters(self):
        """ Return a list with the constant parameters.
        """
        parameters = []

        for item in self.model.getListOfParameters():
            if item.getConstant() == True:
                parameters.append(item)
            
        return parameters

    def getConstantParametersId(self):
        """ Return a list with the identifier of constant parameters.
        """
        ids = []

        for item in self.getConstantParameters():
            ids.append(item.id)

        return ids

    def getConstantParametersValue(self):
        """ Return a list with the value of constant parameters.
        """
        values = []

        for item in self.getConstantParameters():
            values.append(item.value)

        return values

    def getStates(self):
        """ Return a list with the states of the model.
        """
        states = []

        for item in self.model.getListOfSpecies():
            states.append(item)

        return states

    def getStatesId(self):
        """ Return a list with the id of the states.
        """
        ids = []

        for item in self.getStates():
            ids.append(item.id)

        return ids

    def getStatesInitialCondition(self):
        """ Return a list with the initial condition of the states.
        """
        initials = []

        for item in self.getStates():
            initials.append(item.getInitialConcentration())

        return initials

if __name__ == '__main__':
    dae = Sbml2Dae(
        '/home/nobel/Sync/python/workspace/onemodel/examples/antithetic.xml'
    )

    print(dae.getConstantParameters())
    print(dae.getConstantParametersId())
    print(dae.getConstantParametersValue())

    print()
    print(dae.getStates())
    print(dae.getStatesId())
    print(dae.getStatesInitialCondition())


