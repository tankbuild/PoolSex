from poolseq.structure import Structure
from poolseq.processing import Processing
from poolseq.parameters import Parameters


class Pipeline():

    def __init__(self):
        self.structure = Structure()
        self.parameters = Parameters(self.structure)
        self.processing = Processing(self.structure, self.parameters)

    def run(self):
        self.processing.bwa.index()
        self.processing.bwa.mapping()
        self.processing.picard.sort()
        self.processing.picard.add_read_groups()
        self.processing.picard.merge()
