import os

from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    current_path_changed = pyqtSignal(str)
    file_path_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Current working path of the app.
        self._current_path = QtCore.QDir.homePath() + '/Sync'

        # Current open file in the text editor.
        # If None, we don't have a file (or creating new).
        self._file_path = None

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

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, value):
        self._file_path = value
        self.file_path_changed.emit(value)


