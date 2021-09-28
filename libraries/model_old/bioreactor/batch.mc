use ./model/bioreactor/bioreactor.mc;

%% ---------------------------------------------------------
%% Definition of the class Batch.
%% ---------------------------------------------------------

class Batch
  
  extends Bioreactor;

  % Set input and output flow to zero.
  connect (F_in, 0);
  connect (F_out, 0);

end Batch;

%% ---------------------------------------------------------
%% Stand-alone model.
%% ---------------------------------------------------------
 
Batch batch;

parameter m_p( 
  value = 433 
  );

variable mu( 
  value = log(2)/24*batch__s/(batch__s+batch__K_s),
  title = 'Growth rate $\mu$'
  );

connect(batch__m_p, m_p);
connect(batch__mu, mu);
