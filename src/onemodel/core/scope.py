class ScopeError(Exception):
    """Base error class for scope errors. """
    pass

class ScopeIsEmptyError(Exception):
    """Raised when pop() an empty Scope. """
    pass

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
            raise ScopeIsEmptyError

    def peek(self):
        if self.namespaces:
            return self.namespaces[-1]
        else:
            return None

    def set(self, name, value):
        self.peek()[name] = value

    def get(self, name):
        for namespace in reversed(self.namespaces):
            value = namespace[name]

            if value != None:
                return value

        return None

    def get_fullname(self, name):
        namespace_with_the_name = None

        for namespace in reversed(self.namespaces):
            if namespace[name] != None:
                namespace_with_the_name = namespace

        i = 0
        basename = ""
        for namespace in self.namespaces:
            basename += self.identifiers[i] + "__"
            i += 1
        
        fullname = basename + name

        return fullname

    def __setitem__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)
