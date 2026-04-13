import pandas as pd

class ExcelManager:
    def __init__(self):
        self.df = None
        self.file_path = None

    def load_excel(self, file_path):
        try:
            self.df = pd.read_excel(file_path)
            self.file_path = file_path
            return True
        except Exception as e:
            return False
    
    def add_data(self, data):
        new_df = pd.DataFrame([data])
        if self.df is not None:
            if set(self.df.columns.tolist()) != set(new_df.columns.tolist()):
                print("Data columns do not match the Excel file columns.")
                return 
            else:
                self.df = pd.concat([self.df, new_df], ignore_index=True)
                print("Data added successfully.")
        else:
            print("No Excel file loaded. Please load an Excel file first.")

    def save_excel(self):
        if self.df is not None:
            try:
                self.df.to_excel(self.file_path, index=False)
                print("Excel file saved successfully.")
            except Exception as e:
                print(f"Error saving Excel file: {e}")
        else:
            print("No Excel file loaded. Please load an Excel file first.")
    
    def delete_data(self, index):
        if self.df is not None:
            try:
                self.df = self.df.drop(index)
                print("Data deleted successfully.")
            except Exception as e:
                print(f"Error deleting data: {e}")
        else:
            print("No Excel file loaded. Please load an Excel file first.")

    def update_data(self, index, data):
        if self.df is not None:
            try:
                for key, value in data.items():
                    self.df.at[index, key] = value
                print("Data updated successfully.")
            except Exception as e:
                print(f"Error updating data: {e}")
        else:
            print("No Excel file loaded. Please load an Excel file first.")

