from xml.etree import ElementTree

from onemodel.core.objects.reaction import Reaction
from onemodel.core.objects.parameter import Parameter
from onemodel.core.objects.species import Species
from onemodel.core.onemodel import OneModel


def test_init():
    result = Reaction()
    assert isinstance(result, Reaction)

def test_add_2_SBML_model():
    
    m = OneModel()

    m.root['A'] = Species()
    m.root['B'] = Species()
    m.root['k'] = Parameter()

    m.root['J1'] = Reaction()
    r = m.root['J1']
    r.reactants = ['A']
    r.products = ['B']
    r.kinetic_law = 'k'

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
      <species id="A" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="B" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="k" value="0" units="per_second" constant="true"/>
    </listOfParameters>
    <listOfReactions>
      <reaction id="J1" reversible="false">
        <listOfReactants>
          <speciesReference species="A" constant="true"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="B" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> k </ci>
          </math>
        </kineticLaw>
      </reaction>
    </listOfReactions>
  </model>
</sbml>
    """
    expected = ElementTree.fromstring(expected_string)

    assert ElementTree.tostring(result) == ElementTree.tostring(expected)
