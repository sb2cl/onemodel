%% ---------------------------------------------------------
%% Definition of the class OneProtein.
%% ---------------------------------------------------------

use ./model/wildType/wildType.mc;

class OneProtein

  extends WildType;

  % We include the expression of heterologous protein A.
  Protein p_A;

  % We just use the values of ribosomal proteins for protein A.
  p_A__N.value = 1;
  p_A__omega.value = 10;
  p_A__d_m.value = 0.16; 
  p_A__k_b.value = 4.7627;
  p_A__k_u.value = 119.7956;
  p_A__l_p.value = 195;

  % Connect the input values needed for protein A.
  connect(p_A__nu, nu);
  connect(p_A__mu, mu);
  connect(p_A__r, r);
  connect(p_A__m_h, m_h);
  connect(p_A__J_host_sum, J_host_sum);

  % Override these equations taking into account protein A.
  m_p_eq.eqn = 'm_p == p_r__m + p_nr__m + p_A__m';
  J_sum_eq.eqn = 'J_sum == p_r__N*p_r__J + p_nr__N*p_nr__J + p_A__N*p_A__J';
  J_sum_E_eq.eqn = 'J_sum_E == p_r__N*(1+1/p_r__E_m)*p_r__J + p_nr__N*(1+1/p_nr__E_m)*p_nr__J + p_A__N*(1+1/p_A__E_m)*p_A__J';


end OneProtein;

%% ---------------------------------------------------------
%% Stand alone model.
%% ---------------------------------------------------------

parameter s(value = 3.6, isTex = false);
parameter m_p(value = 450, isTex = false);

OneProtein wt;

connect(wt__s, s);
connect(wt__m_p, m_p);
