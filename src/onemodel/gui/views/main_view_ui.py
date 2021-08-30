from os import path

from PyQt5 import QtCore, QtGui, QtWidgets

from onemodel.gui.widgets.directory_tree import DirectoryTree
from onemodel.gui.widgets.text_editor import TextEditor
from onemodel.gui.widgets.console import Console

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):
        self.mainWindow = MainWindow

        MainWindow.setObjectName("MainWindow")

        # Set window geometry.
        MainWindow.setGeometry(0, 0, 1200, 800)

        # Move window to the center of screen.
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle = MainWindow.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())

        # Create the layout. 
        gridLayout = QtWidgets.QGridLayout()
        gridLayout.setColumnStretch(1, 2)

        # Init widgets.
        self.pathField = QtWidgets.QLineEdit()
        self.pathField.setText(MainWindow._model.current_path)
        self.directoryTree = DirectoryTree(MainWindow._model.current_path)
        self.textEditor = TextEditor()
        self.console = Console()

        # Init labels.
        self.label_directoryTree = QtWidgets.QLabel(MainWindow)
        self.label_directoryTree.setText('Current Folder')
        self.label_textEditor = QtWidgets.QLabel(MainWindow)
        self.update_editor_label()
        self.label_console = QtWidgets.QLabel(MainWindow)
        self.label_console.setText('Console Log')

        # Place widgets in the grid.
        gridLayout.addWidget(self.pathField, 0, 0, 1, 2)
        gridLayout.addWidget(self.label_directoryTree, 1, 0, 1, 1)
        gridLayout.addWidget(self.directoryTree.tree, 2, 0, 5, 1)
        gridLayout.addWidget(self.label_textEditor, 1, 1, 1, 1)
        gridLayout.addWidget(self.textEditor.editor, 2, 1, 1, 1)
        gridLayout.addWidget(self.label_console, 3, 1, 1, 1)
        gridLayout.addWidget(self.console.output, 4, 1, 2, 1)
        gridLayout.addWidget(self.console.input, 6, 1, 1, 1)

        # creating a QWidget layout
        container = QtWidgets.QWidget()

        # setting layout to the container
        container.setLayout(gridLayout)

        # making container as central widget
        MainWindow.setCentralWidget(container)

        # creating a status bar object
        self.status = QtWidgets.QStatusBar()

        # setting stats bar to the window
        MainWindow.setStatusBar(self.status)

        # Set window title.
        # TODO: Place version of onemodel here.
        self.mainWindow.setWindowTitle(f'OneModel Editor')

    def update_editor_label(self):
        """ Update the window title.
        """
        file_path = self.mainWindow._model.file_path

        if file_path == None:
            basename = 'Untitled'
        else:
            basename = path.basename(file_path)
            basename = file_path

        self.label_textEditor.setText(f'Editor - {basename}')
