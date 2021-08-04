import os

class Matlab:
    """ This class exports a onemodel model into Matlab syntax.

    This class auto-generates Matlab code that implements the information in
    a onemodel model.

    Attributes:
        onemodel: OneModel
    """

    def __init__(self, onemodel):
        """ Inits Matlab.
        
        Args:
            onemodel: OneModel
                OneModel object to export into Matlab syntax.
        """
        self.onemodel = onemodel

    def generate_param(self):
        """ Generate Matlab function which returns the default parameters.
        
        """
        # Check if build folder exists
        dirName = './build/'
        if not os.path.exists(dirName):
            # Create it.
            os.mkdir(dirName)

        # Create and open the file to export.
        f = open(dirName + self.onemodel.name + '_param.m', "w")

        # Function header.
        f.write(f'function [p,x0,M] = {self.onemodel.name}_param()\n')
        f.write(f'% This script was generated with onemodel.\n\n')

        # Default parameters.
        f.write(f'% Default parameters value.\n')
        for par in self.onemodel.parameters:
            f.write(f'p.{par.name} = {par.value};\n')

        # Default initial conditions.
        f.write(f'\n% Default initial conditions.\n')
        f.write(f'x0 = [\n')
        for var in self.onemodel.variables:
            f.write(f'\t{var.value} % {var.name}\n')
        f.write(f'];\n')

        # Mass matrix.
        f.write(f'\n% Mass matrix for algebraic simulations.\n')
        f.write(f'M = [\n')
        i = 0
        i_max = len(self.onemodel.variables)
        while i < i_max:
            f.write('\t')
            f.write('0 '*i)
            # TODO: Write if the variable is algebraic o not.
            f.write('1 ')
            f.write('0 '*(i_max-i-1))
            f.write('\n')
            i += 1
        f.write(f'];\n')

        f.close()
