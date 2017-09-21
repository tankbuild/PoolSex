from poolseq.processing.samtools.index import Index
from poolseq.processing.samtools.mpileup import Mpileup


class Samtools():

    def __init__(self, data):
        self.index = Index(data)
        self.mpileup = Mpileup(data)
