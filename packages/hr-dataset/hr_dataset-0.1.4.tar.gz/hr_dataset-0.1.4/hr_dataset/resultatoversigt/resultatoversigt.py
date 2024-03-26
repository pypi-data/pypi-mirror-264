from dataclasses import dataclass
from pathlib import Path
from typing import Union

import numpy as np
import pandas as pd
from ..functions.file_handler import InputFile
from ..config.config_parser import ConfigParameters


@dataclass
class Resultatoversigt:
    """Docstring"""
    input_dir: str
    output_dir: str
    config_file: str
    data: Union[str, pd.DataFrame]

    def __post_init__(self):
        self.__validate_inputs(isinstance(self.data, pd.DataFrame))
        self.config = ConfigParameters(Path(self.input_dir, self.config_file))
        self.__aggregering()
        
    def __aggregering(self):
        self.data_filtered = self.__filter_data()
        self.data_hierarchy = self.__agg_hierarchy()
        if self.config.replies_calc:
            self.data_hierarchy = self.__calculate_replies()
        self.data_hierarchy = self.__aggregating_vars()
        if self.config.include_themes:
            self.__calculate_themes()
        self.__sort_columns()
        if self.config.remove_minreplies:
            self.data_hierarchy = self.data_hierarchy[self.data_hierarchy["Svar"]>=self.config.min_replies]
        self.data_hierarchy = self.data_hierarchy.sort_values(by=self.config.ptypeTs, na_position="first")
        self.data_hierarchy = self.data_hierarchy.rename(self.config.rename_vars, axis="columns")

    def __sort_columns(self) -> None:
        columnsSortList = []    
        columnsSortList += ["ptypeId"] + ["Niveau"] + ["Name"] + self.config.ptypeTs
        if self.config.replies_calc:
            columnsSortList += ["Antal"] + ["Svar"] + ["Svarprocent"]
        if self.config.include_themes:
            for theme, var in self.config.themes.items():
                columnsSortList += [theme]
                columnsSortList += var
        else:
            columnsSortList += self.config.agg_vars

        self.data_hierarchy = self.data_hierarchy.reindex(columns=columnsSortList)
        
    def __calculate_themes(self) -> None:
        for theme, var in self.config.themes.items():
            self.data_hierarchy[theme] = self.data_hierarchy[var].mean(axis=1)
        
    def __calculate_replies(self) -> pd.DataFrame:
        var = self.config.complete_var
        repliesDF = pd.DataFrame()
        for ptype in self.config.ptypes:
            tempDF = pd.DataFrame()
            tempDF["ptypeId"] = self.data_filtered.groupby([ptype]).aggregate(ptype).mean()
            tempDF["Antal"] = self.data_filtered.groupby([ptype]).aggregate(var).count()
            tempDF["Svar"] = self.data_filtered.groupby([ptype]).aggregate(var).sum()
            tempDF["Svarprocent"]= tempDF["Svar"]/tempDF["Antal"]
            repliesDF = pd.concat([repliesDF, tempDF.rename(columns={ptype:"ptypeId"})],sort=True)
        
        return pd.merge(self.data_hierarchy, repliesDF, how="left", left_on="ptypeId", right_on="ptypeId")

    def __filter_data(self) -> pd.DataFrame:
        temp = self.data
        if isinstance(self.config.measurement, int):
            temp = temp.query(f"measurem=={self.config.measurement}")
        if self.config.filter_dict:
            for var, value in self.config.filter_dict.items():
                temp = temp[temp[var]==value]
        for var in self.config.agg_vars:
            for value in self.config.missing_values:
                temp.loc[temp[var] == value, var] = np.nan
        return temp
    
    def __agg_hierarchy(self) -> pd.DataFrame:
        ptypeTsNew = []
        ptypeData = pd.DataFrame()
        for ptype, ptypeT, level in zip(self.config.ptypes, self.config.ptypeTs, self.config.levels):
            ptypeTsNew = ptypeTsNew + [ptypeT]
            ptypeDataTemp = self.data_filtered.groupby([ptype],as_index=False)[ptypeTsNew].first()
            ptypeDataTemp["Name"] = ptypeDataTemp[ptypeT]
            ptypeDataTemp["Niveau"] = level
            ptypeData = pd.concat([ptypeData, ptypeDataTemp.rename(columns={ptype:"ptypeId"})], sort=True)
    
        return ptypeData
    
    def __aggregating_vars(self) -> pd.DataFrame:
        aggDataTemp = pd.DataFrame()
        aggDataFinal = pd.DataFrame()
        for ptype in self.config.ptypes:
            aggDataTemp = self.data_filtered.groupby([ptype],as_index=False).aggregate(self.config.var_aggregations).reset_index()
            aggDataFinal = pd.concat([aggDataFinal, aggDataTemp.rename(columns={ptype:"ptypeId"})])
        
        return pd.merge(self.data_hierarchy, aggDataFinal, how="left", left_on="ptypeId", right_on="ptypeId")

    def __validate_inputs(self, pandas_df: bool) -> None:
        cf_file = InputFile(self.input_dir, self.config_file)
        if not cf_file.valid:
            raise ValueError('Invalid inputfiles - check directory and filenames')
        if cf_file.file_type != '.xlsx':
            raise ValueError('Config file has to be a .xlsx file')

        if not pandas_df:
            data_file = InputFile(self.input_dir, self.data)
            if not data_file.valid:
                raise ValueError('Invalid inputfiles - check directory and filenames')
            try:
                self.data = pd.read_csv(data_file.full, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
            except UnicodeDecodeError:
                self.data = pd.read_csv(data_file.full, encoding='ansi', sep=';', decimal=',', low_memory=False)
                
if __name__ == "__main__":
    pass