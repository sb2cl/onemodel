import json

import tatsu
from tatsu.walkers import NodeWalker

from onemodel.utils.setup_input_history import setup_input_history
from onemodel.dsl.onemodel_model import OneModelWalker

class Repl:
    """ REPL

    REPL implements the Read-Evaluate-Print-Loop for onemodel.
    """
    def __init__(self):
        """ __INIT__
        @brief: Init REPL
        
        @return: REPL
        """
        self.init_global_symbol_table()
    
    def init_global_symbol_table(self):
        """ INIT_GLOBAL_SYMBOL_TABLE
        @brief: Inits the symbol table
        
        @return: SymbolTable
        """
        pass
       
    def run(self):
        """ RUN
        @brief: Run the REPL 

        @return: result Result value. 
        """
        setup_input_history()
        continue_loop = True

        # Load the parser.
        grammar = open('/home/nobel/Sync/python/workspace/onemodel/src/onemodel/dsl/onemodel_model.ebnf').read()
        parser = tatsu.compile(grammar, asmodel=True)
        
        # Init the model walker.
        walker = OneModelWalker()

        while continue_loop:
            # 1. READ
            text = input('onemodel> ')
            if text.strip() == "": continue

            # 2. EVALUATE

            # Generate the ast model.
            model = parser.parse(text)

            # Walk the ast model.
            result = walker.walk(model)
            error = None
            should_exit = False

            # 3. PRINT
            if error:
                print(error.as_string())
            elif result:
                print(result)

            # 4. LOOP
            if should_exit:
                continue_loop = False   
