from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFontDatabase

from onemodel.gui.syntax_highlight import OneModelHighlighter, COLORS

class TextEditor:
    """ Main file text editor of onemodel-gui.
    """
    def __init__(self):
        """ Initialize the text editor.
        """
        # Create a Plain Text Edit.
        self.editor = QPlainTextEdit()

        # Set font.
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        css  = 'QPlainTextEdit{\n'
        css += f'color: {COLORS["base07"]};\n'
        css += f'background-color: {COLORS["base00"]};\n'
        css += '}'
        self.editor.setStyleSheet(css)

        self.highlight = OneModelHighlighter(self.editor.document())
        self.editor.show()
