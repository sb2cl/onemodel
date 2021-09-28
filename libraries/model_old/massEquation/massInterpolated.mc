%% ---------------------------------------------------------
%% Definition of the class MassInterpolated.
%% ---------------------------------------------------------

class MassInterpolated

  %% ---------------------------------------------------------
  %% Input variables.
  %% ---------------------------------------------------------

  variable mu(
    units = '1/min',
    comment = 'Growth rate.',
    isPlot = false,
    isTex = false
    );
 
  %% ---------------------------------------------------------
  %% Parameters and variables of the model.
  %% ---------------------------------------------------------

  parameter c_1(
    value = 239089,
    units = 'fg \cdot cell^{-1} \cdot min^2',
    comment = 'First coefficient of mass equation.',
    nameTex = 'c_1',
    reference = '\cite{nobel2020resources}*'
    );

  parameter c_2(
    value = 7432,
    units = 'fg \cdot cell^{-1} \cdot min',
    comment = 'Second coefficient of mass equation.',
    nameTex = 'c_2',
    reference = '\cite{nobel2020resources}*'
    );

  parameter c_3(
    value = 37.06,
    units = 'fg \cdot cell^{-1}',
    comment = 'Third coefficient of mass equation.',
    nameTex = 'c_3',
    reference = '\cite{nobel2020resources}*'
    );

  variable m_p(
    units = 'fg \cdot cell^{-1}',
    comment = 'Total protein mass of the cell.',
    isPlot = false,
    nameTex = 'm_p(\mu)',
    %equationTex = 'm_p = 18.41 ((\mu - 0.01756)/0.008775)^2 + 138.9 (\mu - 0.01756)/0.008775 + 241.3'
    equationTex = 'm_p(\mu) = c_1 \mu^2 + c_2 \mu + c_3',
    isSubstitution = true
    );
 
  %% ---------------------------------------------------------
  %% Equations.
  %% ---------------------------------------------------------
  
  equation (m_p == c_1*mu*mu + c_2*mu + c_3, isSubstitution = true);

end MassInterpolated;
