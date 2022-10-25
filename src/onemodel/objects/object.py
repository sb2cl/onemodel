from onemodel.namespace import Namespace

class Object(Namespace):
    """This class defines the base Object for building models. 

    Everything in OneModel (parameters, species, reactions, etc.) is an
    objects. This clases is the base for implementing the rest of
    OneModel elements.
    """

    def __init__(self):
        super().__init__()

        self['__doc__'] = ""

    def add_to_SBML_model(self, name, scope, SBML_model):
        """Include this object into a SBML model. 

        self['__doc__'] : :obj:`str`
            Documentation of this object.

        Parameters
        ----------
        name : :obj:`str`
            Name used to link to this object in a given scope.

        scope : :obj:`Scope`
            Scope to look for the object using the `name`.

        SBML_model : 
            The SBML model where we have to include the Object.

        Notes
        -----
        * One unique Object can be included one o more times into a SBML model
          under different names.
        * This method has to be overwritten by the classes that extend this
          class.
        """
        pass

    def __repr__(self):
        result = "<object"
        result += ">"

        return result
