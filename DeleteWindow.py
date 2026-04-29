from PySide6 import QtWidgets

class DeleteWindow(QtWidgets.QWidget):
    def __init__(self, excel_manager, on_data_deleted=None):
        super().__init__()
        self.excel_manager = excel_manager
        self.on_data_deleted = on_data_deleted
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
            self.excel_manager.delete_data(row)
            self.excel_manager.save_excel()
            
            
            if self.on_data_deleted:
                self.on_data_deleted()
            
            QtWidgets.QMessageBox.information(self, "Sucesso", "Linha excluída com sucesso!")
            self.close()