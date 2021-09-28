use ./model/wildType/proteinRibosomal.mc;
use ./model/wildType/proteinNonRibosomal.mc;

%% ---------------------------------------------------------
%% Definition of the class WildType.
%% ---------------------------------------------------------

class WildType

  ProteinRibosomal p_r;

  connect(p_r__nu, nu);
  connect(p_r__mu, mu);
  connect(p_r__r, r);
  connect(p_r__m_h, m_h);
  connect(p_r__J_host_sum, J_host_sum);

  ProteinNonRibosomal p_nr;

  connect(p_nr__nu, nu);
  connect(p_nr__mu, mu);
  connect(p_nr__r, r);
  connect(p_nr__m_h, m_h);
  connect(p_nr__J_host_sum, J_host_sum);

  %% ---------------------------------------------------------
  %% Input variables.
  %% ---------------------------------------------------------

  variable s(
    comment = 'Concentration of substrate in the biorreactor.',
    units = 'g \cdot L^{-1}'
    );

  variable m_h(
    units = 'fg \cdot cell^{-1}',
    comment = 'Total host protein mass.'
    );

  %% ---------------------------------------------------------
  %% Parameters. 
  %% ---------------------------------------------------------

  parameter K_s( 
    value = 0.1802,
    units = 'g \cdot L^{-1}',
    comment = 'Half activation threshold of growth rate.',
    reference = '\cite{Zhuang2013}'
    );

  parameter nu_max(
    value = 1260,
    units = 'aa \cdot min^{-1}',
    comment = 'Maximum effective translation rate per ribosome.',
    reference = '\cite{Milo2009}'
    );
 
  parameter m_aa(
    value = 182.6e-9,
    units = 'fg \cdot aa^{-1}',
    comment = 'Average aminoacid mass.',
    reference = '\cite{Sundararaj2004}'
  );

  parameter phi_t(
    value = 0.9473,
    units = 'adim',
    comment = 'Fraction of mature available ribosomes relative to the total.',
    reference = 'Optimized in \cite{nobel2020resources}.'
  ); 

  %% ---------------------------------------------------------
  %% General variables. 
  %% ---------------------------------------------------------

  variable nu(
    value = nu_max*s/(s+K_s),
    units = 'aa \cdot min^{-1}',
    comment = 'Effective translation rate per ribosome.'
    );
 
  variable mu(
    start = 0.01,
    units = 'min^{-1}',
    comment = 'Specific cell growth rate.'
    );
 
  variable m_p(
    value = p_r__m + p_nr__m,
    units = 'fg \cdot cell^{-1}',
    comment = 'Total protein mass calculated from the mass of individual proteins in the cell'
    );
  
  variable J_sum(
    value = p_r__N*p_r__J + p_nr__N*p_nr__J,
    units = 'adim',
    comment = 'Total sum of all the J in the cell.'
    );

  variable J_host_sum(
    value = p_r__N*p_r__J + p_nr__N*p_nr__J,
    units = 'adim',
    comment = 'Total sum of all the host J in the cell.'
    );

  variable J_sum_E(
    value = p_r__N*(1+1/p_r__E_m)*p_r__J + p_nr__N*(1+1/p_nr__E_m)*p_nr__J,
    units = 'adim',
    comment = 'Total sum of all the J in the cell taking into account E_m terms.'
    );
  
  variable phi_b_t(
    value = J_host_sum/(1+J_sum_E),
    units = 'adim',
    comment = 'Fraction of translating ribosomes of $\phi_t r_t(m_r)$.'
    );
  
  variable r(
    start = 350,
    units = 'molec \cdot cell^{-1}',
    comment = 'Free mature ribosomes in the cell.'
    );

  %% ---------------------------------------------------------
  %% Equations.
  %% ---------------------------------------------------------
  
  equation r == phi_t*p_r__r_t/(1+J_sum_E);
  equation mu == m_aa/m_h*nu*phi_b_t*phi_t*p_r__r_t;

end WildType;

%% ---------------------------------------------------------
%% Stand alone model.
%% ---------------------------------------------------------

parameter s(value = 3.6, isTex = false);
parameter m_h(value = 450, isTex = false);

WildType wt;

connect(wt__s, s);
connect(wt__m_h, m_h);
