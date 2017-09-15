from poolseq.processing.crisp.index import Index
from poolseq.processing.crisp.variant_calling import VariantCalling


class Crisp():

    def __init__(self, data):
        self.index = Index(data)
        self.variant_calling = VariantCalling(data)
