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
        self.onemodel.check()

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
        f.write(f'% This script was autogenerated with onemodel.\n\n')

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

        f.write(f'\nend\n')

        f.close()

    def generate_ode(self):
        """ Generate a Matlab function which evaluates the ODE.

        """
        # Check if build folder exists
        dirName = './build/'
        if not os.path.exists(dirName):
            # Create it.
            os.mkdir(dirName)

        # Create and open the file to export.
        f = open(dirName + self.onemodel.name + '_ode.m', "w")

        # Function header.
        f.write(f'function [dx] = {self.onemodel.name}_ode(t,x,p)\n')
        f.write(f'% This function was autogenerated with onemodel.\n')

        # Comment arguments.
        f.write(f'\n% Args:\n')
        f.write(f'%\t t Current time in the simulation.\n')
        f.write(f'%\t x Array with the state value.\n')
        f.write(f'%\t p Struct with the parameters.\n')

        # Comment return.
        f.write(f'\n% Return:\n')
        f.write(f'%\t dx Array with the ODE.\n')

        # Comment states.
        f.write(f'\n% States:\n')
        vars_ = self.onemodel.variables
        i = 0
        while i < len(vars_):
            # TODO: indicate if var is algebraic or not.
            f.write(f'{vars_[i].name} = x({i+1},:);\t % {vars_[i].comment}\n')
            i += 1

        # Comment parameters.
        f.write(f'\n% Parameters.\n')
        for par in self.onemodel.parameters:
            f.write(f'{par.name} = p.{par.name};\t % {par.comment}\n')
       
        # Generate ODE equations.
        f.write(f'\n')
        i = 0
        while i < len(vars_):
            f.write(f'% der({vars_[i].name}) "{vars_[i].equation.comment}"\n')
            f.write(f'dx({i+1},1) = {vars_[i].equation.value};\n\n')
            i += 1

        f.write(f'end\n')
        f.close()

    def generate_states(self):
        """ Generate a function which calculates all the states of the model.
        
        Generate a function which calculates all the states of the model from
        the simulation result. When simulating not all states are simulated, it
        is just simulated the reduced model. Then after the simulation we have
        to recalculate the rest of the states.
        """
         # Check if build folder exists
        dirName = './build/'
        if not os.path.exists(dirName):
            # Create it.
            os.mkdir(dirName)

        # Create and open the file to export.
        f = open(dirName + self.onemodel.name + '_states.m', "w")

        # Function header.
        f.write(f'function [out] = {self.onemodel.name}_states(t,x,p)\n')
        f.write(f'% This function was autogenerated with onemodel.\n')

        # Save the time.
        f.write(f'\n% Save simulation time.\n')
        f.write(f'out.t = t;\n')

        # Save ODE variables.
        f.write(f'\n% Save ODE variables.\n')
        i = 0
        vars_ = self.onemodel.variables
        while i < len(vars_):
            f.write(f'out.{vars_[i].name} = x(:,{i+1}); % {vars_[i].comment}\n')
            i += 1

        # Save parameters.
        f.write(f'\n% Save parameters.\n')
        for param in self.onemodel.parameters:
            f.write(f'out.{param.name} = p.{param.name}*ones(size(t)); % {param.comment}\n')

        f.write(f'\nend\n')
        f.close()

    def generate_driver(self):
        """ Generate an example driver script.
        
        Generate an example driver script taht will call all the generated
        functions and will perform a basic simulation of the model and plot the
        result.
        """
        # Check if build folder exists
        dirName = './build/'
        if not os.path.exists(dirName):
            # Create it.
            os.mkdir(dirName)

        # Create and open the file to export.
        f = open(dirName + self.onemodel.name + '_driver.m', "w")

        # Function header.
        f.write(f'%% Example driver script for simulating "{self.onemodel.name}" model.\n')
        f.write(f'% This sript was autogenerated with onemodel.\n')

        # Clear and close all.
        f.write(f'\nclear all;\n')
        f.write(f'close all;\n')

        # Default parameters.
        f.write(f'\n% Default parameters.\n')
        f.write(f'[p,x0,M] = {self.onemodel.name}_param();\n')

        # Solver options.
        f.write(f'\n% Solver options.\n')
        f.write(f"opt = odeset('AbsTol',1e-8,'RelTol',1e-8);\n")
        f.write(f"opt = odeset(opt,'Mass',M);\n")

        # Simulation time span.
        f.write(f'\n% Simulation time span.\n')
        f.write(f'tspan = [0 10];\n')

        # Simulate.
        f.write(f'\n[t,x] = ode15s(@(t,x) {self.onemodel.name}_ode(t,x,p),tspan,x0,opt);\n')
        f.write(f'out = {self.onemodel.name}_states(t,x,p);\n')
        
        # Plot.
        f.write(f'\n% Plot result.\n')
        f.write(f'plot(t,x);\n')
        f.write(f'grid on;\n')
        # TODO: Add a legend.
