from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QLabel

class AddWindow(QtWidgets.QWidget):
    def __init__(self, excel_manager, on_data_added=None):
        super().__init__()
        self.excel_manager = excel_manager
        self.input_fields = {}
        self.on_data_added = on_data_added
        self.setWindowTitle("Adicionar")
        self.setGeometry(100, 100, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.criar_campos()
    
    def criar_campos(self):
        # Limpar layout anterior
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.input_fields = {}
        
        if self.excel_manager.df is None:
            label = QLabel("Nenhum arquivo Excel carregado.")
            label.setStyleSheet("color: red; font-size: 12px;")
            self.main_layout.addWidget(label)
            return
        
        # Criar campos de entrada para cada coluna
        for header in self.excel_manager.get_columns():
            label = QLabel(header)
            label.setStyleSheet("font-size: 12px; font-weight: bold;")
            self.main_layout.addWidget(label)
            
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 11px; padding: 5px;")
            self.main_layout.addWidget(input_field)
            
            self.input_fields[header] = input_field
        
        # Botão de envio
        button_layout = QHBoxLayout()
        btn_adicionar = QtWidgets.QPushButton("Confirmar")
        btn_adicionar.clicked.connect(self.adicionar_dados)
        btn_adicionar.setStyleSheet("""
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
        
        btn_cancelar = QtWidgets.QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.close)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #718096;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #4a5568;
            }
        """)
        
        button_layout.addWidget(btn_adicionar)
        button_layout.addWidget(btn_cancelar)
        self.main_layout.addLayout(button_layout)
        
        # Adicionar espaço em branco
        self.main_layout.addStretch()
    
    def adicionar_dados(self):
        data = {}
        for header, input_field in self.input_fields.items():
            data[header] = input_field.text()
        
        self.excel_manager.add_data(data)
        self.excel_manager.save_excel()
        
        # Mostrar mensagem de sucesso
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText("Dados adicionados com sucesso!")
        msg_box.setStyleSheet("QMessageBox { background-color: white; }")
        msg_box.exec()
        
        # Recarregar tabela se callback foi definido
        if self.on_data_added:
            self.on_data_added()
        

        self.close()
        
        QtWidgets.QMessageBox.information(
            self,
            "Sucesso",
            "Dados adicionados com sucesso!"
        )