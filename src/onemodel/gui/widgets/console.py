from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QProcess

from PyQt5 import QtGui
from PyQt5 import QtCore

from onemodel.gui.syntax_highlight import COLORS

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

        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        # self.process.start('onemodel-cli.py repl')
