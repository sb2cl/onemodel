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
        # Save here a list of ids of the species defined as reactans or products.
        species_involved = []

        # Create reaction.
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

        # Create reactants.
        for item in self.reactants:
            if item == None:
                continue

            item_name = item

            species_ref = r.createReactant()

            check(
                species_ref, 
                "create reactant"
            )

            check(
                species_ref.setSpecies(item_name), 
                f"assign reactant species {item_name}"
            )

            check(
                species_ref.setConstant(True), 
                f'set "constant" on species {item_name}'
            )

            species_involved.append(item)

        # Create products.
        for item in self.products:
            if item == None:
                continue

            item_name = item

            species_ref = r.createProduct()

            check(
                species_ref, 
                "create product"
            )

            check(
                species_ref.setSpecies(item_name), 
                "assign product species"
            )

            check(
                species_ref.setConstant(True), 
                f'set "constant" on species {item_name}'
            )

            species_involved.append(item)

        # Create kinetic law.
        # aux = math_2_fullname(self.kinetic_law, self.definition_context)
        math_ast = parseL3Formula(self.kinetic_law)

        check(
            math_ast, 
            "create AST for rate expression"
        )

        kinetic_law = r.createKineticLaw()

        check(
            kinetic_law, 
            "create kinetic law"
        )

        check(
            kinetic_law.setMath(math_ast), 
            "set math on kinetic law"
        )

        # Create modifier species reference.
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

            modifier_ref = r.createModifier()

            check(
                modifier_ref, 
                "create modifier"
            )

            check(
                modifier_ref.setSpecies(item), 
                "assign modifier species"
            )
