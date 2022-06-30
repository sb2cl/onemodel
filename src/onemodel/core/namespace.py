class Namespace:
    def __init__(self, parent):
        self.parent = parent
        self.symbols = {}

    def set(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        if name in self.names():
            return self.symbols.get(name, None)

        if self.parent:
            return self.parent.get(name)

        return None

    def delete(self, name):
        return self.symbols.pop(name, None)

    def names(self):
        return list(self.symbols.keys())

    def items(self):
        result = []

        for name in self.names():
            result.append((name, self.symbols[name]))

        return result

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __delitem__(self, name):
        return self.delete(name)
