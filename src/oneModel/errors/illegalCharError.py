from oneModel.errors.error import Error

class IllegalCharError(Error):
    """ ILLEGALCHARERROR(ERROR)

    This error message is shown when an illegal char is processed.
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)
