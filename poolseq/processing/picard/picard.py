from poolseq.processing.picard.sort import Sort
from poolseq.processing.picard.add_read_groups import AddReadGroups
from poolseq.processing.picard.merge import Merge


class Picard():

    def __init__(self, data):
        self.sort = Sort(data)
        self.add_read_groups = AddReadGroups(data)
        self.merge = Merge(data)
