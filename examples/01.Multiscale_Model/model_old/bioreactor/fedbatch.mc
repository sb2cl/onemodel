use ./model/bioreactor/bioreactor.mc;

%% ---------------------------------------------------------
%% Definition of the class Batch.
%% ---------------------------------------------------------

class Fedbatch
  
  extends Bioreactor;

  parameter V_final(
    comment = 'Final desired volume.',
    units = 'L',
    value = 10
    );

  % In fedbatch, we use a high concentrated substrate.
  s_f.value = 180.156;

  connect(F_in, ((1/y)*mu*x*V/(s_f-s)) * (heaviside(V - 0)*(1 - heaviside(V - V_final))));
  connect(F_out, 0);

end Fedbatch;

%% ---------------------------------------------------------
%% Stand-alone model.
%% ---------------------------------------------------------
 
Fedbatch fedbatch;

parameter m_p( 
  value = 433 
  );

variable mu( 
  value = log(2)/24*batch__s/(batch__s+batch__K_s),
  title = 'Growth rate $\mu$'
  );

connect(batch__m_p, m_p);
connect(batch__mu, mu);
