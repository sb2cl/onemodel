import os
import readline
import atexit
from importlib.metadata import version

import onemodel
from onemodel.onemodel_walker import OneModelWalker


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

            result = self.evaluate(text)
            self.print(result)
            exit_loop = False

    def read(self):
        """Read the input from user."""

        result = input(">>> ")

        if result.strip() == "":
            result = None

        return result

    def evaluate(self, text):
        """Evaluate the user input."""

        result, ast = self.onemodel_walker.run(text)
        return result

    def print(self, text):
        """Print the result."""

        result = text

        if not result is None:
            print(result)

        return result

    def print_welcome_message(self): 

        print(f"OneModel v{version('onemodel')}")
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
