import os


class Directories():

    def __init__(self, root_dir):
        self.root = os.path.abspath(root_dir)
        self.genomes = os.path.join(self.root, 'genomes')
        self.qsub = os.path.join(self.root, 'qsub')
        self.reads = os.path.join(self.root, 'reads')
        self.output = os.path.join(self.root, 'results')
        self.poolseq = os.path.join(self.root, 'poolseq')
        self.shell = os.path.join(self.root, 'shell')
