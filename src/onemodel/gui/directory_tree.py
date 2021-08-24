from os import path

from PyQt5.QtWidgets import QFileSystemModel, QTreeView
from PyQt5.QtCore import QDir

class DirectoryTree:
    """ Directory tree.
    """
    def __init__(self, window):
        """ Init the directory tree.
        """
        self.window = window

        # Create directory view.
        self.model = QFileSystemModel()
        self.model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(QDir.homePath()))

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(False)

        # Hide all columns, but name.
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        self.tree.doubleClicked.connect(self.item_selected)

    def item_selected(self, index):
        item_path = self.model.filePath(index)

        if path.isfile(item_path):
            # Open the file in the text editor
            self.window.open_file(item_path)

        elif path.isdir(item_path):
            # Change the current path.
            self.window.set_path(item_path)
