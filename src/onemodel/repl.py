import os
import readline
import atexit

from onemodel.onemodel_walker import OneModelWalker


class Repl:
    """Read-Evaluate-Print-Loop for OneModel."""

    def __init__(self):
        self.onemodel_walker = OneModelWalker()
        self.onemodel = self.onemodel_walker.onemodel
        self.setup_input_history()

    def run(self):
        """Execute the repl."""
        exit_loop = False

        while not exit_loop:
            text = self.read()

            if text is None:
                continue

            result = self.evaluate(text)
            self.print(result)
            exit_loop = False

    def read(self):
        result = input(">>> ")

        if result.strip() == "":
            result = None

        return result

    def evaluate(self, text):
        result, ast = self.onemodel_walker.run(text)
        return result

    def print(self, text):
        result = text

        print(result)
        return result

    def setup_input_history(self):
        """
        @brief: Setup the history for input() command.

        @return: None
        """

        histfile = os.path.join(os.path.expanduser("~"), ".onemodel_history")
        try:
            readline.read_history_file(histfile)
            # default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, histfile)

if __name__ == '__main__':
    repl = Repl()
    repl.run()
