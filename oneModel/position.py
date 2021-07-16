from dataclasses import dataclass

class Position:
    """ POSITION

    This class keep track of the position in files for pin pointing errors.
    """
    idx: int
    ln: int
    col: int
    fn: str
    ftxt: str

    def __init__(self,idx, ln, col, fn, ftxt):
        """
        @brief: Constructor of Position class.
        
        @param: idx  Current index in the text.
              : ln   Current line in the text.
              : col  Current column in the text.
              : fn   Filename.
              : ftxt Text converted into one string.
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self,current_char=None):
        """ ADVANCE
        @brief: Advance one char in the text position.
        
        @param: current_char Current char read.
                
        @return: Position 
        """
        self.idx += 1
        self.col += 1

        # If newline is read
        if current_char == '\n':
            # Increase line count and reset column.
            self.ln += 1
            self.col = 0
    
        return self

    def copy(self):
        """ COPY
        @brief: Copy method
        
        @return: Copy position
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
