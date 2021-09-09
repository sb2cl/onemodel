from datetime import datetime

from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase, QTextCursor
from PyQt5.QtCore import QProcess

from PyQt5 import QtGui
from PyQt5 import QtCore

from onemodel.gui.widgets.syntax_highlight import COLORS

class Console:
    """ Console Window for executing the ondemodel REPL.
    """
    def __init__(self):
        """ Constructor.
        """
        self.input = QLineEdit()
        self.output = QPlainTextEdit()

        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.input.setFont(fixedfont)
        self.output.setFont(fixedfont)

        css  = 'QPlainTextEdit{\n'
        css += f'color: {COLORS["base03"]};\n'
        css += f'background-color: {COLORS["base06"]};\n'
        css += '}'
        self.output.setStyleSheet(css)

    def print(self, string):
        """ Print the string into the console.
        """
        self.output.appendPlainText(string)
        self.output.moveCursor(QTextCursor.End)

    def printCommand(self, string):
        """ Print a command into the console with time and >>.
        """

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        string = f'[{current_time}]>> ' + string
        self.print(string)

#    def process_input(self):
#        """ Process the command in the input box.
#        """
#        text = self.input.text()
#        self.input.setText('')
#
#        self.print(text)
#        text += '\n'
#        self.process.write(text.encode())

