from onemodel.dsl.values.value import Value
from onemodel.dsl.context import Context

class Object(Value):
    """ OneModel Object.
    """
    def __init__(self):
        """ Initialize Object.
        """
        # In this context are the values associated of this object.
        self.context = Context()

        # Set 'self' to reference this value.
        self.context.set('self', self)

        super().__init__()

    def set_definition_context(self, context=None):
        """ Set the context where the value is defined.
        """
        # Save the definition context as the parent of self.context.
        self.context.parent = context

        super().set_definition_context(context)
        

    def add_value_to_model(self, name, model):
        """ Add this value to the SBML model.

        Arguments:
            name: str
                Name of this value.
            model: LibSBML model
                Model to include this value.
        """
        for local in self.context.locals:
            value = self.context.get(local)
            value.namespace = f'{name}__'
            value.add_value_to_model(local, model)

    def __str__(self):
        return f"<object>"

    def __repr__(self):
        return self.__str__()
