from poolseq.processing.picard.sort import Sort
from poolseq.processing.picard.add_read_groups import AddReadGroups
from poolseq.processing.picard.merge import Merge
from poolseq.processing.picard.validate_sam_file import ValidateSamFile
from poolseq.processing.picard.mark_duplicates import MarkDuplicates
from poolseq.processing.picard.build_bam_index import BuildBamIndex


class Picard():

    def __init__(self, data):
        self.sort = Sort(data)
        self.add_read_groups = AddReadGroups(data)
        self.merge = Merge(data)
        self.validate_sam_file = ValidateSamFile(data)
        self.mark_duplicates = MarkDuplicates(data)
        self.build_bam_index = BuildBamIndex(data)
