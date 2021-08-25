from PyQt5.QtWidgets import QToolBar, QAction

class Menu:
    """ This class defines the menu and the tool bar.
    """
    def __init__(self, window):
        """ Initialize menu.
        """
        self.window = window
                
        self.file_menu = window.menuBar().addMenu("&File")

        self.file_toolbar = QToolBar("File")
        window.addToolBar(self.file_toolbar)
    
        # creating a open file action
        open_file_action = QAction("Open file", window)
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(
                lambda: window.open_file(None)
                )
        self.file_menu.addAction(open_file_action)
        self.file_toolbar.addAction(open_file_action)

        # Create export action
        export_action = QAction("Export", window)
        export_action.setStatusTip("Export current model into matlab.")
        export_action.triggered.connect(window.console.export_model)
        self.file_toolbar.addAction(export_action)
