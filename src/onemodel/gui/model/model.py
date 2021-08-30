import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    current_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._current_path = QtCore.QDir.homePath() + '/Sync'

    @property
    def current_path(self):
        return self._current_path

    @current_path.setter
    def current_path(self, value):
        # Save new current_path.
        self._current_path = value

        # Change the working path of the app.
        os.chdir(value)

        # Update in model is reflected in view by sending a signal to view.
        self.current_path_changed.emit(value)
