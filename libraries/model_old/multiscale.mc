% Inner cell models.
use ./model/wildType/wildType.mc;
use ./model/syntheticCircuit/oneProtein.mc;

% Mass equation models.
use ./model/massEquation/massInterpolated.mc;
use ./model/massEquation/massEqJesus.mc;

% Biorreactor models.
use ./model/bioreactor/bioreactor.mc;
use ./model/bioreactor/batch.mc;
use ./model/bioreactor/fedbatch.mc;
use ./model/bioreactor/continous.mc;

% Productivity model.
use ./model/productivity/productivity.mc;


%% ---------------------------------------------------------
%% Definition of the mass equation we want to use.
%% ---------------------------------------------------------

% Wild-type cell model.
if strcmp(opts.cellModel, 'wildType');
  WildType cellModel;
end if;

% Wild-type cell model with a heterologous protein A.
if strcmp(opts.cellModel, 'oneProtein');
  OneProtein cellModel;
end if;




%% ---------------------------------------------------------
%% Definition of the mass equation we want to use.
%% ---------------------------------------------------------

% Interpolated mass equation.
if strcmp(opts.massEq, 'interpolated');
  MassInterpolated mass;

  connect(mass__mu, cellModel__mu);
end if;

% The equation derived by jesus.
if strcmp(opts.massEq, 'eq_jesus');
  MassEqJesus mass;

  connect(mass__mu, cellModel__mu);
end if;

% Assume that the mass if fix.
if strcmp(opts.massEq, 'fix');
  parameter mass__m_h(value = 450, isTex = false);
end if;

connect(cellModel__m_h, mass__m_p);





%% ---------------------------------------------------------
%% Definition of the bioreactor model we want to use.
%% ---------------------------------------------------------

% Use a fix translation rate.
if strcmp(opts.bioreactor, 'nuFix');
  parameter bio__nu(value = 1260);

  % We need to overried the equation of cellModel__nu.
  cellModel__nu_eq.eqn = 'cellModel__nu ==  bio__nu';
 
  connect(cellModel__s, 0);
end if;


% Use a fix substrate concentration.
if strcmp(opts.bioreactor, 'substrateFix');
  parameter bio__s(value = 3.6);

  connect(cellModel__s, bio__s);
end if;

% Use the bioreactor model to calculate the translation rate.
if strcmp(opts.bioreactor, 'batch');
  Batch bio;

  connect(bio__mu, cellModel__mu);
  connect(bio__m_p, cellModel__m_sum);
  connect(cellModel__s, bio__s);
end if;

% Use the bioreactor model to calculate the translation rate.
if strcmp(opts.bioreactor, 'fedbatch');
  Fedbatch bio;

  connect(bio__mu, cellModel__mu);
  connect(bio__m_p, cellModel__m_sum);
  connect(cellModel__s, bio__s);
end if;

% Use the bioreactor model to calculate the translation rate.
if strcmp(opts.bioreactor, 'continous');
  Continous bio;

  connect(bio__mu, cellModel__mu);
  connect(bio__m_p, cellModel__m_sum);
  connect(cellModel__s, bio__s);
end if;






%% ---------------------------------------------------------
%% Definition of the productiviy states.
%% ---------------------------------------------------------

% If oneProtein and bioreactor mode are selected.
if strcmp(opts.cellModel, 'oneProtein') && ~strcmp(opts.bioreactor, 'substrateFix') && ~strcmp(opts.bioreactor, 'nuFix');
  % Add the productivity equations.
  Productivity pro;

  connect(pro__F_out, bio__F_out);
  connect(pro__N, bio__N);
  connect(pro__m_A, cellModel__m_A*1e-15);
end if;
