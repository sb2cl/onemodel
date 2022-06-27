class Object:
    def __init__(self):
        pass

    def add_to_SBML(self):
        raise Exception(
            f'Class "{type(self).__name__}" has not defined add_to_SBML method.'
        )
