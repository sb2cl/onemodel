use ./model/wildType/protein.mc;

%% ---------------------------------------------------------
%% Definition of ProteinNonRibosomal class.
%% ---------------------------------------------------------

class ProteinNonRibosomal

  extends Protein;

  %% ---------------------------------------------------------
  %% Initialize the values of Protein Class.
  %% ---------------------------------------------------------
 
  N.value         = 1735;
  N.reference     = 'Estimated in \cite{nobel2020resources}.';

  omega.value     = 0.0361;
  omega.reference = 'Optimized in \cite{nobel2020resources}.';

  d_m.value       = 0.2;
  d_m.reference   = 'Calculated from \cite{Hausser2019}';

  k_b.value       = 12.4404;
  k_u.reference   = 'Optimized in \cite{nobel2020resources}.';

  k_u.value       = 10.0454;
  k_u.reference   = 'Optimized in \cite{nobel2020resources}.';

  l_p.value       = 333;
  d_m.reference   = 'Calculated from \cite{Hausser2019}';

  E_m_eq.eqn      = 'E_m == 6.3492';
end ProteinNonRibosomal;

%% ---------------------------------------------------------
%% Stand-alone model.
%% ---------------------------------------------------------

ProteinNonRibosomal p_nr;
 
connect(p_nr__nu, 1);
connect(p_nr__mu, 1);
connect(p_nr__r, 1);
connect(p_nr__m_h, 1);
connect(p_nr__J_host_sum, 1);
