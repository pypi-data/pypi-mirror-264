from dataclasses import dataclass
from pathlib import Path
import pandas as pd

@dataclass
class ConfigParameters:
    """Docstring"""

    config_file: Path

    def __post_init__(self):
        self.__validate_config()
        
    @property
    def ptypes(self) -> list[str]:
        return [ptype for ptype in self.__hierarchy["Id"]]

    @property
    def ptypeTs(self) -> list[str]:
        return [ptypeT for ptypeT in self.__hierarchy["Name"]]

    @property
    def levels(self) -> list[str]:
        return [level for level in self.__hierarchy["Label"]]

    @property
    def replies_calc(self) -> bool:
        return bool(self.__config_parameters.get("includeMinRepliesCalculations"))

    @property
    def include_themes(self) -> bool:
        return bool(self.__config_parameters.get("includeThemeCalculations"))
    
    @property
    def remove_minreplies(self) -> bool:
        return bool(self.__config_parameters.get("includeMinRepliesCalculations"))

    @property
    def agg_vars(self) -> list[str]:
        return [var for var in self.__aggresults_vars["Name"]]
    
    @property
    def rename_vars(self) -> dict:
        renames = dict(zip(self.__aggresults_vars["Name"], self.__aggresults_vars["Label"]))
        renames.update(dict(zip(self.__aggresults_vars["Name"], self.__aggresults_vars["Label"])))
        renames.update(dict(zip(self.__aggresults_vars["Theme"], self.__aggresults_vars["ThemeLabel"])))
        return renames
    
    @property
    def missing_values(self) -> list[int]:
        return [int(value) for value in self.__config_parameters.get("sysmisValues").split(";")]

    @property
    def var_aggregations(self) -> dict:
        return dict(zip(self.__aggresults_vars["Name"],self.__aggresults_vars["AggType"]))

    @property
    def themes(self) -> dict:
        themes = {}
        for t, v in zip(self.__aggresults_vars["Theme"], self.__aggresults_vars["Name"]):
            if t in themes:
                themes[t].append(v)
            else:
                themes[t] = [v]
        return themes

    @property
    def id_var(self) -> str:
        return self.__config_parameters.get('id_var')

    @property
    def complete_var(self) -> str:
        return self.__config_parameters.get('repliesVar')
    
    @property
    def min_replies(self) -> int:
        return self.__config_parameters.get('minReplies')

    @property
    def min_diff(self) -> int:
        return self.__config_parameters.get('minDiffrule')
    
    @property
    def measurement(self) -> int:
        curMeasure = self.__config_parameters.get('currentMeasurement')
        return curMeasure if isinstance(curMeasure, int) else None

    @property
    def filter_dict(self) -> dict[str, int]:
        return dict(zip(self.__filters['FilterVar'],self.__filters['FilterValue']))

    @property
    def __config_parameters(self) -> dict[str, str]:
        return dict(zip(self.__basicconfig['Parameter'],self.__basicconfig['Value']))
    
        
    def __validate_config(self) -> None:
        """Only a basic check for now. Could should probably be expanded to ensure that the parameters are correct etc."""
        try:
            pd.read_excel(self.config_file, sheet_name=None)
        except FileNotFoundError:
            raise FileNotFoundError(r'Filen med config findes ikke')

        try:
            self.__basicconfig = pd.read_excel(self.config_file, sheet_name='Konfiguration')
            self.__hierarchy = pd.read_excel(self.config_file, sheet_name='Hierarki')
            self.__filters = pd.read_excel(self.config_file, sheet_name='Filters')
            self.__diffrule = pd.read_excel(self.config_file, sheet_name='Differenceregel')
            self.__aggresults_vars = pd.read_excel(self.config_file, sheet_name='Resultsoversigt_variable')
        except ValueError:
            raise ValueError('Config filen skal som minimum indeholde: Hierarki, Differenceregel, Resultatoversigt & Resultatoversigt_variable')
            

if __name__ == '__main__':
    
    test_path = Path(r'C:\Users\ctf\pq_data\resultatoversigt_data\Setup_file_example.xlsx')
    
    test = ConfigParameters(test_path)
    print(test.id_var)
    print(test.ptypes)
    print(test.min_replies)
    print(test.min_diff)
    print(type(test.replies_calc), test.replies_calc)
    print(test.var_aggregations)
    print(test.missing_values)
    print(test.themes)
    print(test.rename_vars)