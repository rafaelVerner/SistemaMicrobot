from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout

class LoginWindow(QtWidgets.QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        

        layout = QVBoxLayout()
        self.setLayout(layout)