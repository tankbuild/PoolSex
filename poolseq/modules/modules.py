from poolseq.modules.index import Index
from poolseq.modules.mapping import Mapping
from poolseq.modules.sort import Sort
from poolseq.modules.groups import Groups
from poolseq.modules.merge import Merge
from poolseq.modules.duplicates import Duplicates
from poolseq.modules.mpileup import Mpileup
from poolseq.modules.mpileup2sync import Mpileup2sync
from poolseq.modules.clean_temp import CleanTemp


class Modules():

    def __init__(self, data, files_info):
        self.index = Index(data, files_info, 'index')
        self.mapping = Mapping(data, files_info, 'mapping', dependency=self.index)
        self.sort = Sort(data, files_info, 'sort', dependency=self.mapping)
        self.groups = Groups(data, files_info, 'groups', dependency=self.sort)
        self.merge = Merge(data, files_info, 'merge', dependency=self.groups)
        self.duplicates = Duplicates(data, files_info, 'duplicates', dependency=self.merge)
        self.mpileup = Mpileup(data, files_info, 'mpileup', dependency=self.duplicates)
        self.mpileup2sync = Mpileup2sync(data, files_info, 'mpileup2sync', dependency=self.mpileup)
        self.clean_temp = CleanTemp(data, files_info, 'clean_temp', dependency=self.mpileup2sync)
