from os import path

from PyQt5.QtWidgets import QFileSystemModel, QTreeView
from PyQt5.QtCore import QDir

class DirectoryTree:
    """ Directory tree.
    """
    def __init__(self, path=''):
        """ Init the directory tree.
        """
        # Create directory view.
        self.model = QFileSystemModel()
        self.model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(path))

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(False)

        # Hide all columns, but name.
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
