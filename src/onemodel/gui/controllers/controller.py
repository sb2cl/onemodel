from os import path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Controller(QObject):

    def __init__(self, model):
        super().__init__()
        self._model = model

    @pyqtSlot(str)
    def current_path_changed(self, new_path):
        """ Change the current path in the model.

        Returns:
            error: bool
                True if the new_path is not valid.
        """

        if path.isdir(new_path):
            self._model.current_path = new_path
            return False
        else:
            return True
