import os


class Directories():

    def __init__(self):
        self.root = self.get_root_dir()
        self.genomes = os.path.join(self.root, 'genomes')
        self.qsub = os.path.join(self.root, 'qsub')
        self.reads = os.path.join(self.root, 'reads')
        self.results = os.path.join(self.root, 'results')
        self.poolseq = os.path.join(self.root, 'poolseq')
        self.shell = os.path.join(self.root, 'shell')

    def get_root_dir(self):
        temp = os.path.abspath(__file__)
        for i in range(4):
            temp = os.path.split(temp)[0]
        return temp
