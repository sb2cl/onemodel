from onemodel.onemodel_walker import OneModelWalker


class Repl:
    """Read-Evaluate-Print-Loop for OneModel."""

    def __init__(self):
        self.onemodel_walker = OneModelWalker()
        self.onemodel = self.onemodel_walker.onemodel

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


if __name__ == '__main__':
    repl = Repl()
    repl.run()
