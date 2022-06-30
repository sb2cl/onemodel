from libsbml import Species, parseL3Formula

from onemodel.core.utils.check import check
from onemodel.core.utils.get_ast_names import get_ast_names
from onemodel.core.objects.object import Object


class Reaction(Object):

    def __init__(self):
        super().__init__()
        self.reactants = []
        self.products = []
        self.kinetic_law = ""
        self.reversible = False

    def add_to_SBML_model(self, name, model):
        # List of species involved as reactans or products in the reaction.
        species_involved = []

        r = self.create_SBML_reaction(name, model)
        self.create_SBML_reaction_reactants(r, species_involved)
        self.create_SBML_reaction_products(r, species_involved)
        self.create_SBML_reaction_kinetic_law(r, model, species_involved)

    def create_SBML_reaction(self, name, model):
        r = model.createReaction()

        check(
            r, 
            f"create reaction {name}"
        )

        check(
            r.setId(name), 
            f"set reaction id {name}"
        )

        check(
            r.setReversible(self.reversible), 
            "set reaction reversibility flag"
        )

        return r

    def create_SBML_reaction_reactants(self, reaction, species_involved):

        for name in self.reactants:
            if name == None:
                continue

            reactant = reaction.createReactant()

            check(
                reactant, 
                "create reactant"
            )

            check(
                reactant.setSpecies(name), 
                f"assign reactant species {name}"
            )

            check(
                reactant.setConstant(True), 
                f'set "constant" on species {name}'
            )

            species_involved.append(name)

    def create_SBML_reaction_products(self, reaction, species_involved):

        for name in self.products:
            if name == None:
                continue

            species_ref = reaction.createProduct()

            check(
                species_ref, 
                "create product"
            )

            check(
                species_ref.setSpecies(name), 
                "assign product species"
            )

            check(
                species_ref.setConstant(True), 
                f'set "constant" on species {name}'
            )

            species_involved.append(name)

    def create_SBML_reaction_kinetic_law(self, reaction, model, species_involved):

        # aux = math_2_fullname(self.kinetic_law, self.definition_context)
        math_ast = parseL3Formula(self.kinetic_law)

        check(
            math_ast, 
            "create AST for rate expression"
        )

        kinetic_law = reaction.createKineticLaw()

        check(
            kinetic_law, 
            "create kinetic law"
        )

        check(
            kinetic_law.setMath(math_ast), 
            "set math on kinetic law"
        )

        # Sometimes a species appears in the kinetic rate formula of a reaction 
        # but is itself neither created nor destroyed in that reaction
        names = get_ast_names(math_ast)
        names_modifier = []

        for name in names:
            elem = model.getElementBySId(name)

            if type(elem) != Species:
                continue

            if name in species_involved:
                continue

            names_modifier.append(name)

        for item in names_modifier:
            if item == None:
                continue

            modifier_ref = reaction.createModifier()

            check(
                modifier_ref, 
                "create modifier"
            )

            check(
                modifier_ref.setSpecies(item), 
                "assign modifier species"
            )

