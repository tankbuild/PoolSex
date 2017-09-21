from poolseq.processing.crisp.variant_calling import VariantCalling


class Crisp():

    def __init__(self, data):
        self.variant_calling = VariantCalling(data)
