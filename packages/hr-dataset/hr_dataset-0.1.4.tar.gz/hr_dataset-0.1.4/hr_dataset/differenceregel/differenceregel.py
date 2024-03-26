import numpy as np
import pandas as pd

def calculate_diffrule(
    df: pd.DataFrame, 
    ptypes: list[str],
    id_var: str,
    replies_var: str = 'stato_4',
    diff_limit: int = 3, 
    report_limit: int = 5
    ) -> pd.DataFrame:
    """
    Funktion som beregner differenceregel for et HR datasæt fra Results.
    Returnerer en ny dataframe som holder id_var samt de nye difference variable
    
    df: pd.DataFrame som holder datasættet med respondentdata
    ptypes: Liste med navnene på ptype variable. Rækkefølgen her er vigtig, da den skal følge hierarkiet og sidste udfald skal være enhedens ptype
    id_var: Variabel som bruges til at koble diff variablene tilbage på et datasæt. Dette kan være responde, medarbejderens ptype eller lignende
    replies_var: Kan udelades hvorved stato_4 anvendes. Anvendes et alternativ så skal denne variabel være kodet 0/1, hvor 1=gnf
    diff_limit: Minimum antal svar som ikke bryder differencereglen. Default er 3.
    report_limit: Minimum svar før en rapport dannes. Default er 5.
    """    
    
    def return_ptype(value_map: dict[str, list[int]], value_to_check: int | float) -> str:
        # Funktion som finder ptypen for en given værdi
        # Bygger på en dict med ptyper og deres unikke værdier
        for ptype, ptype_value in value_map.items():
            if value_to_check in ptype_value:
                return ptype

    # Starter med at fjerne alle overflødige variable
    rel_vars = [id_var, replies_var] + ptypes
    df_red = df[rel_vars].copy()
    
    # Den reducerede dataframe stackes (converterer kolonner til rækker) 
    # I forbindelse med stacking, så skubbes null værdier til højre
    s = df_red.stack()
    s.index = [s.index.get_level_values(0), s.groupby(level=0).cumcount()]
    # Unstacker så vi er tilbage i udgangspunktet, men nu er der ingen "huller" i ptypestien
    df1 = s.unstack().reindex(columns=range(len(df_red.columns)))
    # Omdøber kolonner i den nye df, så de matcher den gamle
    df1.columns = df_red.columns
    # Danner en backup af ptype-variable med værdierne
    for col in ptypes:
        df1.loc[:, f'{col}_old'] = df1[col]
        
    ### Næste skridt beregner potentielle diff-brud 

    # Først dannes lister med de relevante variable som der skal aggregeres pba og variable til at holde 0/1 markering
    opd_vars = list(reversed(ptypes[:-1]))
    opd_vars2 = list(reversed(ptypes[1:]))
    diff_temp_vars = list(reversed([f'temp_diff_{niv.replace('ptype', '')}' for niv in ptypes[:-1]]))

    # For hvert sæt at aggregeringsvariable beregnes potentielle diff-brud
    for opd_var, opd_var2, diff_var in zip(opd_vars, opd_vars2, diff_temp_vars):
            df1['svar'] = df1.groupby([opd_var, opd_var2])[replies_var].transform('sum')
            df1['stato_4_2'] = np.where(df1['svar']>=report_limit, 0, df1[replies_var])
            df1['svar_sum'] = df1.groupby([opd_var])[replies_var].transform('sum')
            df1['svar_sum_2'] = df1.groupby([opd_var])['stato_4_2'].transform('sum')
            df1['svar_sum'] = np.where(df1['svar']>=diff_limit, pd.NA, df1['svar_sum'])
            df1[diff_var] = np.where(
                (df1.svar<diff_limit) & (df1.svar>0) & (df1.svar_sum.notnull()) & ((df1.svar_sum-df1.svar)>=diff_limit) & (df1.svar_sum_2<diff_limit),
                1,
                0
            )
            df1[opd_var] = np.where(
                df1[diff_var]==1, 'Uoplyst', df1[opd_var]
            )

    # Danner dataframe som udelukkende holder de cases, som er berørt af diff_reglen.
    diff_cases = df1[df1[diff_temp_vars].sum(axis=1) > 0].copy()

    # Danner nye diff_variable, som matcher niveauet som skal blankes
    diff_vars = [f'diff_{col}' for col in ptypes[:-1]]

    for diff_var in diff_vars:
        diff_cases.loc[:, diff_var] = 0
        
    # Variable til at loop igennem
    diff_temp_vars = [f'temp_diff_{niv.replace('ptype', '')}' for niv in ptypes[:-1]]
    ptypes_old_values = [f'{col}_old' for col in ptypes[:-1]]
    
    # Danner dict med map over ptypes og deres unikke værdier
    ptype_values = {}

    for col in ptypes:
        unique_values = df[col].unique()
        ptype_values[col] = unique_values.tolist() 
        
    # For hver række tjekkes om de midlertidige diff variable har værdien 1, hvis ja, så markeres diff variable som matcher hierarki strukturen
    for row in diff_cases.itertuples():
        for temp_diff_var, ptype_value in zip(diff_temp_vars, ptypes_old_values):
            if getattr(row, temp_diff_var)==1:
                old_ptype = return_ptype(ptype_values, getattr(row, ptype_value))
                idx_ptype = ptypes.index(old_ptype)
                diff_cases.at[row.Index, diff_vars[idx_ptype]] = 1

    rel_vars = [id_var] + diff_vars
    return diff_cases[rel_vars]    

def beregn_differenceregel(
    df: pd.DataFrame, 
    ptypes: list[str],
    id_var: str,
    gnf_var: str = 'stato_4',
    graense: int = 3, 
    rapport_graense: int = 5
    ) -> pd.DataFrame:
    """
    Funktion som beregner differenceregel for et HR datasæt fra Results.
    Returnerer en ny dataframe som holder id_var samt de nye difference variable
    
    df: pd.DataFrame som holder datasættet med respondentdata
    ptypes: Liste med navnene på ptype variable. Rækkefølgen her er vigtig, da den skal følge hierarkiet og sidste udfald skal være enhedens ptype
    id_var: Variabel som bruges til at koble diff variablene tilbage på et datasæt. Dette kan være responde, medarbejderens ptype eller lignende
    gnf_var: Kan udelades hvorved stato_4 anvendes. Anvendes et alternativ så skal denne variabel være kodet 0/1, hvor 1=gnf
    graense: Minimum antal svar som ikke bryder differencereglen. Default er 3.
    rapport_graense: Minimum svar før en rapport dannes. Default er 5.
    """
    
    # Starter med at fjerne alle overflødige variable
    rel_vars = [id_var, gnf_var] + ptypes
    df_red = df[rel_vars].copy()

    # Gemmer enhedens ptype
    enhed = ptypes[-1]
    
    # Danner opdelingsvariable, som følger rapporteringsstrukturen. Altså samler variable for niveauer og enheder
    for idx, niv in enumerate(ptypes[1:], start=1):
        df_red[f'opd_{niv}'] = np.where(
            df_red[ptypes[idx-1]].notnull(),
            np.where(
                df_red[niv].isnull(), df_red[enhed], df_red[niv]
            ),
            'Uoplyst'
        )

    df_red[f'opd_{ptypes[0]}'] = df_red[f'{ptypes[0]}']

    # Danner liste med variable som anvendes til at aggregere pba
    opd_vars = list(reversed([f'opd_{niv}' for niv in ptypes[:-1]]))
    opd_vars2 = list(reversed([f'opd_{niv}' for niv in ptypes[1:]]))
    diff_vars = list(reversed([f'diff_{niv.replace('ptype', '')}' for niv in ptypes[:-1]]))

    # For hvert niveau beregnes om der er udfordringer med diff
    for opd_var, opd_var2, diff_var in zip(opd_vars, opd_vars2, diff_vars):
        df_red['svar'] = df_red.groupby([opd_var, opd_var2])[gnf_var].transform('sum')
        df_red['stato_4_2'] = np.where(df_red['svar']>=rapport_graense, 0, df_red[gnf_var])
        df_red['svar_sum'] = df_red.groupby([opd_var])[gnf_var].transform('sum')
        df_red['svar_sum_2'] = df_red.groupby([opd_var])['stato_4_2'].transform('sum')
        df_red['svar_sum'] = np.where(df_red['svar']>=graense, pd.NA, df_red['svar_sum'])
        df_red[diff_var] = np.where(
            (df_red.svar<graense) & (df_red.svar>0) & (df_red.svar_sum.notnull()) & ((df_red.svar_sum-df_red.svar)>=graense) & (df_red.svar_sum_2<graense),
            1,
            0
        )
        
        df_red[opd_var] = np.where(
            df_red[diff_var]==1, 'Uoplyst', df_red[opd_var]
        )

    rel_vars = [id_var] + diff_vars
    return df_red[rel_vars]


if __name__ == '__main__':
    dataset = pd.read_csv(r'C:\Users\ctf\pq_data\resultatoversigt_data\RegH_2021.csv', encoding='ansi', sep=';', decimal=',', low_memory=False)
    dataset = dataset.query(r'measurem==2')
    ptypes = [
        'ptype1',
        'ptype2',
        'ptype3',
        'ptype4',
        'ptype5',
        'ptype6',
        'ptype7',
        'ptype10',
        'ptype8',
        # 'ptype11'
    ]

    # diff_df = beregn_differenceregel(dataset, ptypes, 'ptype9', graense=5)
    diff_df = calculate_diffrule(dataset, ptypes, 'ptype9', diff_limit=5)
    dataset = dataset.merge(diff_df, how='left', left_on='ptype9', right_on='ptype9', suffixes=('', '_new'))
    dataset.to_csv(r'C:\Users\ctf\pq_data\resultatoversigt_data\gfdfdklreg_h_tester.csv', encoding='utf-8-sig', sep=';', decimal=',')
