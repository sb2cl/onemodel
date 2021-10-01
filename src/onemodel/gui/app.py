import sys
from PyQt5.QtWidgets import QApplication

from onemodel.gui.model.model import Model
from onemodel.gui.controllers.controller import Controller
from onemodel.gui.views.main_view import MainView

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = Model()
        self.main_controller = Controller(self.model)
        self.main_view = MainView(self.model, self.main_controller)
        self.main_view.show()

def main():
    app = App(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
