from pathlib import Path
import numpy as np
import pandas as pd

def is_multiple_choice(df: pd.DataFrame, col: str) -> bool:
    """Multiple choice variable i SX er lidt specielle da alle respondenter har 0 på variablen også selvom de ikke har besvaret variablen.
    Dette kan udnyttes."""
    df_red = df.query(r'stato_1==1 or stato_2==1')
    return (df_red[col]==0).all()  # Hvis alle værdier == 0, så true ellers false

def var_type(df: pd.DataFrame, col: str) -> str:
    if df[col].dtype == 'object':
        return 'open_text'
    if df[col].dtype in ['float64', 'int64']:
        if is_multiple_choice(df, col):
            return 'multiple_choice'
        return 'single_choice'
    return 'oops - unknown var type'


def handle_some_answers(df: pd.DataFrame, rel_cols: list[str]) -> pd.DataFrame:
    """Funktion som renser svar på spørgsmålene for nogen svar respondenter.
    Kræver at dataframen indeholder responde og at alle respondenter er inkluderet - også ny + distribueret, da dette anvendes til at afgøre spørgsmålstyper.
    df: pd.Dataframe som holder det komplette datasæt
    rel_cols: list[str] med de variable som skal renses for deres svar."""
    for col in rel_cols:
        col_var_type = var_type(df, col)
        if col_var_type == 'open_text':
            df[col] = np.where(
                df.stato_3==1, "", df[col]
            )
        elif col_var_type == 'single_choice':
            df[col] = np.where(
                df.stato_3==1, pd.NA, df[col]
            )        
        elif col_var_type == 'multiple_choice':
            df[col] = np.where(
                df.stato_3==1, 0, df[col]
            )        
        elif col_var_type == 'oops - unknown var type':
            print(f'Listen med kolonner som skal renses for nogen svar indeholder en ukendt variabeltype: {col}: {df[col].dtype}. Funktionen skal justeres.')
    
    return df

if __name__ == '__main__':
    dataset = pd.read_csv(r'C:\Users\ctf\pq_data\si_ess_data\Eksempel_dataset_fra_SX_anon.csv', encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
    questionnaire_vars = dataset.loc[:, 'samt':'p_32a'].columns.to_list()
    some_answers = handle_some_answers(dataset, questionnaire_vars).query(r"stato_3==1")
    scope3_file_path = Path(r'C:\Users\ctf\pq_data\si_ess_data\Eksempel_scope3_fil_overskriv_nogen_svar.csv')
    scope3_fil = some_answers[["responde"] + questionnaire_vars].to_csv(scope3_file_path, sep=';', decimal=',', encoding='utf-8-sig', index=False)
    