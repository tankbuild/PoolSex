from poolseq.data.directories import get_directories_info
from poolseq.data.files import get_files_info
from poolseq.data.modules import get_modules_info
from poolseq.data.schedulers import get_schedulers_info
from poolseq.data.parameters import get_parameters_info


class Data():

    '''
    The Data class stores the following information:
    - Variables: name of the commonly used variables
    - Directories: path to the directories within a PoolSex directory
    - Files: path to the files used by the pipeline
    - Modules: all the information about each module
    - Schedulers: all the information about different schedulers
    - Parameters: default parameters values
    '''

    def __init__(self, root_dir):
        self.directories = get_directories_info(root_dir)
        self.files = get_files_info(self.directories)
        self.modules = get_modules_info()
        self.schedulers = get_schedulers_info()
        self.parameters = get_parameters_info()
