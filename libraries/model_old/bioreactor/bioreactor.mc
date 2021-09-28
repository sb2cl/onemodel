%% ---------------------------------------------------------
%% Definition of the class Bioreactor.
%% ---------------------------------------------------------

class Bioreactor

  %% ---------------------------------------------------------
  %% Inputs.
  %% ---------------------------------------------------------

  variable m_p(
    units = 'fg',
    comment = 'Total protein mass of the cell.',
    isPlot = false,
    isTex = false
    );

  variable mu(
    units = '1/min',
    comment = 'Growth rate.',
    title='Growth rate',
    ylabel='[min$^{-1}$]',
    ylim = [0 0.03],
    isTex = false
    );

  variable F_in(
    comment = 'Input media flux.',
    units = 'L \cdot min^{-1}',
    isPlot = false,
    nameTex = 'F_{in}'
    );
 
  variable F_out(
    comment = 'Output waste flux.',
    units = 'L \cdot min^{-1}',
    isPlot = false,
    nameTex = 'F_{out}'
    );
 
  %% ---------------------------------------------------------
  %% Parameters.
  %% ---------------------------------------------------------
  
  parameter y(
    comment = 'Biomass yield on glucose.',
    units = 'g^{ }_{biomass} \cdot g^{-1}_{substrate}',
    value = 0.45,
    nameTex = 'y',
    reference = '\cite{Link2008}'
    );
  
  parameter s_f(
    comment = 'Fresh media substrate concentration.',
    units = 'g \cdot L^{-1}',
    value = 3.6,
    nameTex = 's_{feed}',
    reference = '\cite{Zhuang2013}'
    % reference = 'Dynamic strain scanning optimization: An efficient strain design strategy for balanced yield, titer, and productivity. DySScO strategy for strain design'
    );
  
  parameter nOD(
    comment = 'Concentration of E.Coli. cells in 1 OD (Optical density).',
    units = 'cell \cdot L^{-1}',
    %reference = 'http://book.bionumbers.org/what-is-the-concentration-of-bacterial-cells-in-a-saturated-culture/',
    value = 1e12,
    nameTex = 'n_{OD}',
    valueTex = '1e12',
    isTex = false
    );

  %% ---------------------------------------------------------
  %% Variables.
  %% ---------------------------------------------------------

  variable V(
    comment = 'Volume of culture in the biorreactor.',
    units = 'L',
    start = 1,
    title = 'Volume',
    nameTex = 'V',
    equationTex =  '\dot V &= F_{in} - F_{out}'
    % reference = 'Dynamic strain scanning optimization: An efficient strain design strategy for balanced yield, titer, and productivity. DySScO strategy for strain design'
    );

  variable V_feed(
    units = 'L',
    comment = 'Total volume feeded to the bioreactor.',
    title = '$V_{feed}$',
    isTex = false
    );

  variable V_out(
    units = 'L',
    comment = 'Total volume removed from the bioreactor.',
    title = '$V_{out}$',
    isTex = false
    );
 
  variable N(
    comment = 'Concentration of cells in the biorreactor.',
    units = 'cell \cdot L^{-1}',
    title = 'Concentration of cells $n$',
    start = 5e10,
    nameTex = 'n',
    equationTex = '\dot n &= \mu n - \frac{F_{in}}{V} n'
    % reference = 'Dynamic strain scanning optimization: An efficient strain design strategy for balanced yield, titer, and productivity. DySScO strategy for strain design'
    );
  
  variable x(
    comment = 'Concentration of biomass in the biorreactor.',
    units = 'g/L',
    value = N*m_p*1e-15,
    title = 'Biomass concentration $x$',
    nameTex = 'x(n,\mu)',
    equationTex = 'x(n,\mu) = n m_p(\mu)'
    );
  
  variable OD(
    comment = 'Optical density in the biorreactor.',
    units = 'OD',
    value = N/nOD,
    title = 'Optical density',
    nameTex = 'x_{OD}(n)',
    equationTex = 'x_{OD}(n) = n / n_{OD}',
    isTex = false
    );
  
  variable s(
    comment = 'Concentration of substrate in the biorreactor.',
    units = 'g \cdot L^{-1}',
    start = 3.6,
    title = 'Substrate concentration $s$',
    nameTex = 's',
    equationTex = '\dot s &= \frac{F_{in}}{V} (s_{feed} - s) - y^{-1} \mu x(n,\mu)'
    );

  variable S(
    units = 'g',
    comment = 'Total mass of substrate removed from the bioreactor.',
    title = 'S',
    isTex = false
    );

  %% ---------------------------------------------------------
  %% Equations.
  %% ---------------------------------------------------------
  
  equation der_V == F_in - F_out;
  equation der_V_feed == F_in;
  equation der_V_out == F_out;
  equation der_N == mu*N - F_in/V*N;
  %equation der_s == F_in/V*(s_f - s) - y^(-1)*mu*x ;
  equation der_s == F_in/V*(s_f - s) - (1/y)*mu*x ;
  equation der_S == F_out*s;

end Bioreactor;

%% ---------------------------------------------------------
%% Stand-alone model.
%% ---------------------------------------------------------
 
Bioreactor bio;

parameter m_p( 
  value = 433 
  );

variable mu( 
  value = log(2)/24*bio__s/(bio__s+bio__K_s),
  title = 'Growth rate $\mu$'
  );

variable F_in(
  value = 0
  );

variable F_out(
  value = 0
  );

connect(bio__m_p, m_p);
connect(bio__mu, mu);
connect(bio__F_in, F_in);
connect(bio__F_out, F_out);
