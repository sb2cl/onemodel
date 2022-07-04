from xml.etree import ElementTree

from onemodel.core.onemodel import OneModel
from onemodel.core.objects.object import Object
from onemodel.core.objects.species import Species
from onemodel.core.objects.parameter import Parameter
from onemodel.core.objects.reaction import Reaction

def test_init():

    m = OneModel()

    assert isinstance(m, OneModel)


def test_get_SBML_string():

    m = OneModel()

    result_string = m.get_SBML_string()
    result = ElementTree.fromstring(result_string)

    expected_string = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model id="main" name="main" substanceUnits="mole" timeUnits="second" extentUnits="mole">
    <listOfUnitDefinitions>
      <unitDefinition id="per_second">
        <listOfUnits>
          <unit kind="second" exponent="-1" scale="0" multiplier="1"/>
        </listOfUnits>
      </unitDefinition>
    </listOfUnitDefinitions>
    <listOfCompartments>
      <compartment id="default_compartment" spatialDimensions="3" size="1" units="litre" constant="true"/>
    </listOfCompartments>
  </model>
</sbml>
"""
    expected = ElementTree.fromstring(expected_string)

    assert ElementTree.tostring(result) == ElementTree.tostring(expected)

def test_ex01_simple_gene_expression():

    m = OneModel()
    
    m.root['mRNA'] = Species()
    m.root['protein'] = Species()
    
    m.root['k_m'] = Parameter()
    m.root['d_m'] = Parameter()
    m.root['k_p'] = Parameter()
    m.root['d_p'] = Parameter()
    
    m.root['J1'] = Reaction()
    m.root['J1'].reactants = []
    m.root['J1'].products = ['mRNA']
    m.root['J1'].kinetic_law = 'k_m'
    
    m.root['J2'] = Reaction()
    m.root['J2'].reactants = ['mRNA']
    m.root['J2'].products = []
    m.root['J2'].kinetic_law = 'd_m*mRNA'
    
    m.root['J3'] = Reaction()
    m.root['J3'].reactants = ['mRNA']
    m.root['J3'].products = ['mRNA', 'protein']
    m.root['J3'].kinetic_law = 'k_p*mRNA'
    
    m.root['J4'] = Reaction()
    m.root['J4'].reactants = ['protein']
    m.root['J4'].products = []
    m.root['J4'].kinetic_law = 'd_p*protein'
    
    result_string = m.get_SBML_string()
    result = ElementTree.fromstring(result_string)

    print(result_string)
    
    expected_string = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model id="main" name="main" substanceUnits="mole" timeUnits="second" extentUnits="mole">
    <listOfUnitDefinitions>
      <unitDefinition id="per_second">
        <listOfUnits>
          <unit kind="second" exponent="-1" scale="0" multiplier="1"/>
        </listOfUnits>
      </unitDefinition>
    </listOfUnitDefinitions>
    <listOfCompartments>
      <compartment id="default_compartment" spatialDimensions="3" size="1" units="litre" constant="true"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="mRNA" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="protein" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="k_m" value="0" units="per_second" constant="true"/>
      <parameter id="d_m" value="0" units="per_second" constant="true"/>
      <parameter id="k_p" value="0" units="per_second" constant="true"/>
      <parameter id="d_p" value="0" units="per_second" constant="true"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="J1" reversible="false">
        <listOfProducts>
          <speciesReference species="mRNA" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> k_m </ci>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="J2" reversible="false">
        <listOfReactants>
          <speciesReference species="mRNA" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> d_m </ci>
              <ci> mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="J3" reversible="false">
        <listOfReactants>
          <speciesReference species="mRNA" constant="true"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="mRNA" constant="true"/>
          <speciesReference species="protein" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> k_p </ci>
              <ci> mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="J4" reversible="false">
        <listOfReactants>
          <speciesReference species="protein" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> d_p </ci>
              <ci> protein </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>
    """
    expected = ElementTree.fromstring(expected_string)

    assert ElementTree.tostring(result) == ElementTree.tostring(expected)

def test_ex03_protein_constitutive():
    m = OneModel()
    
    m.root['A'] = Object()

    m.root['A']['mRNA'] = Species()
    m.root['A']['protein'] = Species()

    m.root['A']['k_m'] = Parameter()
    m.root['A']['d_m'] = Parameter()
    m.root['A']['k_p'] = Parameter()
    m.root['A']['d_p'] = Parameter()
    
    m.root['A']['J1'] = Reaction()
    m.root['A']['J1'].reactants = []
    m.root['A']['J1'].products = ['mRNA']
    m.root['A']['J1'].kinetic_law = 'k_m'
    
    m.root['A']['J2'] = Reaction()
    m.root['A']['J2'].reactants = ['mRNA']
    m.root['A']['J2'].products = []
    m.root['A']['J2'].kinetic_law = 'd_m*mRNA'
    
    m.root['A']['J3'] = Reaction()
    m.root['A']['J3'].reactants = ['mRNA']
    m.root['A']['J3'].products = ['mRNA', 'protein']
    m.root['A']['J3'].kinetic_law = 'k_p*mRNA'
    
    m.root['A']['J4'] = Reaction()
    m.root['A']['J4'].reactants = ['protein']
    m.root['A']['J4'].products = []
    m.root['A']['J4'].kinetic_law = 'd_p*protein'
 
    result_string = m.get_SBML_string()
    result = ElementTree.fromstring(result_string)

    print(result_string)

    expected_string = """<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model id="main" name="main" substanceUnits="mole" timeUnits="second" extentUnits="mole">
    <listOfUnitDefinitions>
      <unitDefinition id="per_second">
        <listOfUnits>
          <unit kind="second" exponent="-1" scale="0" multiplier="1"/>
        </listOfUnits>
      </unitDefinition>
    </listOfUnitDefinitions>
    <listOfCompartments>
      <compartment id="default_compartment" spatialDimensions="3" size="1" units="litre" constant="true"/>
    </listOfCompartments>
    <listOfSpecies>
      <species id="A__mRNA" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="A__protein" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="A__k_m" value="0" units="per_second" constant="true"/>
      <parameter id="A__d_m" value="0" units="per_second" constant="true"/>
      <parameter id="A__k_p" value="0" units="per_second" constant="true"/>
      <parameter id="A__d_p" value="0" units="per_second" constant="true"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="A__J1" reversible="false">
        <listOfProducts>
          <speciesReference species="A__mRNA" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> A__k_m </ci>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="A__J2" reversible="false">
        <listOfReactants>
          <speciesReference species="A__mRNA" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> A__d_m </ci>
              <ci> A__mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="A__J3" reversible="false">
        <listOfReactants>
          <speciesReference species="A__mRNA" constant="true"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="A__mRNA" constant="true"/>
          <speciesReference species="A__protein" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> A__k_p </ci>
              <ci> A__mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="A__J4" reversible="false">
        <listOfReactants>
          <speciesReference species="A__protein" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> A__d_p </ci>
              <ci> A__protein </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>
    """
    expected = ElementTree.fromstring(expected_string)


    assert ElementTree.tostring(result) == ElementTree.tostring(expected)
