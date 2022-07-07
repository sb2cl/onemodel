from xml.etree import ElementTree

from onemodel.core.onemodel import OneModel
from onemodel.core.objects.species import Species
from onemodel.core.objects.parameter import Parameter
from onemodel.core.objects.assignment_rule import AssignmentRule

def test_init():
    result = AssignmentRule()
    assert isinstance(result, AssignmentRule)

def test_add_2_SBML_model():
    m = OneModel()

    m.root["foo"] = Species()
    m.root["bar"] = Parameter()
    m.root["R1"] = AssignmentRule()
    m.root["R1"].variable = "foo"
    m.root["R1"].math = "10*bar"

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
      <species id="foo" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="bar" value="0" units="per_second" constant="true"/>
    </listOfParameters>
    <listOfRules>
      <assignmentRule id="R1" variable="foo">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <apply>
            <times/>
            <cn type="integer"> 10 </cn>
            <ci> bar </ci>
          </apply>
        </math>
      </assignmentRule>
    </listOfRules>
  </model>
</sbml>
"""

    expected = ElementTree.fromstring(expected_string)
    assert ElementTree.tostring(result) == ElementTree.tostring(expected)
