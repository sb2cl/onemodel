from PyQt5 import QtCore, QtGui, QtWidgets

from onemodel.gui.widgets.directory_tree import DirectoryTree
from onemodel.gui.widgets.text_editor import TextEditor
from onemodel.gui.widgets.console import Console

class Ui_MainWindow(object):
    def setup_ui(self, MainWindow):

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

        # Place widgets in the grid.
        gridLayout.addWidget(self.pathField, 0, 0, 1, 2)
        gridLayout.addWidget(self.directoryTree.tree, 1, 0, 4, 1)
        gridLayout.addWidget(self.textEditor.editor, 1, 1, 1, 1)
        gridLayout.addWidget(self.console.output, 2, 1, 2, 1)
        gridLayout.addWidget(self.console.input, 4, 1, 1, 1)

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

