from poolseq.processing.bwa import Bwa
from poolseq.processing.picard import Picard
from poolseq.processing.gatk import Gatk


class Processing():

    def __init__(self, structure, parameters):
        self.bwa = Bwa(structure, parameters)
        self.picard = Picard(structure, parameters)
        self.gatk = Gatk(structure, parameters)
