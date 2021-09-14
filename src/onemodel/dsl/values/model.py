from onemodel.dsl.values.value import Value

class Model(Value):
    """ Definition of OneModel models.
    """
    def __init__(self, name, body_node):
        """ Initialize Model.
        """
        self.name = name
        self.body = body_node

    def __str__(self):
         return f"<model {self.name}>"

    def __repr__(self):
         return self.__str__()
