classdef ex02_two_genes_expression
	% This file was automatically generated by OneModel.
	% Any changes you make to it will be overwritten the next time
	% the file is generated.

	properties
		p      % Default model parameters.
		x0     % Default initial conditions.
		M      % Mass matrix for DAE systems.
		opts   % Simulation options.
	end

	methods
		function obj = ex02_two_genes_expression()
			%% Constructor of ex02_two_genes_expression.
			obj.p    = obj.default_parameters();
			obj.x0   = obj.initial_conditions();
			obj.M    = obj.mass_matrix();
			obj.opts = obj.simulation_options();
		end

		function p = default_parameters(~)
			%% Default parameters value.
			p = [];
			p.k_m_A = 1.0;
			p.d_m_A = 1.0;
			p.k_p_A = 1.0;
			p.d_p_A = 1.0;
			p.k_m_B = 1.0;
			p.d_m_B = 1.0;
			p.k_p_B = 1.0;
			p.d_p_B = 1.0;
		end

		function x0 = initial_conditions(~)
			%% Default initial conditions.
			x0 = [
				0.0 % mRNA_A
				0.0 % protein_A
				0.0 % mRNA_B
				0.0 % protein_B
			];
		end

		function M = mass_matrix(~)
			%% Mass matrix for DAE systems.
			M = [
				1 0 0 0 
				0 1 0 0 
				0 0 1 0 
				0 0 0 1 
			];
		end

		function opts = simulation_options(~)
			%% Default simulation options.
			opts.t_end = 10.0;
			opts.t_init = 0.0;
		end

		function dx = ode(~,t,x,p)
			%% Evaluate the ODE.
			%
			% Args:
			%	 t Current time in the simulation.
			%	 x Array with the state value.
			%	 p Struct with the parameters.
			%
			% Return:
			%	 dx Array with the ODE.

			% ODE and algebraic states:
			mRNA_A = x(1,:);
			protein_A = x(2,:);
			mRNA_B = x(3,:);
			protein_B = x(4,:);

			% Assigment states:

			% der(mRNA_A)
			dx(1,1) =  + (p.k_m_A) - (p.d_m_A.*mRNA_A) + (p.k_p_A.*mRNA_A) - (p.k_p_A.*mRNA_A);

			% der(protein_A)
			dx(2,1) =  + (p.k_p_A.*mRNA_A) - (p.d_p_A.*protein_A);

			% der(mRNA_B)
			dx(3,1) =  + (p.k_m_B) - (p.d_m_B.*mRNA_B) + (p.k_p_B.*mRNA_B) - (p.k_p_B.*mRNA_B);

			% der(protein_B)
			dx(4,1) =  + (p.k_p_B.*mRNA_B) - (p.d_p_B.*protein_B);

		end
		function out = simout2struct(~,t,x,p)
			%% Convert the simulation output into an easy-to-use struct.

			% We need to transpose state matrix.
			x = x';
			% ODE and algebraic states:
			mRNA_A = x(1,:);
			protein_A = x(2,:);
			mRNA_B = x(3,:);
			protein_B = x(4,:);

			% Assigment states:

			% Save simulation time.
			out.t = t;

			% Vector for extending single-value states and parameters.
			ones_t = ones(size(t'));


			% Save states.
			out.mRNA_A = (mRNA_A.*ones_t)';
			out.protein_A = (protein_A.*ones_t)';
			out.mRNA_B = (mRNA_B.*ones_t)';
			out.protein_B = (protein_B.*ones_t)';

			% Save parameters.
			out.k_m_A = (p.k_m_A.*ones_t)';
			out.d_m_A = (p.d_m_A.*ones_t)';
			out.k_p_A = (p.k_p_A.*ones_t)';
			out.d_p_A = (p.d_p_A.*ones_t)';
			out.k_m_B = (p.k_m_B.*ones_t)';
			out.d_m_B = (p.d_m_B.*ones_t)';
			out.k_p_B = (p.k_p_B.*ones_t)';
			out.d_p_B = (p.d_p_B.*ones_t)';

		end
		function plot(~,out)
			%% Plot simulation result.
			figure('Name','');
			subplot(2,2,1);
			plot(out.t, out.mRNA_A);
			title("mRNA_A");
			ylim([0, +inf]);
			grid on;

			subplot(2,2,2);
			plot(out.t, out.protein_A);
			title("protein_A");
			ylim([0, +inf]);
			grid on;

			subplot(2,2,3);
			plot(out.t, out.mRNA_B);
			title("mRNA_B");
			ylim([0, +inf]);
			grid on;

			subplot(2,2,4);
			plot(out.t, out.protein_B);
			title("protein_B");
			ylim([0, +inf]);
			grid on;

		end
	end
end
