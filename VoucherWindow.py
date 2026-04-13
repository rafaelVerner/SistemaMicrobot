from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout
import ExcelManager

class VoucherWindow(QtWidgets.QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.excel_manager = ExcelManager.ExcelManager()
        
        self.layout = QVBoxLayout()
        
        if(self.excel_manager.load_excel(".\\Planilhas\\vouchers.xlsx")):  
            QtWidgets.QMessageBox.information(self, "Success", "Excel file loaded successfully.")
            self.populate_table()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Error loading Excel file.")
        
        btn_Adcionar = QtWidgets.QPushButton("Adicionar Aluno")
        
        self.layout.addWidget(btn_Adcionar)
        self.setLayout(self.layout)
    
    def populate_table(self):
        if self.excel_manager.df is not None:
            self.table = QtWidgets.QTableWidget()
            self.table.setRowCount(len(self.excel_manager.df))
            self.table.setColumnCount(len(self.excel_manager.df.columns))
            self.table.setHorizontalHeaderLabels(self.excel_manager.df.columns.tolist())
            
            for i in range(len(self.excel_manager.df)):
                for j in range(len(self.excel_manager.df.columns)):
                    item = QtWidgets.QTableWidgetItem(str(self.excel_manager.df.iloc[i, j]))
                    self.table.setItem(i, j, item)
            
            # Expandir a tabela para preencher o espaço disponível
            self.table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            
            
            self.layout.addWidget(self.table)