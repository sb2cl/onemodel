%% Example driver script for simulating "one_protein" model.

clear all;
close all;

% Init model.
m = one_protein();

% Solver options.
opt = odeset('AbsTol',1e-9,'RelTol',1e-9);
opt = odeset(opt,'Mass',m.M);

%% First simulation to get initial condition without the exogenous circuit.

p0 = m.p;
p0.cell__p_A__omega = 0;
[~,x0] = ode15s(@(t,x) m.ode(t,x,p0),[0 1e6],m.x0,opt);

x0 = x0(end,:);

%% Simulation time span.

tspan = [m.opts.t_init m.opts.t_end];

[t,x] = ode15s(@(t,x) m.ode(t,x,m.p),tspan,x0,opt);
out = m.simout2struct(t,x,m.p);

%% Plot result.

figure(1);

subplot(2,1,1);

hold on;

plot(out.t, out.cell__p_r__m);
plot(out.t, out.cell__p_nr__m);
plot(out.t, out.cell__p_A__m);

legend('ribo', 'non-ribo', 'A');
ylabel('Mass [fg]');
xlabel('Time [min]');

subplot(2,1,2);

plot(out.t, out.cell__mu);
ylabel('Growth rate [1/min]');
ylim([0 0.03]);
xlabel('Time [min]');