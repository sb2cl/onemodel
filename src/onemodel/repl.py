import os
import readline
import atexit
# TODO: use this again
# from importlib.metadata import version 

import onemodel
from onemodel.onemodel_walker import OneModelWalker
from tatsu.exceptions import FailedLeftRecursion

def shell():
    repl = Repl()
    repl.run()

    return repl.onemodel

class Repl:
    """Read-Evaluate-Print-Loop for OneModel."""

    def __init__(self):
        self.onemodel_walker = OneModelWalker()
        self.onemodel = self.onemodel_walker.onemodel
        self.setup_input_history()

    def run(self):
        """Execute the repl."""

        self.print_welcome_message()

        exit_loop = False
        while not exit_loop:
            text = self.read()

            if text is None:
                continue

            try:
                result = self.evaluate(text)
                self.print(result)
            except Exception as e:
                print(type(e).__name__ + ': ' + str(e))

            exit_loop = self.onemodel["__exit__"]

    def read(self):
        """Read the input from user."""

        result = input("one> ")

        if result.strip() == "":
            result = None

        return result

    def evaluate(self, text):
        """Evaluate the user input."""

        result, ast = self.onemodel_walker.run(text)
        return result

    def print(self, evaluation_result):
        """Print the result."""

        if isinstance(evaluation_result, list):
            result = None
            for item in evaluation_result:
                printed = self.printResult(item)
                if result is None:
                    result = str(printed)
                else:
                    result += '\n' + str(printed)
            return result

        result = self.printResult(evaluation_result)

        return result

    def printResult(self, result):
        if result is None:
            return

        if isinstance(result, str):
            print('"' + result + '"')
            return '"' + result + '"'

        print(result)
        return(result)

    def print_welcome_message(self): 

        print(f"OneModel v1.0.0")
        print("Documentation: https://onemodel.readthedocs.io/")
        print()

    def setup_input_history(self):
        """Setup the history for input() function."""

        histfile = os.path.join(os.path.expanduser("~"), ".onemodel_history")
        try:
            readline.read_history_file(histfile)
            # default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, histfile)
