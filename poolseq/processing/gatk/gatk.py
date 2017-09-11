from poolseq.processing.gatk.index import Index
from poolseq.processing.gatk.haplotype_caller import HaplotypeCaller


class Gatk():

    def __init__(self, data):
        self.index = Index(data)
        self.haplotype_caller = HaplotypeCaller(data)
