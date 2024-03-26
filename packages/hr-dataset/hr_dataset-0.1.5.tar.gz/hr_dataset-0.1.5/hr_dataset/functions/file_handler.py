from dataclasses import dataclass
from pathlib import Path


@dataclass
class InputFile:
    folder: str
    file: str

    def __post_init__(self):
        self.full = Path(self.folder, self.file)
        self.file_name_only = Path(self.full).name
        self.file_name_wo_ext = Path(self.full).stem
        self.file_type: str = Path(self.full).suffix
        self.full_path: str = Path(self.full).resolve().parent

    @property
    def valid(self) -> bool:
        return True if self.full.exists() else False


if __name__ == '__main__':

    test = InputFile(
        folder=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        file=r'Setup_file_example.xlsx'
    )
    
    test2 = InputFile(
        folder=r'C:\Users\ctf\pq_data\resultatoversigt_data',
        file=r'hr_dataset_anon.csv'
    )
    
    if not test.valid and not test2.valid:
        print('false')

    print(test.valid, test2.valid)
