%% Example driver script for simulating "antithetic_controller" model.

clear all;
close all;

% Init model.
m = antithetic_controller();

% Solver options.
opt = odeset('AbsTol',1e-9,'RelTol',1e-9);
opt = odeset(opt,'Mass',m.M);

%% First simulation to get initial condition without the exogenous circuit.

p0 = m.p;
p0.cell__z1__omega = 0;
[~,x0] = ode15s(@(t,x) m.ode(t,x,p0),[0 1e6],m.x0,opt);

x0 = x0(end,:);

%% Simulation time span.

tspan = [m.opts.t_init m.opts.t_end];

[t,x] = ode15s(@(t,x) m.ode(t,x,m.p),tspan,x0,opt);
out = m.simout2struct(t,x,m.p);

%% Plot result.

figure(1);

subplot(3,1,1);

hold on;

plot(out.t, out.cell__p_r__m);
plot(out.t, out.cell__p_nr__m);

legend('ribo', 'non-ribo');
ylabel('Mass [fg]');
xlabel('Time [min]');

subplot(3,1,2);

hold on;

plot(out.t, out.cell__z1__m);
plot(out.t, out.cell__z2__m);
plot(out.t, out.cell__z12__m);
plot(out.t, out.cell__x__m);

legend('z1', 'z2', 'z12', 'x');
ylabel('Mass [fg]');
xlabel('Time [min]');

subplot(3,1,3);

plot(out.t, out.cell__mu);
ylabel('Growth rate [1/min]');
ylim([0 0.03]);
xlabel('Time [min]');