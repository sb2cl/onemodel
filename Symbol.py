class Symbol:
    def __init__(self):
        self.name = "null"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, n):
        if(type(n) != str):
            raise ValueError("'%s' has not a valid type for the name. Use string type instead." % str(n))
        self._name = n
