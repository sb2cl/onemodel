%% Initialization of the model.

clear all;
close all;

m = multiscale();

% Solver options.
opt = odeset('AbsTol',1e-8,'RelTol',1e-8);
opt = odeset(opt,'Mass',m.M);

% Simulation time span.
tspan = [m.opts.t_init m.opts.t_end];

p = m.p;

%% Simulation of the model.


% Parameters from the Bremer publication.
q = paramBremer();

n = 50;

nu = q.nu(1) + (0:n-1)*(q.nu(end) - q.nu(1))/(n-1);

OUT = [];

for i = 1:n
    % We want to use the parameters that give rise to the growth rate we
    % selected.
    p.cell__nu_max = nu(i);
    
    % Options for the solver.
    opt = odeset('AbsTol', 1e-8, 'RelTol', 1e-8);
    opt = odeset(opt,'Mass',m.M);
    
    % Simulate the model.
    [t,x] = ode15s(@(t,x) m.ode(t,x,p),tspan,m.x0,opt);
    out = m.simout2struct(t,x,p);
    
    f = fields(out);
    for i = 1:length(f)
        out.(f{i}) = out.(f{i})(end);
    end
    
    if isempty(OUT)
        OUT = out;
    else
        OUT = concatStruct(OUT,out);
    end
end

%% Plot figures.

colors;

figure(1);

subplot(3,2,1);

hold on;
plot(q.nu,q.proteinMass,'s','Color',myColors.array{1});
plot(OUT.cell__nu,OUT.cell__m_p,'Color',myColors.array{1});
grid on;
title('Cell Mass');
legend('exp','model','Location','Best');


subplot(3,2,2);

hold on;
plot(q.nu,q.mu,'s','Color',myColors.array{1});
plot(OUT.cell__nu,OUT.cell__mu,'Color',myColors.array{1});
grid on;
title('Growth rate');
legend('exp','model','Location','Best');


subplot(3,2,3);

hold on;
plot(OUT.cell__mu,OUT.cell__p_r__m,'Color',myColors.array{1});
plot(OUT.cell__mu,OUT.cell__p_nr__m,'Color',myColors.array{2});
plot(OUT.cell__mu,OUT.cell__m_p,'Color',myColors.array{3});
plot(q.mu,q.rt.*q.r_weight,'s','Color',myColors.array{1});
plot(q.mu,q.proteinMass-q.rt.*q.r_weight,'s','Color',myColors.array{2});
plot(q.mu,q.proteinMass,'s','Color',myColors.array{3});
grid on;
title('Absolute mass distribution');
legend('model r','model nr','total mass','exp r','exp nr','exp mass','Location','Best');

subplot(3,2,4);

hold on;
plot(OUT.cell__mu,OUT.cell__p_r__m./OUT.cell__m_p,'Color',myColors.array{1});
plot(OUT.cell__mu,OUT.cell__p_nr__m./OUT.cell__m_p,'Color',myColors.array{2});
plot(q.mu,q.rt.*q.r_weight./q.proteinMass,'s','Color',myColors.array{1});
plot(q.mu,(q.proteinMass-q.rt.*q.r_weight)./q.proteinMass,'s','Color',myColors.array{2});
grid on;
title('Normalized mass distribution');
legend('model r','model nr','exp r','exp nr','Location','Best');

subplot(3,2,5);

hold on;
plot(q.mu,q.r,'s','Color',myColors.array{1});
plot(OUT.cell__mu, OUT.cell__r,'Color',myColors.array{1});
legend('model','exp','Location','Best');

grid on;
title('Free ribosomes');

subplot(3,2,6);

hold on;
plot(q.mu,q.rt,'s','Color',myColors.array{1});
plot(OUT.cell__mu, OUT.cell__p_r__r_t,'Color',myColors.array{1});
legend('model','exp','Location','Best');

grid on;
title('Total ribosomes');

figure(2);

plot(OUT.cell__nu, OUT.cell__phi_b_t);
grid on;
title('$\phi_b^t$','Interpreter','latex');
ylim([0 1]);
xlabel('Effective translation rate $\nu$','Interpreter','latex');