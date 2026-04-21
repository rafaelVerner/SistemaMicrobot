from PySide6 import QtWidgets
from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout
import AgendamentoWindow
import LoginWindow
import VoucherWindow

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Sistema MicroBOT")
        self.showMaximized()

        menu = QHBoxLayout()
        menu.setContentsMargins(0,10,0,0)
        menu.setSpacing(5)
        btn_Voucher = QtWidgets.QPushButton("Voucher")
        btn_Voucher.setMaximumWidth(250)
        btn_Voucher.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
        
        btn_Login = QtWidgets.QPushButton("Login")
        btn_Login.setMaximumWidth(250)
        btn_Login.setStyleSheet("""
            QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #4a5568;
            }
        """)
        
        btn_Agendamento = QtWidgets.QPushButton("Agendamento")
        btn_Agendamento.setMaximumWidth(250)
        btn_Agendamento.setStyleSheet("""
            QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #4a5568;
            }
        """)

        self.stack = QStackedWidget()
        self.stack.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.tela1 = LoginWindow.LoginWindow(self.stack)
        self.tela2 = VoucherWindow.VoucherWindow(self.stack)
        self.tela3 = AgendamentoWindow.AgendamentoWindow(self.stack)

        self.stack.addWidget(self.tela1)
        self.stack.addWidget(self.tela2)
        self.stack.addWidget(self.tela3)

        btn_Voucher.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela2))
        btn_Login.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela1))
        btn_Agendamento.clicked.connect(lambda: self.stack.setCurrentWidget(self.tela3))
        
        menu.addWidget(btn_Login)
        menu.addWidget(btn_Voucher)
        menu.addWidget(btn_Agendamento)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.layout.addLayout(menu, stretch=0)
        self.layout.addWidget(self.stack, stretch=1)
        self.setLayout(self.layout)