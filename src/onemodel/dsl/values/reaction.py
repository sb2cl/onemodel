from libsbml import parseL3Formula, Species

from onemodel.dsl.values.value import Value
from onemodel.dsl.utils import check, getAstNames, math_2_fullname

class Reaction(Value):
    """ SBML Reaction.
    """
    def __init__(self):
        super().__init__()
        self.reactants = []
        self.products = []
        self.kinetic_law = ''
        self.reversible = False

    def add_value_to_model(self, name, model):
        """ Add this value to the SBML model.

        Arguments:
            name: str
                Name of this value.
            model: LibSBML model
                Model to include this value.
        """
        # Save here a list of ids of the species defined as reactans or products.
        names_defined = []

        # Create reaction.
        r = model.createReaction()

        check(
            r,
            f'create reaction {name}'
        )

        check(
            r.setId(name), 
            f'set reaction id {name}'
        )

        check(
            r.setReversible(self.reversible), 
            'set reaction reversibility flag'
        )

        # Create reactants.
        for item in self.reactants:
            if item == None: continue

            item_name = item.getFullname()

            species_ref = r.createReactant()

            check(
                species_ref,
                'create reactant'
            )

            check(
                species_ref.setSpecies(item_name),
                f'assign reactant species {item_name}'
            )

            check(
                species_ref.setConstant(True),
                f'set "constant" on species {item_name}'
            )

            names_defined.append(item)

        # Create products.
        for item in self.products:
            if item == None: continue

            item_name = item.getFullname()

            species_ref = r.createProduct()

            check(
                species_ref,
                'create product'
            )

            check(
                species_ref.setSpecies(item_name),
                'assign product species'
            )

            check(
                species_ref.setConstant(True),
                f'set "constant" on species {item_name}'
            )

            names_defined.append(item)
 
        # Create kinetic law.
        aux = math_2_fullname(self.kinetic_law, self.definition_context)
        math_ast = parseL3Formula(aux)

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
            elem = model.getElementBySId(name)

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

    def __str__(self):
        reaction = ''

        #for item in self.reactants:
        #    if item == None: continue
        #    reaction += item + '+'

        #if self.reactants != []:
        #    if reaction[-1] == '+':
        #        reaction = reaction[:-1]

        #reaction += '->'

        #for item in self.products:
        #    if item == None: continue
        #    reaction += '+' + item

        #if self.products != []:
        #    if reaction[-1] == '+':
        #        reaction = reaction[:-1]

        #reaction += ';' + self.kinetic_law

        return f'<reaction>'
    
    def __repr__(self):
        return self.__str__()
