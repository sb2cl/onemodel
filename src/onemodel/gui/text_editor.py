from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtGui import QFontDatabase

class TextEditor:
    """ Main file text editor of onemodel-gui.
    """
    def __init__(self):
        """ Initialize the text editor.
        """
        # Create a Plain Text Edit.
        self.editor = QPlainTextEdit()

        # Set the font.
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)
