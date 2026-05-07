import Window

class ReposicaoWindow(Window.Window):
    def __init__(self, stack):
        super().__init__(stack, self.resource_path("./Planilhas/reposicao.xlsx"))