import sys
import os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QVBoxLayout
import ExcelManager
import DeleteWindow
import AddWindow
import UpdateWindow
import fpdf
from fpdf.fonts import FontFace

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
        self.table = None
        self.error_label = None
        
        if(self.excel_manager.load_excel(self.file_path)):  
            self.criar_tabela()
            self.atualizar_tabela()
            
            self.deleteWindow.set_table(self.table)
        else:
            self.error_label = QtWidgets.QLabel("Erro ao carregar o arquivo Excel.")
            self.error_label.setAlignment(QtCore.Qt.AlignCenter)
            self.error_label.setStyleSheet("color: red; font-size: 25px;")
            self.layout.addWidget(self.error_label)
            
        btn_Recarregar = QtWidgets.QPushButton()
        btn_Recarregar.setFixedSize(40, 40)
        btn_Recarregar.setIcon(QtGui.QIcon(self.resource_path("./assets/icons/reload.png")))
        btn_Recarregar.setIconSize(QtCore.QSize(20, 20))
        btn_Recarregar.clicked.connect(self.recarregar_tabela)
        btn_Recarregar.setStyleSheet("""
                QPushButton {
                    background-color: #41a4fa;
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 20px;
                    
                }
                QPushButton:hover {
                    background-color: #5eb4ff;
                }
            """)
        
        btn_Adcionar = QtWidgets.QPushButton("Adicionar")
        btn_Adcionar.setMaximumWidth(110)
        btn_Adcionar.clicked.connect(self.adicionar_linha)
        btn_Adcionar.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
        
        btn_Atualizar = QtWidgets.QPushButton("Atualizar")
        btn_Atualizar.setMaximumWidth(110)
        btn_Atualizar.clicked.connect(self.atualizar_linha)
        btn_Atualizar.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
        btn_Excluir = QtWidgets.QPushButton("Excluir")
        btn_Excluir.clicked.connect(self.excluir_linha)
        btn_Excluir.setMaximumWidth(110)
        btn_Excluir.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
        btn_backup = QtWidgets.QPushButton("Fazer Backup")
        btn_backup.setMaximumWidth(110)
        btn_backup.clicked.connect(self.fazer_backup)
        btn_backup.setStyleSheet("""
                QPushButton {
                    background-color: #2d3748;  
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #4a5568;
                }
            """)
        btn_PDF = QtWidgets.QPushButton("Gerar PDF")
        btn_PDF.setMaximumWidth(110)
        btn_PDF.clicked.connect(self.gerar_pdf)
        btn_PDF.setStyleSheet("""
                QPushButton {
                    background-color: #ff4d4d;
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #ff6666;
                }
            """)
        
        btn_arquivo = QtWidgets.QPushButton("Abrir Arquivo")
        btn_arquivo.setMaximumWidth(110)
        btn_arquivo.clicked.connect(self.abrir_arquivo)
        btn_arquivo.setStyleSheet("""
                QPushButton {
                    background-color: #7ad154;  
                    color: white;
                    border: none;
                    padding: 10px 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #82c963;
                }
            """)
        
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addWidget(btn_Recarregar)
        buttons_layout.addWidget(btn_Adcionar)
        buttons_layout.addWidget(btn_Atualizar)
        buttons_layout.addWidget(btn_Excluir)
        buttons_layout.addWidget(btn_backup)
        buttons_layout.addWidget(btn_PDF)
        buttons_layout.addWidget(btn_arquivo)
        
        self.layout.addLayout(buttons_layout, stretch=0)
        self.setLayout(self.layout)
    
#-----Funções relacionadas à tabela-----   
    
    def criar_tabela(self):

        self.table = QtWidgets.QTableWidget()

        self.table.verticalHeader().hide()

        self.table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectItems
        )

        self.table.setSelectionMode(
            QtWidgets.QAbstractItemView.SingleSelection
        )

        self.table.cellClicked.connect(
            self.voltar_para_celula
        )

        self.table.cellDoubleClicked.connect(
            self.selecionar_linha
        )

        header = self.table.horizontalHeader()

        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #2d3748;
                color: white;
                padding: 4px;
                border: none;
            }
        """)

        header.setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )

        self.layout.insertWidget(0, self.table, stretch=1)
            
            
            
    def atualizar_tabela(self):

        if self.excel_manager.df is None:
            return

        self.table.clear()

        self.table.setColumnCount(
            len(self.excel_manager.df.columns)
        )

        self.table.setHorizontalHeaderLabels(
            self.excel_manager.get_columns()
        )

        self.table.setRowCount(
            len(self.excel_manager.df)
        )

        self.preencher_tabela()

        QtCore.QTimer.singleShot(
            0,
            self.ajustar_colunas
        )         
            
    
    def preencher_tabela(self):
        """Preenche a tabela com os dados do Excel Manager"""    
        if self.excel_manager.df is None:
            return
        
        if self.table is None:
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
        if self.table is None:
            return
        self.table.resizeColumnsToContents()

        total_width = sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))

        
        available_width = self.table.width()

        
        available_width -= self.table.verticalHeader().width()

        
        available_width -= 20

        if total_width > 0:
            scale = available_width / total_width

            for i in range(self.table.columnCount()):
                self.table.setColumnWidth(i, int(self.table.columnWidth(i) * scale))

        
        diff = available_width - sum(self.table.columnWidth(i) for i in range(self.table.columnCount()))
        if diff != 0:
            last = self.table.columnCount() - 1
            self.table.setColumnWidth(last, self.table.columnWidth(last) + diff)
    
    
    def recarregar_tabela(self):
        self.excel_manager.load_excel(self.file_path)

        if self.table is None:
            return
        self.table.setRowCount(0)
         
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
        self.selected_row = None
        
        self.preencher_tabela()
        self.ajustar_colunas()
    
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
        self.selected_row = None
    
        
        self.preencher_tabela()
        self.ajustar_colunas()
        
    
    def adicionar_linha(self):
        self.addWindow = AddWindow.AddWindow(self.excel_manager, on_data_added=self.recarregar_tabela)
        self.addWindow.show()
        
    def abrir_arquivo(self,): 
        file_path, _= QtWidgets.QFileDialog.getOpenFileName(self, "Selecione um arquivo Excel", "", "Excel Files (*.xlsx *.xls)")
        
        self.file_path = file_path
        if self.excel_manager.load_excel(self.file_path):

            self.selected_row = None
            if self.table is  None:
                self.criar_tabela()
                self.layout.removeWidget(self.error_label)
                self.error_label.deleteLater()
            self.atualizar_tabela()
            self.deleteWindow.set_table(self.table)
            
                
    def gerar_pdf(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Salvar PDF",
            "",
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        if not file_path.endswith('.pdf'):
            file_path += '.pdf'

        pdf = fpdf.FPDF(
            orientation='L',
            unit='mm',
            format='A4'
        )

        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.add_page()

        logo_path = self.resource_path("./assets/logos/Logo.png")

        if os.path.exists(logo_path):
            pdf.image(logo_path, x=15, y=5, w=40)

        # ===== TÍTULO =====
        pdf.set_font('Helvetica', 'B', 24)
        pdf.cell(
            0,
            15,
            "Relatório de Dados",
            align='C',
            new_x="LMARGIN",
            new_y="NEXT"
        )

        pdf.ln(10)

        col_count = self.table.columnCount()

        # ===== LARGURA DAS COLUNAS =====
        
        
        page_width = pdf.epw

        col_count = self.table.columnCount()

        col_widths = []

        pdf.set_font("Helvetica", size=7)

        for col in range(col_count):

            header = self.table.horizontalHeaderItem(col).text()

            max_width = pdf.get_string_width(header)

            for row in range(self.table.rowCount()):

                item = self.table.item(row, col)

                if item:

                    text = item.text().replace("\n", " ")

                    text_width = pdf.get_string_width(text)

                    if text_width > max_width:
                        max_width = text_width

            # margem interna
            col_widths.append(max_width + 6)

        # soma total
        total_width = sum(col_widths)

        # proporcional à largura da página
        col_widths = [
            (w / total_width) * page_width
            for w in col_widths
]

        # ===== TABELA =====
        with pdf.table(
            borders_layout="ALL",
            cell_fill_mode="ROWS",
            col_widths=col_widths,
            headings_style=FontFace(
                color=(255, 255, 255),
                fill_color=(45, 55, 72),
                emphasis="B"
            ),
            line_height=6,
            text_align="CENTER",
        ) as table:

            # ===== CABEÇALHO =====
            row = table.row()

            for col in range(col_count):
                header_text = self.table.horizontalHeaderItem(col).text()
                pdf.set_font("Helvetica", "B", size=8)
                row.cell(header_text)

            # ===== DADOS =====
            for row_index in range(self.table.rowCount()):

                pdf.set_font("Helvetica", size=7)

                row = table.row()

                for col in range(col_count):

                    item = self.table.item(row_index, col)

                    text = item.text() if item else ""

                    text = text.replace("\n", " ")

                    lower = text.lower()

                    # Cor dinâmica
                    style = {}

                    style = None

                    if lower == "sim":
                        style = FontFace(fill_color=(198, 239, 206),
                                    size_pt=7,
                                    emphasis=None
                                )

                    elif lower in ("não", "nao"):
                        style = FontFace(fill_color=(255, 199, 206),
                                     size_pt=7,
                                    emphasis=None
                                )
                        
                    
                    row.cell(text, style=style)

        pdf.output(file_path)

        QtWidgets.QMessageBox.information(
            self,
            "Sucesso",
            "PDF gerado com sucesso!"
        )
        
    def fazer_backup(self):
        if self.excel_manager.save_backup():
            QtWidgets.QMessageBox.information(
                self,
                "Sucesso",
                "Backup criado com sucesso!"
            )
        else:
            QtWidgets.QMessageBox.critical(
                self,
                "Erro",
                "Falha ao criar backup."
            )
           
        
#-----Funções relacionadas à seleção de linha-----    
    
    def voltar_para_celula(self, row, col, *_):
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.selected_row = None
        self.table.setCurrentCell(row, col)
    
    def selecionar_linha(self, row, col, *_):
        self.selected_row = row
        self.table.clearSelection()
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.selectRow(row)
        
        
#---------Função para pegar os caminhos--------

    def resource_path(self,relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)