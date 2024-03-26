from hr_dataset.functions.file_handler import InputFile


def validate_inputs():
    if InputFile(self.input_dir, self.config_file).valid:
        print('hep')
    else:
        print('false')
