from poolseq.processing.bwa.index import Index
from poolseq.processing.bwa.mapping import Mapping


class Bwa():

    def __init__(self, data):
        self.index = Index(data)
        self.mapping = Mapping(data)
