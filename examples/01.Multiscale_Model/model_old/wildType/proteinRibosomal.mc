use ./model/wildType/protein.mc;

%% ---------------------------------------------------------
%% Definition of ProteinRibosomal class.
%% ---------------------------------------------------------

class ProteinRibosomal

  extends Protein;

  %% ---------------------------------------------------------
  %% Initialize the values of Protein Class.
  %% ---------------------------------------------------------
 
  N.value         = 55;
  N.reference     = 'Estimated in \cite{nobel2020resources}.';

  omega.value     = 7.33;
  omega.reference = 'Optimized in \cite{nobel2020resources}.';

  d_m.value       = 0.16;
  d_m.reference   = 'Calculated from \cite{Hausser2019}';

  k_b.value       = 4.7627;
  k_u.reference   = 'Optimized in \cite{nobel2020resources}.';

  k_u.value       = 119.7956;
  k_u.reference   = 'Optimized in \cite{nobel2020resources}.';

  l_p.value       = 195;
  d_m.reference   = 'Calculated from \cite{Hausser2019}';

  E_m_eq.eqn      = 'E_m == 3.459';

  %% ---------------------------------------------------------
  %% Parameters.
  %% ---------------------------------------------------------
 
  parameter ribosomeWeight(
    %value = m_r/(N_r*lp_r*m_aa), % Esto da 0.002 fg cuando con los datos de Bremer debería ser 0.0045 fg.
    value = 0.0045,
    units = 'fg',
    comment = 'Weight of a ribosome.',
    reference = '\cite{Bremer:2008}'
  );
   
  %% ---------------------------------------------------------
  %% Variables.
  %% ---------------------------------------------------------

  variable r_t(
    value = m/ribosomeWeight,
    units = 'molec \cdot cell^{-1}',
    comment = 'Number of mature and inmmature ribosomes.'
    );

end ProteinRibosomal;

%% ---------------------------------------------------------
%% Stand-alone model.
%% ---------------------------------------------------------

ProteinRibosomal p_r;
 
connect(p_r__nu, 1);
connect(p_r__mu, 1);
connect(p_r__r, 1);
connect(p_r__m_h, 1);
connect(p_r__J_host_sum, 1);
