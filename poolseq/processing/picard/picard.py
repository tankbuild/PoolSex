from poolseq.processing.picard.sort import Sort
from poolseq.processing.picard.add_read_groups import AddReadGroups
from poolseq.processing.picard.merge import Merge
from poolseq.processing.picard.validate_sam_file import ValidateSamFile


class Picard():

    def __init__(self, data):
        self.sort = Sort(data)
        self.add_read_groups = AddReadGroups(data)
        self.merge = Merge(data)
        self.validate_sam_file = ValidateSamFile(data)
