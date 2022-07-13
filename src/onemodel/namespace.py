class Namespace(dict):
    """The Namespace links names with objects.
    
    Notes 
    -----
    The Namespace class is just a wrapper of the Python `dict` class. We could
    have used Python dictionaries directly to implement the Namespace and avoid
    defining this class. However, we think it is easier to understand the code
    if we explicitly specify the Namespace class. However, the result is that
    this class is just an extension of the Python dictionary class with some
    extra methods.  
    """

    def is_empty(self):
        """Returns True if the Namespace is empty, and False otherwise.
        """
        return not bool(self)
