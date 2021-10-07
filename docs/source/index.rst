.. onemodel documentation master file, created by
   sphinx-quickstart on Fri Sep 24 11:27:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to OneModel's documentation!
====================================

**OneModel** is a Python package for defining dynamic synthetic biology models easily and efficiently.

OneModel's syntax allows the definition of models with chemical reactions, ODEs and/or algebraic loops --which makes OneModel especially suitable for control theory applications where you need to combine biological processes with controllers implemented by DAEs.
OneModel focuses on code readability and modularity; and provides the user with tools to check the coherence of the generated models.
OneModel generates an `SBML <http://sbml.org/>`_ model file as output, which can be easily converted to other language implementations (such as Matlab, Julia, OpenModelica) with **sbml2dae**, or you could use many of the great SBML software developed by the community.

Check out the :doc:`usage` section for further information, including how to :ref:`install <installation>` OneModel.

.. note::

  This project is under active development.

.. toctree::
  :maxdepth: 2
  :caption: Contents:

  usage
  quick_start
  onemodel_syntax


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
