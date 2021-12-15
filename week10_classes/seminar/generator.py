import random

from PyQt6 import QtWidgets

from generator_widgets import Ui_MainWindow


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.generate()
        self.pushButton.clicked.connect(self.generate)

    def generate(self):
        min_value = self.minValue.text()
        max_value = self.maxValue.text()
        if (
                min_value.isdigit() and
                max_value.isdigit() and
                int(min_value) <= int(max_value)
        ):
            text = str(random.randint(int(min_value), int(max_value)))
        else:
            text = 'Error'
        self.label.setText(text)


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()
