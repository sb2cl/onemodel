from os import path

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import pyqtSlot

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

        # Triggered open_file_action.
        self._ui.open_file_action.triggered.connect(
                self.on_triggered_open_file_action
                )

        # Triggered export_action.
        self._ui.export_action.triggered.connect(
                self.on_triggered_export_action
                )

        ####################################################################
        #   listen for model event signals
        ####################################################################

        # Current path is updated.
        self._model.current_path_changed.connect(self.on_current_path_changed)

        # File path is updated.
        self._model.file_path_changed.connect(self.on_file_path_changed)

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

    def on_triggered_export_action(self):
        file_path = self._model._file_path

        if file_path != None:
            cmd = 'python -m onemodel.cli.cli'
            cmd += f' export {self._model._file_path}'

            self._ui.console.print(f'>> {cmd}')
            self._main_controller.execute_cmd(cmd)

        else:
            # If not, show error message.
            title = 'Error Exporting Model'
            msg = f'Not model open in Editor.\n'
            msg += 'Please open a model before exporting.'

            QtWidgets.QMessageBox.about(self, title, msg) 

    def on_cli_ready_read(self, text):
        self._ui.console.print(text)
