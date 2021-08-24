#!/usr/bin/env python3
import sys

# importing required libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set window geometry.
        self.setGeometry(0, 0, 1200, 800)

        # Move the window to the center of the screen.
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle = self.frameGeometry()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Create the layout. 
        grid_layout = QGridLayout()
        self.setLayout(grid_layout)
        grid_layout.setColumnStretch(1, 2)

        # Create directory view.
        self.model = QFileSystemModel()
        self.model.setRootPath('')

        self.tree = QTreeView()
        self.tree.setModel(self.model)

        self.tree.setAnimated(False)
        self.tree.setIndentation(20)
        self.tree.setSortingEnabled(True)

        # Hide all columns, but name.
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)

        grid_layout.addWidget(self.tree, 0, 0, 3, 1)

        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()
        grid_layout.addWidget(self.editor, 0, 1, 1, 1)

        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()
        grid_layout.addWidget(self.editor, 1, 1, 2, 1)

        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()
        grid_layout.addWidget(self.editor, 0, 2, 3, 1)

        self.setWindowTitle('OneModel Editor')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windowExample = MainWindow()
    windowExample.show()
    app.exec_()
