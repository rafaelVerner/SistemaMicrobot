from PySide6 import QtWidgets
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLineEdit, QLabel

class UpdateWindow(QtWidgets.QWidget):
    def __init__(self, excel_manager, on_data_updated=None):
        super().__init__()
        self.excel_manager = excel_manager
        self.on_data_updated = on_data_updated
        self.input_fields = {}
        self.row_index = None
        self.setWindowTitle("Atualizar")
        self.setGeometry(100, 100, 400, 300)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
    
    def carregar_dados(self, row_index):
        """Carrega os dados de uma linha específica para edição"""
        self.row_index = row_index
        self.criar_campos()
    
    def criar_campos(self):
        # Limpar layout anterior
        while self.main_layout.count():
            self.main_layout.takeAt(0).widget().deleteLater()
        
        self.input_fields = {}
        
        if self.excel_manager.df is None:
            label = QLabel("Nenhum arquivo Excel carregado.")
            label.setStyleSheet("color: red; font-size: 12px;")
            self.main_layout.addWidget(label)
            return
        
        if self.row_index is None:
            label = QLabel("Nenhuma linha selecionada.")
            label.setStyleSheet("color: red; font-size: 12px;")
            self.main_layout.addWidget(label)
            return
        
        # Criar campos de entrada para cada coluna com placeholders dos dados originais
        for header in self.excel_manager.get_columns():
            label = QLabel(header)
            label.setStyleSheet("font-size: 12px; font-weight: bold;")
            self.main_layout.addWidget(label)
            
            input_field = QLineEdit()
            input_field.setStyleSheet("font-size: 11px; padding: 5px;")
            
            # Obter o valor original da célula e usar como placeholder
            original_value = str(self.excel_manager.df.iloc[self.row_index][header]).strip()
            input_field.setPlaceholderText(original_value)
            
            self.main_layout.addWidget(input_field)
            self.input_fields[header] = input_field
        
        # Botão de envio
        button_layout = QHBoxLayout()
        btn_atualizar = QtWidgets.QPushButton("Confirmar")
        btn_atualizar.clicked.connect(self.atualizar_dados)
        btn_atualizar.setStyleSheet("""
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
        
        button_layout.addWidget(btn_atualizar)
        button_layout.addWidget(btn_cancelar)
        self.main_layout.addLayout(button_layout)
        
        # Adicionar espaço em branco
        self.main_layout.addStretch()
    
    def atualizar_dados(self):
        data = {}
        for header, input_field in self.input_fields.items():
            text = input_field.text()
            # Se o campo estiver vazio, usa o placeholder (valor original)
            if text.strip() == "":
                data[header] = input_field.placeholderText()
            else:
                data[header] = text
        
        self.excel_manager.update_data(self.row_index, data)
        self.excel_manager.save_excel()
        self.close()
        
        # Mostrar mensagem de sucesso
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Sucesso")
        msg_box.setText("Dados atualizados com sucesso!")
        msg_box.setStyleSheet("QMessageBox { background-color: white; }")
        msg_box.exec()
        
        # Recarregar tabela se callback foi definido
        if self.on_data_updated:
            self.on_data_updated()