# OneModel

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Description

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

## Citing

If you use OneModel in your research, please use the following citations in your published works:

- Santos-Navarro, F. N., Navarro, J. L., Boada, Y., Vignoni, A., & Picó, J. (2022). "OneModel: an open-source SBML modeling tool focused on accessibility, simplicity, and modularity." *DYCOPS*.

- Santos-Navarro, F. N., Vignoni, A., & Picó, J. (2022). "Multi-scale host-aware modeling for analysis and tuning of synthetic gene circuits for bioproduction." *PhD thesis*.

## License

Copyright 2022 Fernando N. Santos-Navarro, Jose Luis Herrero, Yadira Boada, Alejandro Vignoni, and Jesús Picó

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this software except in compliance with the License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
