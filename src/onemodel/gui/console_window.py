from PyQt5.QtWidgets import QLineEdit, QPlainTextEdit
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtCore import QProcess

class ConsoleWindow:
    """ Console Window for executing the ondemodel REPL.
    """
    def __init__(self, window):
        """ Constructor.
        """
        self.window = window

        self.input = QLineEdit()
        self.output = QPlainTextEdit()


        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.input.setFont(fixedfont)
        self.output.setFont(fixedfont)

        self.input.returnPressed.connect(self.process_input)

        self.process = QProcess()
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyRead.connect(self.on_read)
        # self.process.start('onemodel-cli.py repl')

    def execute_command(self, cmd):
        self.print(f'>> {cmd}')
        self.process.start(cmd)

    def on_read(self):
        result = self.process.readAll().data().decode()
        self.print(result)

    def process_input(self):
        """ Process the command in the input box.
        """
        text = self.input.text()
        self.input.setText('')

        self.print(text)
        text += '\n'
        self.process.write(text.encode())

    def print(self, string):
        """ Print the string into the console.
        """
        self.output.appendPlainText(string)

    def export_model(self):
        """ Export current model.
        """

        cmd = f'python -m onemodel.cli.cli export {self.window.file_path}'

        self.execute_command(cmd)
