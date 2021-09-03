from os import path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Controller(QObject):

    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot(str)
    def change_current_path(self, new_path):
        """ Change the current path in the model.

        Returns:
            error: bool
                True if the new_path is not valid.
        """
        # Check if the path is valid.
        if path.isdir(new_path):
            # Update current path.
            self._model.current_path = new_path
            return False

        else:
            # Path is not valid, do not update it.
            return True

    @pyqtSlot(str)
    def change_file_path(self, new_file_path):
        self._model.file_path = new_file_path

    def change_is_file_modified(self, value):
        self._model.is_file_modified = value

    @pyqtSlot(str)
    def open_file(self, file_path):
        # TODO: Check if there was a not saved previous open file.
        self.change_file_path(file_path)

    @pyqtSlot()
    def save_file_to_path(self, text, path):

        with open(path, 'w') as f:
            f.write(text)
        
        self.change_is_file_modified(False)

    @pyqtSlot()
    def execute_cmd(self, cmd):
        self._model._onemodel_cli.start(cmd)
