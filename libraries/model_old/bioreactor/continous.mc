use ./model/bioreactor/bioreactor.mc;

%% ---------------------------------------------------------
%% Definition of the class Continous.
%% ---------------------------------------------------------

class Continous
  
  extends Bioreactor;

  parameter x_ref(
    comment = 'Desired biomass concentration.',
    units = 'g L^-1',
    value = 1
    );

  parameter V_final(
    comment = 'Final total desired volume we want to use.',
    units = 'L',
    value = 10
    );

  variable D(
    comment = 'Dilution rate.',
    units = 'adim',
    start = 0.0,
    isPlot = false
    );

  equation D == mu*x/x_ref;

  % Set input and output flow to dilution rate.
  connect(F_in, D*V * (1 - heaviside(V+V_feed - V_final)));
  connect(F_out, D*V * (1 - heaviside(V+V_feed - V_final)));

end Continous;
