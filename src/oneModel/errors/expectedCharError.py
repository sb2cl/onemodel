from oneModel.errors.error import Error

class ExpectedCharError(Error):
    """ EXPECTEDCHARERROR(ERROR)

    This error message is shown when we expected a char but we did not find it.
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)
