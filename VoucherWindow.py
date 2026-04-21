import Window

class VoucherWindow(Window.Window):
    def __init__(self, stack):
        super().__init__(stack, ".\\Planilhas\\vouchers.xlsx")
        
        