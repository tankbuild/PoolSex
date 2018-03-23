from poolseq.processing.popoolation.mpileup2sync import Mpileup2sync


class Popoolation():

    def __init__(self, data):
        self.mpileup2sync = Mpileup2sync(data)
