class Scope:

    def __init__(self):
        # List with the namespaces in the scope.
        self.namespaces = []
        # List with the identifiers of each namespace.
        self.identifiers = []

    def push(self, aNamespace, aIndentifier=""):
        self.namespaces.append(aNamespace)
        self.identifiers.append(aIndentifier)

    def pop(self):
        if self.namespaces:
            self.namespaces.pop()
            self.identifiers.pop()
        else:
            raise Exception("Scope is empty")

    def peek(self):
        if self.namespaces:
            return self.namespaces[-1]
        else:
            return None

    def set(self, name, value):
        self.peek()[name] = value

    def get(self, name):
        for namespace in reversed(self.namespaces):
            if name in namespace:
                return namespace[name]

        return None

    def get_fullname(self, name):

        i = len(self.namespaces)
        for namespace in reversed(self.namespaces):
            if name in namespace:
                break
            i -= 1
        position_namespace_has_name = i

        basename = ""
        i = 0
        while i < position_namespace_has_name:
            if self.identifiers[i] != "":
                basename += self.identifiers[i] + "__"
            i += 1
        
        fullname = basename + name

        return fullname

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)
