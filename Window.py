from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QVBoxLayout
import ExcelManager
import DeleteWindow
import AddWindow
import UpdateWindow

class Window(QtWidgets.QWidget):
    def __init__(self, stack, file_path=None):
        super().__init__()
        self.stack = stack
        self.excel_manager = ExcelManager.ExcelManager()
        self.deleteWindow = DeleteWindow.DeleteWindow(self.excel_manager, on_data_deleted=self.recarregar_tabela)
        self.updateWindow = UpdateWindow.UpdateWindow(self.excel_manager, on_data_updated=self.recarregar_tabela)
        self.file_path = file_path
        self.selected_row = None
        self.layout = QVBoxLayout()
        
        if(self.excel_manager.load_excel(self.file_path)):  
            self.criar_tabela()
        else:
            error_label = QtWidgets.QLabel("Erro ao carregar o arquivo Excel.")
            error_label.setAlignment(QtCore.Qt.AlignCenter)
            error_label.setStyleSheet("color: red; font-size: 25px;")
            self.layout.addWidget(error_label)

        btn_Adcionar = QtWidgets.QPushButton("Adicionar")
        btn_Adcionar.setMaximumWidth(180)
        btn_Adcionar.clicked.connect(self.adicionar_linha)
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
        btn_Atualizar.clicked.connect(self.atualizar_linha)
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
        btn_Excluir.clicked.connect(self.excluir_linha)
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
        
        self.layout.addLayout(buttons_layout, stretch=0)
        self.setLayout(self.layout)
    
#-----Funções relacionadas à tabela-----   
    
    def criar_tabela(self):
        if self.excel_manager.df is not None:
            self.table = QtWidgets.QTableWidget()
            self.table.verticalHeader().hide()
            self.table.setColumnCount(len(self.excel_manager.df.columns))
            self.table.setHorizontalHeaderLabels(self.excel_manager.get_columns())

            self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
            self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            

            self.table.cellClicked.connect(self.voltar_para_celula)
            self.table.cellDoubleClicked.connect(self.selecionar_linha)
            
            self.table.horizontalHeader().setStyleSheet(""" 
                QHeaderView::section {
                    background-color: #2d3748;  
                    color: white;
                    padding: 4px;
                    border: none;
                }
                """)
            
            self.layout.addWidget(self.table, stretch=1)
            
            # Passar referência da tabela para o DeleteWindow
            self.deleteWindow.set_table(self.table)
            
            # Preencher a tabela com dados
            self.preencher_tabela()
            self.ajustar_colunas()
    
    def preencher_tabela(self):
        """Preenche a tabela com os dados do Excel Manager"""
        if self.excel_manager.df is None:
            return
        
        self.table.setRowCount(len(self.excel_manager.df))
        
        for i in range(len(self.excel_manager.df)):
            for j in range(len(self.excel_manager.df.columns)):
                cell_text = str(self.excel_manager.df.iloc[i, j]).strip()
                item = QtWidgets.QTableWidgetItem(cell_text)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
                item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)

                normalized = cell_text.lower()
                
                if normalized == 'sim':
                    item.setBackground(QtGui.QBrush(QtGui.QColor('#c6efce')))
                elif normalized in ('não', 'nao'): 
                    item.setBackground(QtGui.QBrush(QtGui.QColor('#ffc7ce')))

                self.table.setItem(i, j, item)
            
            
    def ajustar_colunas(self):
        self.table.resizeColumnsToContents()

        total_width = sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))

        
        available_width = self.table.width()

        
        available_width -= self.table.verticalHeader().width()

       
        if self.table.verticalScrollBar().isVisible():
            available_width -= self.table.verticalScrollBar().width()

        
        available_width -= 20

        if total_width > 0:
            scale = available_width / total_width

            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, int(self.table.columnWidth(i) * scale))

        # 🔥 correção final de pixel (ESSENCIAL)
        diff = available_width - sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))
        if diff != 0:
            last = self.table.columnCount() - 1
            self.table.setColumnWidth(last, self.table.columnWidth(last) + diff)
    
    
    def recarregar_tabela(self):
        self.excel_manager.load_excel(self.file_path)

        self.table.setRowCount(0)  # limpa tudo
        self.table.setRowCount(len(self.excel_manager.df))

        self.preencher_tabela()
        self.ajustar_colunas()
        
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'table'):
            self.ajustar_colunas()
            
            
#-----Funções relacionadas aos botões-----

    def excluir_linha(self):
        if self.selected_row is None:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Aviso")
            msg_box.setText("Por favor, selecione uma linha para excluir!")
            msg_box.setStyleSheet("QMessageBox { background-color: white; }")
            msg_box.exec()
            return
        self.deleteWindow.excluir_linha_selecionada(self.selected_row)
    
    def atualizar_linha(self):
        if self.selected_row is None:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle("Aviso")
            msg_box.setText("Por favor, selecione uma linha para atualizar!")
            msg_box.setStyleSheet("QMessageBox { background-color: white; }")
            msg_box.exec()
            return
        
        self.updateWindow.carregar_dados(self.selected_row)
        self.updateWindow.show()
    
        
        # Preencher a tabela existente com novos dados
        self.preencher_tabela()
        self.ajustar_colunas()
        
        
    def adicionar_linha(self):
        self.addWindow = AddWindow.AddWindow(self.excel_manager, on_data_added=self.recarregar_tabela)
        self.addWindow.show()
    
#-----Funções relacionadas à seleção de linha-----    
    
    def voltar_para_celula(self):
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
    
    def selecionar_linha(self, row):
        self.selected_row = row
        self.table.clearSelection()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.selectRow(row)
            