from os import path

from PyQt5.QtWidgets import QLineEdit

class PathField(QLineEdit):
    """ Current path field.
    """
    def __init__(self, window):
        """ Init PathField.
        """
        super().__init__()

        self.window = window
        # self.field = QLineEdit()

        self.returnPressed.connect(self.update_path)
        self.editingFinished.connect(window.restore_path)

    def update_path(self):
        """ Update the path.
        """
        new_path = self.text()
        self.window.set_path(new_path)
