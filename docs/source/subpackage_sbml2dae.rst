Subpackage SBML2dae
===================

At the same time as we developed OneModel, we created SBML2dae: a OneModel subpackage, which provides programming tools to generate SBML exporters to other programming languages for simulation or analysis.
SBML2dae is open-source, written in Python, and complies with OneModel's design philosophy.

By default, SBML2dae only allows exporting SBML to Matlab.
However, it is straightforward for an expert user to create a new parser for another programming language such as Modelica, Julia, or Python. 
We expect more syntactic parsers to be incorporated using SBML2dae (by our group or by the community).

The differences with other Matlab parsers are (i) SBML2dae allows the simulation of algebraic loops (an indispensable element for the simulation of reduced-order models, using the quasi-steady-state approximation), (ii) it generates Matlab code using classes that significantly facilitates the integration of the models with the rest of Matlab tools and (iii) SBML2dae is easily modifiable to change the way of exporting the models.

There are excellent tools for simulation and analysis of SBML models, but one of the most significant drawbacks is when the tool does not fit the needs of pre-existing workflows.
SBML2dae solves this problem by allowing the user to implement customized SBML parsers that fit their particular workflow quickly.
