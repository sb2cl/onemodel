%% ---------------------------------------------------------
%% Definition of the class Productivity.
%% ---------------------------------------------------------

class Productivity

  %% ---------------------------------------------------------
  %% Inputs.
  %% ---------------------------------------------------------

  variable F_out(
    units = 'L/min',
    comment = 'Output media flux',
    isPlot = false,
    isTex = false
    );

  variable N(
    units = 'cells/L',
    comment = 'Concentration of cells in the biorreactor.',
    isPlot = false,
    isTex = false
    );

  variable m_A(
    units = 'fg',
    comment = 'Protein mass invested as protein A in a cell.',
    isPlot = false,
    isTex = false
    );

  %% ---------------------------------------------------------
  %% Variables.
  %% ---------------------------------------------------------

  variable M_A(
    units = 'g',
    comment = 'Total mass of protein A removed from the bioreactor.',
    isTex = false,
    isPlot = false,
    title = '$M_A$'
    );

  equation der_M_A == F_out*m_A*N;

end Productivity;
