#!/usr/bin/env python3
import sys

import os
from os import path

# importing required libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *

from onemodel.gui.text_editor import TextEditor
from onemodel.gui.directory_tree import DirectoryTree
from onemodel.gui.path_field import PathField
from onemodel.gui.console_window import ConsoleWindow
from onemodel.gui.menu import Menu

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Current working directory path.
        self.current_path = None

        # Current open file in the text editor.
        # If none, we haven't got a file open yet (or creating new).
        self.file_path = None

        # Set window geometry.
        self.setGeometry(0, 0, 1200, 800)

        # Move the window to the center of the screen.
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Create the layout. 
        grid_layout = QGridLayout()
        grid_layout.setColumnStretch(1, 2)

        # Init the directory tree.
        self.dirTree = DirectoryTree(self)
        grid_layout.addWidget(self.dirTree.tree, 1, 0, 4, 1)

        # Init the text editor.
        self.textEditor = TextEditor()
        grid_layout.addWidget(self.textEditor.editor, 1, 1, 1, 1)

        # Init the path field.
        self.pathField = PathField(self)
        grid_layout.addWidget(self.pathField, 0, 0, 1, 2)

        # Init the console window.
        self.console = ConsoleWindow(self)
        grid_layout.addWidget(self.console.output, 2, 1, 2, 1)
        grid_layout.addWidget(self.console.input, 4, 1, 1, 1)

        # creating a QWidget layout
        container = QWidget()

        # setting layout to the container
        container.setLayout(grid_layout)

        # making container as central widget
        self.setCentralWidget(container)

        # creating a status bar object
        self.status = QStatusBar()

        # setting stats bar to the window
        self.setStatusBar(self.status)

        self.menu = Menu(self)

        # Init the current_path to the home directory.
        self.set_path(QDir.homePath())
        self.set_path('/home/nobel/Sync/python/workspace/onemodel')
        
        # Init the title of the window.
        self.update_title()

    def set_path(self, new_path):
        """ Set a new current path.
        """
        # Check that the new path is valid.
        if path.isdir(new_path):
            # Update current path.
            self.current_path = new_path
            
            # Update path field.
            self.pathField.setText(self.current_path)

            # Update directory tree.
            self.dirTree.tree.setRootIndex(self.dirTree.model.index(self.current_path))

        else:
            # If not, show error message.
            title = 'Error Changing Folder'
            msg = f'Cannot find folder "{new_path}".\n'
            msg += 'Check the spelling and try again.'

            QMessageBox.about(self, title, msg) 

    def restore_path(self):
        """ Restore the path to the last valid path.
        """
        self.set_path(self.current_path)

    def open_file(self, file_path=None):
        """ Open a file in the text editor.
        
        TODO: Long description.
        
        Args:
            file_path: str
                Path to the file
                
        Returns:
            None
        """

        if file_path == None:
            # getting path and bool value
            file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    "Open file",
                    "",
                    "Text documents (*.txt);All files (*.*)"
                    )

        try:
            with open(file_path, 'rU') as f:
                # Read the file
                text = f.read()
                self.file_path = file_path
                self.textEditor.editor.setPlainText(text)

        except Exception as e:
            # show error using critical method
            self.dialog_critical(str(e))

        self.update_title()
       
    def dialog_critical(self, msg):
        """ Shows a critical error dialog message.
        
        Args:
            msg: str
                Message to show.
                
        Returns:
            None
        """
        # creating a QMessageBox object
        dlg = QMessageBox(self)
        # setting text to the dlg
        dlg.setText(msg)
        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)
        # showing it
        dlg.show()

    def update_title(self):
        """ Update the window title.
        """
        if self.file_path == None:
            basename = 'Untitled'
        else:
            basename = path.basename(self.file_path)

        self.setWindowTitle(f'{basename} - OneModel Editor')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
