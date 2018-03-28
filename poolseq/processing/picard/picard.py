from poolseq.processing.picard.sort import Sort
from poolseq.processing.picard.add_read_groups import AddReadGroups
from poolseq.processing.picard.merge import Merge
from poolseq.processing.picard.mark_duplicates import MarkDuplicates


class Picard():

    def __init__(self, data, files_info):
        self.add_read_groups = AddReadGroups(data, files_info)
        self.merge = Merge(data, files_info)
        self.mark_duplicates = MarkDuplicates(data, files_info)
        self.sort = Sort(data, files_info)
