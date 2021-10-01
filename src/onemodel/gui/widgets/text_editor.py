from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFontDatabase
from PyQt5 import QtCore, QtWidgets

from onemodel.gui.widgets.syntax_highlight import OneModelHighlighter, COLORS
    
class TextEditor(QPlainTextEdit):
    """ Main file text editor of onemodel-gui.
    """
    def __init__(self,parent=None):
        """ Initialize the text editor.
        """
        super(TextEditor,self).__init__(parent=None)

        # Set font.
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.setFont(fixedfont)

        css  = 'QPlainTextEdit{\n'
        css += f'color: {COLORS["base07"]};\n'
        css += f'background-color: {COLORS["base00"]};\n'
        css += '}'
        self.setStyleSheet(css)

        self.highlight = OneModelHighlighter(self.document())
        self.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Tab:
            tc = self.textCursor()
            tc.insertText("  ")
            return
        else:
            super().keyPressEvent(event)

    def open_file(self, file_path):
        with open(file_path, 'rU') as f:
            # Read the file
            text = f.read()
            self.setPlainText(text)
