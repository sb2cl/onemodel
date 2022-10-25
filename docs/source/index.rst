.. onemodel documentation master file, created by
   sphinx-quickstart on Fri Sep 24 11:27:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OneModel's documentation!
====================================

**OneModel** is an open-source text-based tool for defining SBML models in a modular and incremental way that minimizes the user’s programming knowledge requirements.

With the advent of the Systems Biology Markup Language (`SBML <http://sbml.org/>`_), a large community of SBML-compliant tools has been created.
However, these tools can only be used to their full potential by expert users with advanced programming knowledge.
OneModel is an open-source text-based tool for defining SBML models in a modular and incremental way that minimizes the user’s programming knowledge requirements.
It is focused on accessibility, simplicity, and modularity.
OneModel syntax allows the user to define models based on chemical (and pseudo-chemical) reactions, differential equations, and algebraic equations.
OneModel is written in Python and it provides two interfaces: a command-line interface for expert-users, and a graphical user interface for non-expert users.

Check out the :doc:`installation` and :doc:`quick_start` sections for further information.

.. note::

  This project is under active development.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  introduction
  installation
  quick_start
  onemodel_workflow
  onemodel_design_philosophy
  onemodel_implementation
  subpackage_sbml2dae
  onemodel_syntax
  examples
  modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
