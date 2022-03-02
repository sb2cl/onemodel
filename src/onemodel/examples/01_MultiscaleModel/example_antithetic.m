%% Example driver script for simulating "antithetic_controller" model.

clear all;

% Init model.
m = antithetic_controller();
p = m.p;

p.cell____burden = 0;
p.cell____dilution = 0;
outA = simulate(m,p);

p.cell____burden = 0;
p.cell____dilution = 1;
outB = simulate(m,p);

p.cell____burden = 1;
p.cell____dilution = 0;
outC = simulate(m,p);

p.cell____burden = 1;
p.cell____dilution = 1;
outD = simulate(m,p);

%% Plot result.

close all;

fig = figure('units','centimeters','position',[0,0,14,5]);
colors;

subplot(1,2,1);

hold on;
plot(outA.t, outA.cell__x__m, 'Color', myColors.blue);
plot(outB.t, outB.cell__x__m, '--', 'Color', myColors.blue);
plot(outC.t, outC.cell__x__m, 'Color', myColors.orange);
plot(outD.t, outD.cell__x__m, '--', 'Color', myColors.orange);

grid on;
ylabel('Protein $x$ [fg]','interpreter','latex');
xlabel('Time [h]','interpreter','latex');
ylim([0 105]);
yticks([0 35 70 105]);
xticks([0 5 10 15 20]);

subplot(1,2,2);

hold on;
plot(outA.t, outA.cell__mu, 'Color', myColors.blue);
plot(outB.t, outB.cell__mu, '--', 'Color', myColors.blue);
plot(outC.t, outC.cell__mu, 'Color', myColors.orange);
plot(outD.t, outD.cell__mu, '--', 'Color', myColors.orange);

grid on;
ylabel('Growth rate [min$^{-1}$]','interpreter','latex');
ylim([0 0.03]);
yticks([0 0.01 0.02 0.03]);
xticks([0 5 10 15 20]);
xlabel('Time [h]','interpreter','latex');

print(fig,'./figs/Example_03.eps','-depsc');

%% Simulate auxiliar funtion

function out = simulate(m,p)

% Solver options.
opt = odeset('AbsTol',1e-9,'RelTol',1e-9);
opt = odeset(opt,'Mass',m.M);

% First simulation to get initial condition without the exogenous circuit.

p0 = p;
p0.cell__z1__omega = 0;
[t0,x0] = ode15s(@(t,x) m.ode(t,x,p0),[0 1e6],m.x0,opt);
out0 = m.simout2struct(t0,x0,p0);
out0.t = out0.t/60;

x0 = x0(end,:);

% Second simulation.
tspan = [m.opts.t_init 20*60];

[t,x] = ode15s(@(t,x) m.ode(t,x,p),tspan,x0,opt);
out = m.simout2struct(t,x,p);

out.t = out.t/60;
end