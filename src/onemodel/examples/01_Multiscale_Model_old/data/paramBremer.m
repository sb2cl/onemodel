function [p] = paramBremer()
%% This function recopiles the data presented in the paper of Bremer.

%% Cell or global parameters.

% Growth rate. 1/min
p.mu = [
    log(2)/100
    log(2)/60
    log(2)/40
    log(2)/30
    log(2)/24
    ];

% Translation rate. aa/min
p.nu = [
    12
    16
    18
    20
    21
    ]*60;

% p.nu(3) = 1097.5;

% Number of ribosomes (mature and inmature). molecs
p.rt = [
    6800
    13500
    26300
    45100
    72000
    ];

% Protein mass. fg
p.proteinMass = [
    100
    156
    234
    340
    450
    ];

% cell DW (fg)
p.cellMass = [
    148
    258
    433
    641
    865
    ];


% Average amino acid mass.
p.m_aa = 182.6e-9; % fg

% Tasa de utilizacion de los ribosomas.
p.phi_rt = p.proteinMass.*p.mu./(p.nu.*p.m_aa.*p.rt);

% Ribosomas activos.
p.ra = p.rt.*p.phi_rt;

% Dalton unit
p.Da = 1.6605e-24; % g/Da

% Ribosome weight
p.r_weight = 2.7; %MDalton
p.r_weight = p.r_weight*p.Da*1000000*1e15;% fg

p.ribosome_fraction_mass = p.rt.*p.r_weight./p.proteinMass;

% Suponemos una cantidad de ribosomas libres basandonos en nuestro
% resultados y la publicación de los ribosomas que encontré.
p.r = 350; % molecs

% Claro, esta r debe ser para una cantidad de ribosomas totales especifica.
% Si mantenemos el ratio debe dar algo como esto:
p.r = p.r/p.rt(5).*p.rt; % molecs

% Definimos ribosmas maduros como:
p.rm = p.ra + p.r;

p.phi_r = (p.rm-p.r)./p.rm;

% Cálculo de J experimentales.
p.Jsum_exp = p.phi_r./(1-p.phi_r);
p.Jr_exp = p.Jsum_exp.*p.ribosome_fraction_mass;
p.Jnr_exp = p.Jsum_exp.*(1-p.ribosome_fraction_mass);
p.r_exp = p.r;

%% Ribosomal

% Abundancy of ribosomal mRNA. molecs. [0 1380].
% p.rna_r = 668.5198;
% Average ribosomal protein length. aa.
p.lp_r = 195;
% Ribosome occupancy length. aa molec^-1. [20 30].
p.le_r = 24;
% Degradation rate of ribosmal mRNA. 1/min.
p.dm_r = 0.28;
% Dissotiation rate RBS-ribosome. 1/min. [6 135].
% ku_r = 135;
% Dissotiation rate RBS-ribosome. 1/min/molec. [3 15].
% kb_r = 3;


%% Non-ribosomal

% Abundancy of non-ribosomal mRNA. molecs [0 1380]
% rna_nr = 1380-668.5198;
% Average non-ribosomal protein length. aa.
p.lp_nr = 333;
% Ribosome occupancy length. aa molec^-1. [20 30].
p.le_nr = 24;
% Degradation rate of non-ribosmal mRNA. 1/min.
p.dm_nr = 0.28;
% Dissotiation rate RBS-ribosome. 1/min. [6 135].
% ku_nr = 135;
% Dissotiation rate RBS-ribosome. 1/min/molec. [3 15].
% kb_nr = 15;

end
