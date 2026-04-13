from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QVBoxLayout
import ExcelManager

class VoucherWindow(QtWidgets.QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.excel_manager = ExcelManager.ExcelManager()
        
        layout = QVBoxLayout()
        
        if(self.excel_manager.load_excel(".Planilhas\\vouchers.xlsx")):  
            
            layout.addWidget(QtWidgets.QLabel("Voucher Window"))    
       
       
        self.setLayout(layout)