import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout
import LoginWindow
import VoucherWindow

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Sistema MicroBOT")

        menu = QHBoxLayout()
        btn_Voucher = QtWidgets.QPushButton("Voucher")
        btn_Login = QtWidgets.QPushButton("Login")
        btn_Voucher.setStyleSheet("""
                background-color: #2d3748;
                color: white;
                border: none;
                padding: 10px 20px;
            """)
        btn_Login.setStyleSheet("""
            background-color: #2d3748;
            color: white;
            border: none;
            padding: 10px 20px;
        """)

        self.stack = QStackedWidget()
        self.tela1 = LoginWindow.LoginWindow(self.stack)
        self.tela2 = VoucherWindow.VoucherWindow(self.stack)

        self.stack.addWidget(self.tela1)
        self.stack.addWidget(self.tela2)

        btn_Voucher.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela2))
        btn_Login.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela1))
        
        menu.addWidget(btn_Login)
        menu.addWidget(btn_Voucher)

        layout = QVBoxLayout()
        layout.addLayout(menu)
        layout.addWidget(self.stack)
        self.setLayout(layout)