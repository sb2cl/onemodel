OneModel workflow
=================

This section describes the OneModel workflow to help understand its use and usefulness.

.. figure:: ../images/onemodel_workflow.svg
  :align: center
  :width: 350
  :alt: onemodel workflow

  Graphic scheme of the OneModel workflow. The user writes a model using OneModel syntax (".one"). Then, the model is exported into SBML using OneModel. Finally, the SBML-compliant tools can be used as (i) SBML2dae generates a Matlab implementation of the model (".m"), or (ii) SBML2Modelica generates a Modelica representation (".mo").

The first step is to write a model, as a plain text file with ".one" or ".onemodel" as extension, using OneModel syntax.
The user can use either the OneModel's editor (available in the graphical user interface) or his own text editor.
Our goal is to get non-expert users to use our editor, but we prefer that they eventually switch to working with the command-line interface and their preferred text editor (such as Vim, SublimeText, or Atom)---as they become proficient with OneModel.

The second step is to export this model as an SBML file.
Both the graphical user interface and the command line interface can export the model. Actually, the graphical user interface calls the command-line interface in the background to perform the export.

Then, the SBML file can be fed into any available SBML-compliant tools to perform the computational simulations, analysis, etc.
The scope of OneModel is limited only to the definition of SBML models, so it relies on other tools to make use of them.
We have implemented the tool SBML2dae (included with \textit{OneModel}) to generate simulation-ready Matlab implementations of SBML models.
As an alternative to our SBML2dae, we could also have used SBML2Modelica, a translator tool available in the literature, to generate a Modelica implementation instead.
In this way, the users can choose which of the large and powerful tools of the SBML community they want to incorporate into their workflow.

Finally, once the model has been validated, we can repeat this loop, generating a new model that imports the code and functionality of the previously defined models.
