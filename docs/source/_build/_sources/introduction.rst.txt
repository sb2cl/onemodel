Introduction 
============

The Systems Biology Markup Language (SBML) is the software data format for describing models in biology.
With the advent of SBML, many SBML-compliant tools have been created.
These tools fulfill the syntax and semantics of SBML through different approaches: text-based tools such as Antimony, Little b, BioCRNpyler; or graphical user interface based tools such as CellDesigner and iBioSim.

Models are often constructed as a monolithic set of equations, reactions, parameters, and species.
This leads to inefficient modeling practices in which (i) new models are implemented from scratch, rather than extending previous models; (ii) models have to be validated as a whole, rather than validating the constituent parts of the model; and (iii) models tend to be large and repetitive, rather than defining and reusing modules in their implementation.
Antimony, BioCRNpyler and Little b solve this problem by implementing different degrees of modularity.
However, these tools are aimed at, or can only be used to their full potential by, expert users with advanced programming knowledge.

OneModel is an open-source text-based tool for defining and compiling SBML models in a modular way.
This modularity allows incremental implementations of several simple models to obtain a more complex one.
OneModel also minimizes the user's programming knowledge requirements.
OneModel was designed in this Thesis to be easy-to-use and easy-to-incorporate into pre-existing workflows.
We used well-documented Python libraries to avoid custom code development in its implementation. Therefore advanced programmers will be able to tweak, expand or hack OneModel functionality easily.
The syntax of our tool implements modularity through object-oriented programming.
We were inspired by the Arduino community, where a simple graphical user interface enables non-expert users to contribute their work and ideas to the community.
