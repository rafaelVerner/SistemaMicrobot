import pandas as pd

class ExcelManager:
    def __init__(self):
        self.df = None
        self.file_path = None

    def load_excel(self, file_path):
        try:
            self.df = pd.read_excel(file_path, engine='openpyxl')
            self.df = self.df.fillna(" ")
            self.file_path = file_path
            return True
        except Exception as e:
            return False
    
    def add_data(self, data):
        new_df = pd.DataFrame([data])
        if self.df is not None:
            if set(self.df.columns.tolist()) != set(new_df.columns.tolist()):
                return False
            else:
                self.df = pd.concat([self.df, new_df], ignore_index=True)
                return True
        else:
            return False

    def save_excel(self):
        if self.df is not None:
            try:
                self.df.fillna("").to_excel(self.file_path, index=False)
                return True
            except Exception as e:
                return False
        else:
            
            return False

    def delete_data(self, index):
        if self.df is not None:
            try:
                self.df = self.df.drop(index)
                return True
            except Exception as e:
                return False
        else:
            return False

    def update_data(self, index, data):
        if self.df is not None:
            try:
                for key, value in data.items():
                    self.df.at[index, key] = value
                return True
            except Exception as e:
                return False
        else:
            return False


    def get_columns(self):
        return self.df.columns.tolist()
