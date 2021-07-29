from onemodel.dsl.position import Position
from onemodel.dsl.errors.string_with_arrows import string_with_arrows

class Error:
    """ ERROR

    This class defines the base error implementation for errors.
    """

    def __init__(self, pos_start, pos_end, error_name, details):
        """
        @brief: Constructor of Error.
        
        @param: pos_start   Error start position. 
              : pos_end     Error end position.
              : error_name  Error name.
              : details     Error details to show to the user.
        """
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        """ AS_STRING
        @brief: Return the error information as a string.
        
        @return: str
        """
        result  = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
