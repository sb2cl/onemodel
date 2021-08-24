from PyQt5.QtWidgets import QLineEdit, QErrorMessage
from PyQt5.QtCore import QDir

class PathField:
    """ Current path field.
    """
    def __init__(self, window):
        """ Init PathField.
        """
        self.window = window
        self.field = QLineEdit()
        self.field.insert(QDir.homePath())

        self.field.textChanged.connect(self.check_path)

    def check_path(self):
        """ Check that the path is valid.
        """
        error_dialog = QErrorMessage(self.window)
        error_dialog.showMessage('Oh no!')
        error_dialog.show()
