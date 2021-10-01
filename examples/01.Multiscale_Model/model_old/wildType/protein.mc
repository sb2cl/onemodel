%% ---------------------------------------------------------
%% Definition of the class Protein.
%% ---------------------------------------------------------

class Protein

  %% ---------------------------------------------------------
  %% Input variables.
  %% ---------------------------------------------------------

  variable nu(
    units = 'aa \cdot min^{-1}',
    comment = 'Effective translation rate per risobome.'
    );

  variable mu(
    units = 'min^{-1}',
    comment = 'Specific growth rate.'
    );

  variable r(
    units = 'molec \cdot cell^{-1}',
    comment = 'Free mature ribosomes in the cell.'
    );

  variable m_h(
    units = 'fg \cdot cell^{-1}',
    comment = 'Total protein mass of host genes.'
    );

  variable J_host_sum(
    units = 'adim',
    comment = 'Total sum of all the host J.'
    );

  %% ---------------------------------------------------------
  %% Parameters.
  %% ---------------------------------------------------------

  parameter N(
    units = 'adim',
    comment = 'Number of copies of the gene.'
  );

  parameter omega(
    units = 'molec \cdot min^{-1} \cdot cell^{-1}',
    comment = 'Promoter transcription rate.'
  );

  parameter d_m(
    units = 'min^{-1}',
    comment = 'Mean degradation rate of mRNA.'
  );

  parameter k_b(
    range = [3 15],
    units = 'cell \cdot min^{-1} \cdot molec^{-1}',
    comment = 'Association rate RBS-ribosome.'
  );

  parameter k_u(
    range = [6 135],
    units = 'min^{-1}',
    comment = 'Dissotiation rate RBS-ribosome.'
  );

  parameter l_p(
    units = 'aa',
    comment = 'Protein length.'
  );

  parameter l_e(
    value = 25,
    units = 'aa',
    comment = 'Ribosome occupancy length.',
    reference = 'estimated \cite{Fernandes2017,Eriksen2017,Picard2013,Siwiak2013}'
  );

  %% ---------------------------------------------------------
  %% Variables.
  %% ---------------------------------------------------------
 
  variable K_C0(
    value = k_b/(k_u+nu/l_e),
    units = 'cell \cdot molec^{-1}',
    comment = 'Effective RBS affinity.'
    );

  variable E_m(
    value = 0.62*l_p/l_e,
    units = 'adim',
    comment = 'Ribosomes density related term.'
    );
 
  variable J(
    value = E_m*omega/(d_m/K_C0+mu*r),
    units = 'adim',
    comment = 'Resources recruitment strength.'
    );

  variable m(
    start = 100,
    units = 'fg \cdot cell^{-1}',
    comment = 'Total mass of this protein in the cell.'
  );

  %% ---------------------------------------------------------
  %% Variables.
  %% ---------------------------------------------------------
 
  equation der_m == (m_h*N*J/J_host_sum - m)*mu;

end Protein;
