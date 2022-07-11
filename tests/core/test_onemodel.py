from xml.etree import ElementTree

from onemodel.core.onemodel import OneModel
from onemodel.core.objects.object import Object
from onemodel.core.objects.species import Species
from onemodel.core.objects.parameter import Parameter
from onemodel.core.objects.reaction import Reaction
from onemodel.core.objects.assignment_rule import AssignmentRule
from onemodel.core.objects.function import Function
from onemodel.core.scope import Scope

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

def ProteinConstitutive(scope):
   
    scope['self'] = Object()

    scope['self']['mRNA'] = Species()
    scope['self']['protein'] = Species()

    scope['self']['k_m'] = Parameter()
    scope['self']['k_m'].value = 1
    scope['self']['d_m'] = Parameter()
    scope['self']['d_m'].value = 1
    scope['self']['k_p'] = Parameter()
    scope['self']['k_p'].value = 1
    scope['self']['d_p'] = Parameter()
    scope['self']['d_p'].value = 1

    scope['self']['J1'] = Reaction()
    scope['self']['J1'].reactants = []
    scope['self']['J1'].products = ['mRNA']
    scope['self']['J1'].kinetic_law = 'k_m'

    scope['self']['J2'] = Reaction()
    scope['self']['J2'].reactants = ['mRNA']
    scope['self']['J2'].products = []
    scope['self']['J2'].kinetic_law = 'd_m*mRNA'

    scope['self']['J3'] = Reaction()
    scope['self']['J3'].reactants = ['mRNA']
    scope['self']['J3'].products = ['mRNA', 'protein']
    scope['self']['J3'].kinetic_law = 'k_p*mRNA'

    scope['self']['J4'] = Reaction()
    scope['self']['J4'].reactants = ['protein']
    scope['self']['J4'].products = []
    scope['self']['J4'].kinetic_law = 'd_p*protein'

    return scope['self']
 
def test_ex03_protein_constitutive():
    m = OneModel()
    
    m.root['ProteinConstitutive'] = Function()
    m.root['ProteinConstitutive'].argument_names = []
    m.root['ProteinConstitutive'].body = ProteinConstitutive

    scope = Scope()
    scope.push(m.root)

    m.root['A'] = m.root['ProteinConstitutive'].call(scope, [])

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
      <parameter id="A__k_m" value="1" units="per_second" constant="true"/>
      <parameter id="A__d_m" value="1" units="per_second" constant="true"/>
      <parameter id="A__k_p" value="1" units="per_second" constant="true"/>
      <parameter id="A__d_p" value="1" units="per_second" constant="true"/>
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

def ProteinInduced(scope):

    scope["self"] = scope['ProteinConstitutive'].call(scope, [])

    scope["self"]["TF"] = Species()
    scope["self"]["k_m"] = Species()

    scope["self"]["h"] = Parameter()
    scope["self"]["h"].value = 1

    scope["self"]["k_m_max"] = Parameter()
    scope["self"]["k_m_max"].value = 1

    scope["self"]["R1"] = AssignmentRule()
    scope["self"]["R1"].variable = "k_m"
    scope["self"]["R1"].math = "k_m_max*TF(TF+h)"

    return scope['self']

def test_ex05_protein_induced():
    m = OneModel()
    
    m.root['ProteinConstitutive'] = Function()
    m.root['ProteinConstitutive'].argument_names = []
    m.root['ProteinConstitutive'].body = ProteinConstitutive

    m.root['ProteinInduced'] = Function()
    m.root['ProteinInduced'].argument_names = []
    m.root['ProteinInduced'].body = ProteinInduced

    scope = Scope()
    scope.push(m.root)

    m.root['A'] = m.root['ProteinConstitutive'].call(scope, [])
    m.root['B'] = m.root['ProteinInduced'].call(scope, [])

    m.root['R1'] = AssignmentRule()
    m.root["R1"].variable = "B__TF"
    m.root["R1"].math = "A__protein"

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
      <species id="B__mRNA" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="B__protein" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="B__k_m" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
      <species id="B__TF" compartment="default_compartment" initialConcentration="0" substanceUnits="mole" hasOnlySubstanceUnits="false" boundaryCondition="false" constant="false"/>
    </listOfSpecies>
    <listOfParameters>
      <parameter id="A__k_m" value="1" units="per_second" constant="true"/>
      <parameter id="A__d_m" value="1" units="per_second" constant="true"/>
      <parameter id="A__k_p" value="1" units="per_second" constant="true"/>
      <parameter id="A__d_p" value="1" units="per_second" constant="true"/>
      <parameter id="B__d_m" value="1" units="per_second" constant="true"/>
      <parameter id="B__k_p" value="1" units="per_second" constant="true"/>
      <parameter id="B__d_p" value="1" units="per_second" constant="true"/>
      <parameter id="B__h" value="1" units="per_second" constant="true"/>
      <parameter id="B__k_m_max" value="1" units="per_second" constant="true"/>
    </listOfParameters>
    <listOfRules>
      <assignmentRule id="B__R1" variable="B__k_m">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <apply>
            <times/>
            <ci> B__k_m_max </ci>
            <apply>
              <ci> B__TF </ci>
              <apply>
                <plus/>
                <ci> B__TF </ci>
                <ci> B__h </ci>
              </apply>
            </apply>
          </apply>
        </math>
      </assignmentRule>
      <assignmentRule id="R1" variable="B__TF">
        <math xmlns="http://www.w3.org/1998/Math/MathML">
          <ci> A__protein </ci>
        </math>
      </assignmentRule>
    </listOfRules>
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
      <reaction id="B__J1" reversible="false">
        <listOfProducts>
          <speciesReference species="B__mRNA" constant="true"/>
        </listOfProducts>
        <listOfModifiers>
          <modifierSpeciesReference species="B__k_m"/>
        </listOfModifiers>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <ci> B__k_m </ci>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="B__J2" reversible="false">
        <listOfReactants>
          <speciesReference species="B__mRNA" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> B__d_m </ci>
              <ci> B__mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="B__J3" reversible="false">
        <listOfReactants>
          <speciesReference species="B__mRNA" constant="true"/>
        </listOfReactants>
        <listOfProducts>
          <speciesReference species="B__mRNA" constant="true"/>
          <speciesReference species="B__protein" constant="true"/>
        </listOfProducts>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> B__k_p </ci>
              <ci> B__mRNA </ci>
            </apply>
          </math>
        </kineticLaw>
      </reaction>
      <reaction id="B__J4" reversible="false">
        <listOfReactants>
          <speciesReference species="B__protein" constant="true"/>
        </listOfReactants>
        <kineticLaw>
          <math xmlns="http://www.w3.org/1998/Math/MathML">
            <apply>
              <times/>
              <ci> B__d_p </ci>
              <ci> B__protein </ci>
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


