import os
from poolseq.data import file_names
from poolseq.data import directory_names as dir_names


class Files():

    def __init__(self, root_dir):
        self.qsub = os.path.join(root_dir, dir_names.qsub, file_names.qsub)
        self.settings = os.path.join(root_dir, file_names.settings)
