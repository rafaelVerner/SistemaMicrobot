import Window

class VoucherWindow(Window.Window):
    def __init__(self, stack):
        super().__init__(stack, self.resource_path("./Planilhas/vouchers.xlsx"))
        
        