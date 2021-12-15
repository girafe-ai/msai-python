# https://www.qt.io
# https://build-system.fman.io/qt-designer-download
# https://www.riverbankcomputing.com/software/pyqt/download

# pip install PyQt6
# pyuic6 client.ui -o clientui.py


from PyQt6 import QtWidgets
import clientui


class ExampleApp(QtWidgets.QMainWindow, clientui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # to run on button click:
        # self.some_button.pressed.connect(self.some_method)


app = QtWidgets.QApplication([])
window = ExampleApp()
window.show()
app.exec()
