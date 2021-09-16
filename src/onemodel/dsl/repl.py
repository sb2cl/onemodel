import json
from importlib_resources import files

import tatsu
from tatsu.walkers import NodeWalker

from onemodel.utils.setup_input_history import setup_input_history
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
        setup_input_history()
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
