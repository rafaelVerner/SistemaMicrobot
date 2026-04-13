import sys
import MainWindow
from PySide6 import QtWidgets

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janela = MainWindow.MainWindow()
    janela.show()
    sys.exit(app.exec())