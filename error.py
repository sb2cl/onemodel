from position import Position
from string_with_arrows import string_with_arrows

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

class IllegalCharError(Error):
    """ ILLEGALCHARERROR(ERROR)

    This error message is shown when an illegal char is processed.
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
    """ EXPECTEDCHARERROR(ERROR)

    This error message is shown when we expected a char but we did not find it.
    """
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    """ INVALIDSYNTAXERROR(ERROR)

    This error message is shown when the order of the tokens is not valid (syntax error).
    """
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

# TODO: Implement context.
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
    #self.context = context

    def as_string(self):
        result  = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return 'Traceback (most recent call last):\n' + result
