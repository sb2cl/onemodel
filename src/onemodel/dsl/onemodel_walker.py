import sys

import tatsu
from tatsu.walkers import NodeWalker
from libsbml import *
 
def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value == None:
        raise SystemExit(
            'LibSBML returned a null value trying to ' + message + '.'
        )
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        else:
            err_msg = 'Error encountered trying to ' + message + '.' \
                 + 'LibSBML returned error code ' + str(value) + ': "' \
                 + OperationReturnValue_toString(value).strip() + '"'
        raise SystemExit(err_msg)
    else:
        return

def getAstNames(ast):
    """ Returns the user defined names in a MathML ast.
    """
    names = []

    if ast.isName():
        names.append(ast.getName())

    for i in range(ast.getNumChildren()):
        child = ast.getChild(i)
        child_names = getAstNames(child)

        for item in child_names:
            names.append(item)

    return names

class SymbolTable:
  def __init__(self, parent=None):
    self.symbols = {}
    self.parent = parent

  def get(self, name):
    value = self.symbols.get(name, None)

    if value == None and self.parent:
        return self.parent.get(name)
    
    if value == None:
        raise NameError(f"NameError: name '{name}' is not defined")
    
    return value

  def set(self, name, value):
    self.symbols[name] = value

  def remove(self, name):
    del self.symbols[name]


class OneModelWalker(NodeWalker):
    def __init__(self, model_name):
        # Create the symbol table, we will store all objects here.
        # libSBML objects will be stored both in the symbol table and in the
        # model.
        self.symbol_table = SymbolTable()

        # Create and empty SBMLDocument object.
        try:
            self.document = SBMLDocument(3, 2)
        except ValueError:
            raise SystemExit('Could not create SBMLDocument object')

        # Create the basic Model object inside the SBMLDocument object.
        self.model = self.document.createModel()
        check(self.model, 'create model')
        check(self.model.setName(model_name), 'set model name')
        check(self.model.setId(model_name), 'set model id')
        check(self.model.setTimeUnits('second'), 'set model-wide time units')
        check(self.model.setExtentUnits('mole'), 'set model units of extent')
        check(self.model.setSubstanceUnits('mole'), 'set model substance units')

        # Create a unit definition we will need later.
        per_second = self.model.createUnitDefinition()
        check(per_second, 'create unit definition')
        check(per_second.setId('per_second'),'set unit definition id')

        unit = per_second.createUnit()
        check(unit, 'create unit on per_second')
        check(unit.setKind(UNIT_KIND_SECOND),'set unit kind')
        check(unit.setExponent(-1), 'set unit exponent')
        check(unit.setScale(0), 'set unit scale')
        check(unit.setMultiplier(1), 'set unit multiplier')

        # Create a default_compartment.
        c = self.model.createCompartment()

        self.symbol_table.set('default_compartment', c)

        check(c, 'create default compartment')
        check(c.setId('default_compartment'), 'set compartment id')
        check(c.setConstant(True), 'set compartment "constant"')
        check(c.setSize(1), 'set compartment "size"')
        check(c.setSpatialDimensions(3), 'set compartment dimensions')
        check(c.setUnits('litre'), 'set compartment size units')

    def checkConsistency(self):
        if self.document.checkConsistency():
            self.document.printErrors()

    def getSBML(self):
        self.checkConsistency()
        return writeSBMLToString(self.document)

    def walk_object(self, node):
        return node

    def walk_list(self, nodes):
        results = []

        for node in nodes:
            results.append(self.walk(node))

        if len(results) == 1:
            results = results[0]

        return results

    def walk_AccessIdentifier(self, node):
        name = node.name
        value = self.symbol_table.get(name)

        return value

    def walk_Species(self, node):
        name = node.name
        value = self.walk(node.value)

        if value == None:
            value = 0

        s = self.model.createSpecies()

        self.symbol_table.set(name, s)

        check(
            s, 
            f'create species {name}'
        )

        check(
            s.setId(name), 
            f'set species {name} id'
        )

        check(
            s.setCompartment('default_compartment'), 
            f'set species {name} in default_compartment'
        )

        check(
            s.setConstant(False), 
            f'set "constant" attribute on {name}'
        )

        check(
            s.setInitialConcentration(value), 
            f'set initial amount for {name}'
        )

        check(
            s.setSubstanceUnits('mole'), 
            f'set substance units for {name}'
        )

        check(
            s.setBoundaryCondition(False),
            f'set "boundaryCondition" on {name}'
        )

        check(
            s.setHasOnlySubstanceUnits(False),
            f'set "hasOnlySubstanceUnits" on {name}'
        )

        self.checkConsistency()

        return s

    def walk_Parameter(self, node):
        name = node.name
        value = self.walk(node.value)

        if value == None:
            value = 0

        if not type(value) in (int, float):
            print('Error: value must be int or float')
            return
            
        p = self.model.createParameter()

        self.symbol_table.set(name, p)

        check(
            p,
            f'create parameter {name}'
        )

        check(
            p.setId(name),
            f'set parameter {name} id'
        )

        check(
            p.setConstant(True),
            f'set parameter {name} "constant"'
        )

        check(
            p.setValue(value),
            f'set parameter {name} value'
        )

        check(
            p.setUnits('per_second'),
            f'set parameter {name} units'
        )
 
        self.checkConsistency()

        return p

    def walk_Reaction(self, node):
        name = node.name
        reactants = node.reactants
        products = node.products
        kinetic_law_str = node.kinetic_law

        if type(reactants) != list:
            reactants = [reactants] 

        if type(products) != list:
            products = [products] 

        if name == None:
            name = f'_J{self.model.getNumReactions()}'

        # Save here a list of ids of the species defined as reactans or products.
        names_defined = []

        # Create reaction.
        r = self.model.createReaction()

        self.symbol_table.set(name, r)

        check(
            r,
            f'create reaction {name}'
        )

        check(
            r.setId(name), 
            f'set reaction id {name}'
        )

        check(
            r.setReversible(False), 
            'set reaction reversibility flag'
        )

        # Create reactants.
        for item in reactants:
            if item == None: continue

            species_ref = r.createReactant()

            check(
                species_ref,
                'create reactant'
            )

            check(
                species_ref.setSpecies(item),
                f'assign reactant species {item}'
            )

            check(
                species_ref.setConstant(True),
                f'set "constant" on species {item}'
            )

            names_defined.append(item)

        # Create products.
        for item in products:
            if item == None: continue

            species_ref = r.createProduct()

            check(
                species_ref,
                'create product'
            )

            check(
                species_ref.setSpecies(item),
                'assign product species'
            )

            check(
                species_ref.setConstant(True),
                f'set "constant" on species {item}'
            )

            names_defined.append(item)
 
        # Create kinetic law.
        math_ast = parseL3Formula(kinetic_law_str)

        check(
            math_ast,
            'create AST for rate expression'
        )
 
        kinetic_law = r.createKineticLaw()

        check(
            kinetic_law,
            'create kinetic law'
        )

        check(
            kinetic_law.setMath(math_ast),
            'set math on kinetic law'
        )

        # Create modifier species reference.
        names = getAstNames(math_ast)
        names_modifier = []

        for name in names:
            elem = self.model.getElementBySId(name)

            if type(elem) != Species: 
                continue

            if name in names_defined:
                continue

            names_modifier.append(name)

        for item in names_modifier:
            if item == None: continue

            modifier_ref = r.createModifier()

            check(
                modifier_ref,
                'create modifier'
            )

            check(
                modifier_ref.setSpecies(item),
                'assign modifier species'
            )

        self.checkConsistency()

        return r

    def walk_RateRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.model.getNumRules()}'

        math_ast = parseL3Formula(math)

        r = self.model.createRateRule()

        self.symbol_table.set(name, r)

        check(
            r,
            f'create rate rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set rate rule id {name}'
        )

        check(
            r.setVariable(variable),
            f'set variable on rate rule {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on rate rule {name}'
        )

        return r

    def walk_AssignmentRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.model.getNumRules()}'

        math_ast = parseL3Formula(math)

        r = self.model.createAssignmentRule ()

        self.symbol_table.set(name, r)

        check(
            r,
            f'create assignment rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set assignment rule id {name}'
        )

        check(
            r.setVariable(variable),
            f'set variable on assignment rule {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on assignment rule {name}'
        )

        return r

    def walk_AlgebraicRule(self, node):
        name = node.name
        variable = node.variable
        math = node.math

        if name == None:
            name = f'_R{self.model.getNumRules()}'

        # We have to pass the variable to the other equation side.
        math = f'{variable} - ({math})'

        math_ast = parseL3Formula(math)

        r = self.model.createAlgebraicRule ()

        self.symbol_table.set(name, r)

        check(
            r,
            f'create algebraic rule {name}'
        )

        check(
            r.setIdAttribute(name), 
            f'set algebraic rule id {name}'
        )

        check(
            r.setMath(math_ast),
            f'set math on algebraic rule {name}'
        )

        return r

        print(name)
        print(variable)
        print(math)

    def walk_PrintSBML(self, node):
        print(self.getSBML())
        return

if __name__ == '__main__':
    print(create_model())
