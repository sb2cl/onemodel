from oneModel.errors.error import Error

class InvalidSyntaxError(Error):
    """ INVALIDSYNTAXERROR(ERROR)

    This error message is shown when the order of the tokens is not valid (syntax error).
    """
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
