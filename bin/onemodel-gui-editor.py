#!/usr/bin/env python3

# importing required libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys

# Creating main window class
class MainWindow(QMainWindow):

    # constructor
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # setting window geometry
        self.setGeometry(100, 100, 600, 400)

        # creating a layout
        layout = QVBoxLayout()

        # creating a QPlainTextEdit object
        self.editor = QPlainTextEdit()

        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        # adding editor to the layout
        layout.addWidget(self.editor)

        # creating a QWidget layout
        container = QWidget()

        # setting layout to the container
        container.setLayout(layout)

        # making container as central widget
        self.setCentralWidget(container)

        # creating a status bar object
        self.status = QStatusBar()

        # setting stats bar to the window
        self.setStatusBar(self.status)

        # creating a file tool bar
        file_toolbar = QToolBar("File")

        # adding file tool bar to the window
        self.addToolBar(file_toolbar)

        # creating a file menu
        file_menu = self.menuBar().addMenu("&File")

        # creating actions to add in the file menu
        # creating a open file action
        open_file_action = QAction("Open file", self)

        # setting status tip
        open_file_action.setStatusTip("Open file")

        # adding action to the open file
        open_file_action.triggered.connect(self.file_open)

        # adding this to file menu
        file_menu.addAction(open_file_action)

        # adding this to tool bar
        file_toolbar.addAction(open_file_action)

        # similarly creating a save action
        save_file_action = QAction("Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        # similarly creating save action
        saveas_file_action = QAction("Save As", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        # for print action
        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        # creating another tool bar for editing text
        edit_toolbar = QToolBar("Edit")

        # adding this tool bar to the main window
        self.addToolBar(edit_toolbar)

        # creating a edit menu bar
        edit_menu = self.menuBar().addMenu("&Edit")

        # adding actions to the tool bar and menu bar

        # undo action
        undo_action = QAction("Undo", self)
        # adding status tip
        undo_action.setStatusTip("Undo last change")

        # when triggered undo the editor
        undo_action.triggered.connect(self.editor.undo)

        # adding this to tool and menu bar
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        # redo action
        redo_action = QAction("Redo", self)
        redo_action.setStatusTip("Redo last change")

        # when triggered redo the editor
        redo_action.triggered.connect(self.editor.redo)

        # adding this to menu and tool bar
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        # cut action
        cut_action = QAction("Cut", self)
        cut_action.setStatusTip("Cut selected text")

        # when triggered cut the editor text
        cut_action.triggered.connect(self.editor.cut)

        # adding this to menu and tool bar
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        # copy action
        copy_action = QAction("Copy", self)
        copy_action.setStatusTip("Copy selected text")

        # when triggered copy the editor text
        copy_action.triggered.connect(self.editor.copy)

        # adding this to menu and tool bar
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        # paste action
        paste_action = QAction("Paste", self)
        paste_action.setStatusTip("Paste from clipboard")

        # when triggered paste the copied text
        paste_action.triggered.connect(self.editor.paste)

        # adding this to menu and tool bar
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        # select all action
        select_action = QAction("Select all", self)
        select_action.setStatusTip("Select all text")

        # when this triggered select the whole text
        select_action.triggered.connect(self.editor.selectAll)

        # adding this to menu and tool bar
        edit_toolbar.addAction(select_action)
        edit_menu.addAction(select_action)


        # wrap action
        wrap_action = QAction("Wrap text to window", self)
        wrap_action.setStatusTip("Check to wrap text to window")

        # making it checkable
        wrap_action.setCheckable(True)

        # making it checked
        wrap_action.setChecked(True)

        # adding action
        wrap_action.triggered.connect(self.edit_toggle_wrap)

        # adding it to edit menu not to the tool bar
        edit_menu.addAction(wrap_action)

        # calling update title methpd
        self.update_title()

        # showing all the components
        self.show()

    # creating dialog critical method
    # to show errors
    def dialog_critical(self, s):

        # creating a QMessageBox object
        dlg = QMessageBox(self)

        # setting text to the dlg
        dlg.setText(s)

        # setting icon to it
        dlg.setIcon(QMessageBox.Critical)

        # showing it
        dlg.show()

    # action called by file open action
    def file_open(self):

        # getting path and bool value
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                            "Text documents (*.txt);All files (*.*)")

        # if path is true
        if path:
            # try opening path
            try:
                with open(path, 'rU') as f:
                    # read the file
                    text = f.read()

            # if some error occured
            except Exception as e:

                # show error using critical method
                self.dialog_critical(str(e))
            # else
            else:
                # update path value
                self.path = path

                # update the text
                self.editor.setPlainText(text)

                # update the title
                self.update_title()

    # action called by file save action
    def file_save(self):

        # if there is no save path
        if self.path is None:

            # call save as method
            return self.file_saveas()

        # else call save to path method
        self._save_to_path(self.path)

    # action called by save as action
    def file_saveas(self):

        # opening path
        path, _ = QFileDialog.getSaveFileName(self, "Save file", "",
                            "Text documents (*.txt);All files (*.*)")

        # if dialog is cancelled i.e no path is selected
        if not path:
            # return this method
            # i.e no action performed
            return

        # else call save to path method
        self._save_to_path(path)

    # save to path method
    def _save_to_path(self, path):

        # get the text
        text = self.editor.toPlainText()

        # try catch block
        try:

            # opening file to write
            with open(path, 'w') as f:

                # write text in the file
                f.write(text)

        # if error occurs
        except Exception as e:

            # show error using critical
            self.dialog_critical(str(e))

        # else do this
        else:
            # change path
            self.path = path
            # update the title
            self.update_title()

    # action called by print
    def file_print(self):

        # creating a QPrintDialog
        dlg = QPrintDialog()

        # if executed
        if dlg.exec_():

            # print the text
            self.editor.print_(dlg.printer())

    # update title method
    def update_title(self):

        # setting window title with prefix as file name
        # suffix aas PyQt5 Notepad
        self.setWindowTitle("%s - OneModel Editor" %(os.path.basename(self.path)
                                                if self.path else "Untitled"))

    # action called by edit toggle
    def edit_toggle_wrap(self):

        # chaning line wrap mode
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0 )


# drivers code
if __name__ == '__main__':

    # creating PyQt5 application
    app = QApplication(sys.argv)

    # setting application name
    app.setApplicationName("onemodel")

    # creating a main window object
    window = MainWindow()

    # loop
    app.exec_()
