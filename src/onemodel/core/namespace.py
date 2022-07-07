class Namespace:
    def __init__(self):
        self.symbols = {}

    def set(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        return self.symbols.get(name, None)

    def delete(self, name):
        return self.symbols.pop(name, None)

    def names(self):
        return list(self.symbols.keys())

    def items(self):
        result = []

        for name in self.names():
            result.append((name, self.symbols[name]))

        return result

    def is_empty(self):
        return not bool(self.symbols)

    def has_name(self, name):
        if name in self.names():
            return True
        else:
            return False

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __delitem__(self, name):
        return self.delete(name)
