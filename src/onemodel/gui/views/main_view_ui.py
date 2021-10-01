from os import path

from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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
        hbox = QHBoxLayout()

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

        # Vertical splitter.
        split_v = QSplitter(Qt.Vertical)
        split_v.setStretchFactor(0,2);
        split_v.setStretchFactor(1,1);

        # Create frame for editor.
        frame = QFrame()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.label_textEditor)
        vbox.addWidget(self.textEditor)
        frame.setLayout(vbox)
        # Add it to vertical splitter.
        split_v.addWidget(frame)

        # Create frame console log.
        frame = QFrame()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.label_console)
        vbox.addWidget(self.console.output)
        frame.setLayout(vbox)
        # Add it to vertical splitter.
        split_v.addWidget(frame)

        # Horizontal splitter.
        split_h = QSplitter(Qt.Horizontal)

        # Create frame for directory tree.
        frame = QFrame()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.label_directoryTree)
        vbox.addWidget(self.directoryTree.tree)
        frame.setLayout(vbox)
        # Add it to horizontal splitter.
        split_h.addWidget(frame)

        # Add the vertival splitter to the horizontal one.
        split_h.addWidget(split_v)

        # Create main frame with the pathField and the horizontal splitter.
        frame = QFrame()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.pathField)
        vbox.addWidget(split_h)
        frame.setLayout(vbox)

        # Add it to the layout.
        hbox.addWidget(frame)

        # Set initial sizes of splitters.
        split_v.setStretchFactor(0,2);
        split_v.setStretchFactor(1,1);
        split_h.setStretchFactor(0,1);
        split_h.setStretchFactor(1,4);

        # creating a QWidget layout
        container = QtWidgets.QWidget()

        # setting layout to the container
        container.setLayout(hbox)

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

        # Create run action.
        self.run_action = QtWidgets.QAction('Run', MainWindow)
        self.run_action.setStatusTip("Run current model.")
        self.file_toolbar.addAction(self.run_action)

        # Create export action.
        self.export_action = QtWidgets.QAction('Export', MainWindow)
        self.export_action.setStatusTip("Export current model into Matlab code.")
        self.file_toolbar.addAction(self.export_action)

        # Create save action.
        self.save_action = QtWidgets.QAction('Save', MainWindow)
        self.save_action.setShortcut('Ctrl+S')
        self.save_action.setStatusTip("Save current file.")
        self.file_menu.addAction(self.save_action)

        # Create examples action.
        self.examples_action = QtWidgets.QAction('Examples', MainWindow)
        self.examples_action.setStatusTip("Change current path to examples folder.")
        self.file_menu.addAction(self.examples_action)

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
