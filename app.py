import sys
import MainWindow
from PySide6 import QtWidgets, QtGui
import ctypes


if __name__ == "__main__":
    myappid = 'meuprograma.sistema.1.0'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
        myappid
    )
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("assets\\icons\\icon_exe.ico"))
    janela = MainWindow.MainWindow()
    janela.show()
    janela.showMaximized()
    sys.exit(app.exec())