import Window

class AgendamentoWindow(Window.Window):
    def __init__(self, stack):
        super().__init__(stack, ".\\Planilhas\\agendamentos.xlsx")