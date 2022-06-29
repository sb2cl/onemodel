from xml.etree import ElementTree

from onemodel.core.onemodel import OneModel


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


# def test_ex01_simple_gene_expression():
#
#    m = OneModel()
#
#    m['mRNA'] = Species(start=0)
#    m['protein'] = Species(start=0)
#
#    m['k_m'] = Parameter(value=1)
#    m['d_m'] = Parameter(value=1)
#    m['k_p'] = Parameter(value=1)
#    m['d_p'] = Parameter(value=1)
#
#    m['J1'] = Reaction(
#        None,
#        'mRNA',
#        'k_m'
#    )
#
#    m['J2'] = Reaction(
#        'mRNA',
#        None,
#        'd_m*mRNA'
#    )
#
#    m['J3'] = Reaction(
#        'mRNA',
#        ['mRNA', 'protein'],
#        'k_p*mRNA'
#    )
#
#    m['J4'] = Reaction(
#        'protein',
#        None,
#        'd_p*protein']
#    )
#
#    sbml = m.getSBML()
#
