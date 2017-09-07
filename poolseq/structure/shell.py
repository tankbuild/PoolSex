import os


class Shell():

    def __init__(self, directories):
        self.directories = directories

    def index(self):
        return os.path.join(self.directories.shell, 'bwa_index.sh')

    def mapping(self, info):
        file_name = '_'.join(['mapping', info['sex'], info['lane']]) + '.sh'
        return(os.path.join(self.directories.shell, file_name))

    def picard_sort(self, bam_file_name):
        file_name = 'picard_sort_' + bam_file_name.replace('.bam', '.sh')
        return os.path.join(self.directories.shell, file_name)
