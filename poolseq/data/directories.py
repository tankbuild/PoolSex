import os
from poolseq.data import directory_names as dir_names


class Directories():

    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)
        self.genomes = os.path.join(self.root, dir_names.genomes)
        self.qsub = os.path.join(self.root, dir_names.qsub)
        self.reads = os.path.join(self.root, dir_names.reads)
        self.output = os.path.join(self.root, dir_names.output)
        self.poolseq = os.path.join(self.root, dir_names.poolseq)
        self.shell = os.path.join(self.root, dir_names.shell)
