from pathlib import Path
import pandas as pd

def load_dataset(file_path: Path, file_type: str) -> pd.DataFrame:
    if file_type == '.csv':
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, encoding='ansi', sep=';', decimal=',', low_memory=False)
    elif file_type == '.xlsx':
        df = pd.read_excel(file_path)
    return df
