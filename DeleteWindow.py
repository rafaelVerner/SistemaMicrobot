from PySide6 import QtWidgets

class DeleteWindow(QtWidgets.QWidget):
    def __init__(self, excel_manager, table=None):
        super().__init__()
        self.excel_manager = excel_manager
        self.table = table
        self.setWindowTitle("Excluir")
        self.setGeometry(100, 100, 400, 200)
    
    def set_table(self, table):
        """Define a referência da tabela"""
        self.table = table
    
    def excluir_linha_selecionada(self, selected_row):
        """Excluir a linha selecionada da tabela"""
        if self.table is None:
            QtWidgets.QMessageBox.warning(self, "Erro", "Tabela não inicializada.")
            return
        
        row = selected_row
        
        # Pedir confirmação
        reply = QtWidgets.QMessageBox.question(
            self, 
            "Confirmação", 
            "Tem certeza que deseja excluir esta linha?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            # Excluir do Excel Manager
            self.excel_manager.delete_data(row)
            self.excel_manager.save_excel()
            
            # Excluir da tabela visual
            self.table.removeRow(row)
            
            QtWidgets.QMessageBox.information(self, "Sucesso", "Linha excluída com sucesso!")
            self.close()