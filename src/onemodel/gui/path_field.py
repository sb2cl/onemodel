from os import path
from PyQt5.QtWidgets import QLineEdit, QMessageBox
from PyQt5.QtCore import QDir

class PathField:
    """ Current path field.
    """
    def __init__(self, window):
        """ Init PathField.
        """
        self.window = window
        self.field = QLineEdit()

        self.field.setText(QDir.homePath())
        self.last_valid_path = self.field.text()

        self.field.returnPressed.connect(self.check_path)
        self.field.editingFinished.connect(self.restore_path)

    def set_path(self, path):
        """ Set a new path.
        """
        self.last_valid_path = self.field.text()
        self.field.setText(path)
        self.dirTree.tree.setRootIndex(self.dirTree.model.index(path))

    def check_path(self):
        """ Check that the path is valid.
        """
        # Check if the new path existis.
        if path.isdir(self.field.text()):
            # Update the paths.
            self.set_path(self.field.text())

        else:
            # If not, show error message.
            title = 'Error Changing Folder'
            msg = f'Cannot find folder "{self.field.text()}".\n'
            msg += 'Check the spelling and try again.'

            dialog = QMessageBox.about(self.window, title, msg) 

    def restore_path(self):
        """ Restore the path to the last valid path.
        """
        self.field.setText(self.last_valid_path)
