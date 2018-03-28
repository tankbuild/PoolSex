from poolseq.processing.bwa.index import Index
from poolseq.processing.bwa.mapping import Mapping


class Bwa():

    def __init__(self, data, files_info):
        self.index = Index(data, files_info)
        self.mapping = Mapping(data, files_info)
