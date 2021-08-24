from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase

class ConsoleWindow:
    """ Console Window for executing the ondemodel REPL.
    """
    def __init__(self, window):
        """ Constructor.
        """
        self.window = window

        self.input = QLineEdit()
        self.output = QPlainTextEdit()


        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.input.setFont(fixedfont)
        self.output.setFont(fixedfont)

        self.input.returnPressed.connect(self.process_input)

    def process_input(self):
        """ Process the command in the input box.
        """
        self.print('>> ' + self.input.text())
        self.input.setText('')

    def print(self, string):
        """ Print the string into the console.
        """
        self.output.appendPlainText(string)
