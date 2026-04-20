from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout
import ExcelManager

class AgendamentoWindow(QtWidgets.QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.excel_manager = ExcelManager.ExcelManager()
        
        self.layout = QVBoxLayout()
        
        if(self.excel_manager.load_excel(".\\Planilhas\\agendamentos.xlsx")):  
            self.criar_tabela()
        else:
            error_label = QtWidgets.QLabel("Error! Não foi possível carregar o arquivo Excel.")
            error_label.setAlignment(QtCore.Qt.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 18px;")
            self.layout.addWidget(error_label)
        
        btn_Adcionar = QtWidgets.QPushButton("Adicionar")
        btn_Adcionar.setMaximumWidth(180)
        btn_Adcionar.setStyleSheet("""
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
        
        btn_Atualizar = QtWidgets.QPushButton("Atualizar")
        btn_Atualizar.setMaximumWidth(180)
        btn_Atualizar.setStyleSheet("""
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
        btn_Excluir = QtWidgets.QPushButton("Excluir")
        btn_Excluir.setMaximumWidth(180)
        btn_Excluir.setStyleSheet("""
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
        btn_PDF = QtWidgets.QPushButton("Gerar PDF")
        btn_PDF.setMaximumWidth(180)
        btn_PDF.setStyleSheet("""
                QPushButton {
                    background-color: #ff4d4d;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
        
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(btn_Adcionar)
        buttons_layout.addWidget(btn_Atualizar)
        buttons_layout.addWidget(btn_Excluir)
        buttons_layout.addWidget(btn_PDF)
        
        self.layout.addLayout(buttons_layout)
        self.setLayout(self.layout)
    
    def criar_tabela(self):
        if self.excel_manager.df is not None:
            self.table = QtWidgets.QTableWidget()
            self.table.setRowCount(len(self.excel_manager.df))
            self.table.setColumnCount(len(self.excel_manager.df.columns))
            self.table.setHorizontalHeaderLabels(self.excel_manager.df.columns.tolist())
            self.table.horizontalHeader().setStyleSheet(""" 
                QHeaderView::section {
                    background-color: #2d3748;  
                    color: white;
                    padding: 4px;
                    border: none;
                }
                """)
            
            
            for i in range(len(self.excel_manager.df)):
                for j in range(len(self.excel_manager.df.columns)):
                    item = QtWidgets.QTableWidgetItem(str(self.excel_manager.df.iloc[i, j]))
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                    item.setTextAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
                    self.table.setItem(i, j, item)
            
            
            self.layout.addWidget(self.table, stretch=1)
            self.ajustar_colunas()
            
    def ajustar_tabela(self):
        self.table.resizeColumnsToContents()
        
        total_width = sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))
        available_width = self.table.width()
        
        available_width -= self.table.verticalHeader().width()
        
        available_width -= 20
        
        if self.table.verticalScrollBar().isVisible():
            available_width -= self.table.verticalScrollBar().width()
        
        if total_width > 0:
            scale = available_width / total_width
            
            for i in range(self.table.columnCount()):
                new_width = int(self.table.columnWidth(i) * scale)
                self.table.setColumnWidth(i, new_width)
        
        diff = available_width - sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))
        
        if diff != 0:
            last = self.table.columnCount() - 1
            self.table.setColumnWidth(last, self.table.columnWidth(last) + diff)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'table'):
            self.ajustar_colunas()