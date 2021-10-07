from os import path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

import onemodel
from onemodel.gui.views.main_view_ui import Ui_MainWindow

class MainView(QMainWindow):
    def __init__(self, model, main_controller):
        super().__init__()

        self._model = model
        self._main_controller = main_controller
        self._ui = Ui_MainWindow()
        self._ui.setup_ui(self)

        ####################################################################
        #   connect widgets to controllers
        ####################################################################

        # Return pressed in pathField.
        self._ui.pathField.returnPressed.connect(
                self.on_return_pressed_pathField
                )

        # Editing finished in pathField.
        self._ui.pathField.editingFinished.connect(
                self.on_editing_finished_pathField
                )

        # Double click on item in directoryTree.
        self._ui.directoryTree.tree.doubleClicked.connect(
                self.on_double_click_directoryTree
                )
        
        # Text changed in text editor.
        self._ui.textEditor.textChanged.connect(
                self.on_text_changed_textEditor
                )

        # Triggered open_file_action.
        self._ui.open_file_action.triggered.connect(
                self.on_triggered_open_file_action
                )

        # Triggered run action.
        self._ui.run_action.triggered.connect(
                self.on_triggered_run_action
                )

        # Triggered export_action.
        self._ui.export_action.triggered.connect(
                self.on_triggered_export_action
                )

        # Triggered save_action.
        self._ui.save_action.triggered.connect(
                self.on_triggered_save_action
                )

        # Triggered examples_action.
        self._ui.examples_action.triggered.connect(
                self.on_triggered_examples_action
                )

        ####################################################################
        #   listen for model event signals
        ####################################################################

        # Current path is updated.
        self._model.current_path_changed.connect(self.on_current_path_changed)

        # File path is updated.
        self._model.file_path_changed.connect(self.on_file_path_changed)

        # Is file modified updated.
        self._model.is_file_modified_changed.connect(
                self.on_is_file_modified_changed
        )

        # onemodel-cli ready to read.
        self._model.onemodel_cli_read.connect(self.on_cli_ready_read)

    def on_return_pressed_pathField(self):
        new_path = self._ui.pathField.text()

        error = self._main_controller.change_current_path(new_path)

        if error:
            # If not, show error message.
            title = 'Error Changing Folder'
            msg = f'Cannot find folder "{new_path}".\n'
            msg += 'Check the spelling and try again.'

            QtWidgets.QMessageBox.about(self, title, msg) 
            

    def on_editing_finished_pathField(self):
        self._ui.pathField.setText(self._model.current_path)

    def on_double_click_directoryTree(self, index):
        item_path = self._ui.directoryTree.model.filePath(index)

        if path.isfile(item_path):

            # Check if there is a not saved file open.
            if self._model.is_file_modified == True:
                # If not, show error message.
                # TODO: Finish this error message.
                title = 'Changes Not Saved'
                msg = 'Save changes to current document before closing?\n'
                msg += f'If you don\'t save, changes will be permanently lost.'

                QtWidgets.QMessageBox.about(self, title, msg) 


            self._main_controller.open_file(item_path)

        elif path.isdir(item_path):
            # Change current path.
            self._main_controller.change_current_path(item_path)

    def on_current_path_changed(self, path):
        self._ui.pathField.setText(path)
        self._ui.directoryTree.tree.setRootIndex(
                self._ui.directoryTree.model.index(path)
                )

    def on_file_path_changed(self, file_path):
        self._ui.update_editor_label()
        self._ui.textEditor.open_file(file_path)

    def on_is_file_modified_changed(self, value):
        self._ui.update_editor_label()
    
    def on_text_changed_textEditor(self):
        self._main_controller.change_is_file_modified(True)

    def on_triggered_open_file_action(self):
        # getting path and bool value
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self,
                "Open file",
                "",
                "Text documents (*.txt);All files (*.*)"
                )

        if file_path != '':
            self._main_controller.open_file(file_path)

    def on_triggered_run_action(self):
        file_path = self._model._file_path

        if file_path != None:
            cmd = 'onemodel-cli'
            cmd += f' run {self._model._file_path}'

            self._ui.console.printCommand(cmd)
            self._main_controller.execute_cmd(cmd)

    def on_triggered_export_action(self):
        file_path = self._model._file_path

        if file_path != None:
            cmd = 'onemodel-cli'
            cmd += f' export {self._model._file_path}'

            self._ui.console.printCommand(cmd)
            self._main_controller.execute_cmd(cmd)

        else:
            # If not, show error message.
            title = 'Error Exporting Model'
            msg = f'Not model open in Editor.\n'
            msg += 'Please open a model before exporting.'

            QtWidgets.QMessageBox.about(self, title, msg) 

    def on_triggered_save_action(self):
        if self._model.file_path == None:
            # We are creating a new file.
            # TODO:
            print('Call save as')

        else:
            text = self._ui.textEditor.toPlainText()

            self._main_controller.save_file_to_path(
                text,
                self._model.file_path
            )

            self._ui.status.showMessage('Done saving.')

    def on_triggered_examples_action(self):

        example_path = path.abspath(onemodel.__file__)
        example_path = path.dirname(example_path)
        example_path = path.join(example_path,'examples')

        self._main_controller.change_current_path(example_path)
        self._ui.status.showMessage('Examples folder open.')

    def on_cli_ready_read(self, text):
        self._ui.console.print(text)
