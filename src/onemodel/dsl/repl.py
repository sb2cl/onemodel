import json
from importlib_resources import files

import tatsu
from tatsu.walkers import NodeWalker

from onemodel.dsl.onemodel_walker import OneModelWalker
from onemodel.dsl.context import Context

class Repl:
    """ REPL

    REPL implements the Read-Evaluate-Print-Loop for onemodel.
    """
    def __init__(self):
        """ __INIT__
        @brief: Init REPL
        
        @return: REPL
        """
        pass
      
    def run(self):
        """ RUN
        @brief: Run the REPL 

        @return: result Result value. 
        """
        self.setup_input_history()
        continue_loop = True

        # Init the model walker.
        walker = OneModelWalker('repl')

        while continue_loop:
            # 1. READ
            text = input('onemodel> ')
            if text.strip() == "": continue

            # 2. EVALUATE
            try:
                result = walker.run(text)
            except Exception as e:
                print(str(e))
                continue

            error = None
            should_exit = False

            # 3. PRINT
            if error:
                print(error.as_string())
            elif result != None:
                if type(result) == str:
                    print("'" + result + "'")
                else:
                    print(result)

            # 4. LOOP
            if should_exit:
                continue_loop = False   
    
    def setup_input_history():
    """  
    @brief: Setup the history for input() command.
    
    @return: None
    """
    import atexit
    import os
    import readline

    histfile = os.path.join(os.path.expanduser("~"), ".onemodel_history")
    try:
        readline.read_history_file(histfile)
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length(1000)
    except FileNotFoundError:
        pass

    atexit.register(readline.write_history_file, histfile)

