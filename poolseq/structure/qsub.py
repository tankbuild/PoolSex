import os


class Qsub():

    def __init__(self, directories):
        self.directories = directories

    def bwa_index(self):
        return os.path.join(self.directories.qsub, 'bwa_index.sh')

    def mapping(self):
        return os.path.join(self.directories.qsub, 'mapping.sh')

    def picard_sort(self):
        return os.path.join(self.directories.qsub, 'picard_sort.sh')

    def picard_add_read_groups(self):
        return os.path.join(self.directories.qsub, 'picard_add_read_groups.sh')

    def picard_merge(self):
        return os.path.join(self.directories.qsub, 'picard_merge.sh')
