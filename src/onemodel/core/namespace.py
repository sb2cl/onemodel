class Namespace:
    """Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int
        Description of arg1
    arg2 : str
        Description of arg2

    Returns
    -------
    bool
        Description of return value

    See Also
    --------
    otherfunc : some related other function

    Examples
    --------
    These are written in doctest format, and should illustrate how to
    use the function.

    >>> a=[1,2,3]
    >>> print [x + 3 for x in a]
    [4, 5, 6]
    """
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
