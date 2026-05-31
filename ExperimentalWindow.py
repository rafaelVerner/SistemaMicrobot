import Window

class ExperimentalWindow(Window.Window):
    def __init__(self, stack):
        super().__init__(stack,".\\Planilhas\\experimental.xlsx")