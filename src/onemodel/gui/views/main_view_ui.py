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

        # Add file_menu.
        self.file_menu = MainWindow.menuBar().addMenu('&File')

        # Add file_toolbar.
        self.file_toolbar = QtWidgets.QToolBar('File')
        MainWindow.addToolBar(self.file_toolbar)

        # Create open file action.
        self.open_file_action = QtWidgets.QAction("Open file", MainWindow)
        self.open_file_action.setStatusTip("Open file in the text editor.")
        self.file_menu.addAction(self.open_file_action)
        self.file_toolbar.addAction(self.open_file_action)

        # Create export action.
        self.export_action = QtWidgets.QAction('Export', MainWindow)
        self.export_action.setStatusTip("Export current model into Matlab code.")
        self.file_toolbar.addAction(self.export_action)

        # Create save action.
        self.save_action = QtWidgets.QAction('Save', MainWindow)
        self.save_action.setStatusTip("Save current file.")
        self.file_menu.addAction(self.save_action)
        self.file_toolbar.addAction(self.save_action)

        self.set_title()

    def set_title(self):
        version = self.mainWindow._model.version
        self.mainWindow.setWindowTitle(f'OneModel Editor v{version}')

    def update_editor_label(self):
        """ Update the window title.
        """
        file_path = self.mainWindow._model.file_path
        is_file_modified = self.mainWindow._model.is_file_modified

        if file_path == None:
            basename = 'Untitled'
        else:
            basename = path.basename(file_path)
            basename = file_path

        title = f'Edit - {basename}'

        if is_file_modified == True:
            title += '*'
        
        self.label_textEditor.setText(title)
