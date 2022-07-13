from xml.etree import ElementTree

from onemodel.objects.parameter import Parameter
from onemodel.onemodel import OneModel


def test_init():
    result = Parameter()
    assert isinstance(result, Parameter)


def test_add_2_SBML_model():

    m = OneModel()
    m["a"] = Parameter()
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
    <listOfParameters>
      <parameter id="a" value="0" units="per_second" constant="true"/>
    </listOfParameters>
  </model>
</sbml>
    """
    expected = ElementTree.fromstring(expected_string)

    assert ElementTree.tostring(result) == ElementTree.tostring(expected)
