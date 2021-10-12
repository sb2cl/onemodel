# OneModel

**OneModel** is a Python package for defining dynamic synthetic biology models easily and efficiently.

OneModel's syntax allows the definition of models with chemical reactions, ODEs and/or algebraic loops --which makes OneModel especially suitable for control theory applications where you need to combine biological processes with controllers implemented by DAEs.
OneModel focuses on code readability and modularity; and provides the user with tools to check the coherence of the generated models.
OneModel generates an [SBML](http://sbml.org/) model file as output, which can be easily converted to other language implementations (such as Matlab, Julia, OpenModelica) with sbml2dae, or you could use many of the great SBML software developed by the community.

*This project is under active development.*


- **Documentation**: https://onemodel.readthedocs.io/en/latest/

## Installation

*Requires Python 3.8 or greater installed.*

```
  pip install onemodel
```

## Example


