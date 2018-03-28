from poolseq.processing.samtools.mpileup import Mpileup


class Samtools():

    def __init__(self, data, files_info):
        self.mpileup = Mpileup(data, files_info)
