%% ---------------------------------------------------------
%% Definition of the class MassInterpolated.
%% ---------------------------------------------------------

class MassEqJesus

  %% ---------------------------------------------------------
  %% Input variables.
  %% ---------------------------------------------------------

  variable mu(
    units = '1/min',
    comment = 'Growth rate.',
    isPlot = false
    );
 
  %% ---------------------------------------------------------
  %% Parameters and variables of the model.
  %% ---------------------------------------------------------

  parameter mp_mp0(
    value = 77.3748,
    units = 'g'
    );
  
  parameter mp_beta(
    value = 61.7813,
    units = 'min'
    );

  variable m_p(
    units = 'fg',
    comment = 'Total protein mass of the cell.',
    isPlot = false
    );
 
  %% ---------------------------------------------------------
  %% Equations.
  %% ---------------------------------------------------------
  

  equation (m_p == mp_mp0*exp(mp_beta*mu), isSubstitution = true);

end MassEqJesus;
