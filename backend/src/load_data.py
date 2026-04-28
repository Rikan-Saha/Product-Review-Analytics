import pandas as pd

def load_csv(file) -> pd.DataFrame:
    return pd.read_csv(file)
def load_xlsx(file) -> pd.DataFrame:
    return pd.read_excel(file)
# def load_text():
    