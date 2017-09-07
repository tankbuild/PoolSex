import os


class Output():

    def __init__(self, directories):
        self.directories = directories

    def mapping(self, info=None):
        file_name = '_'.join([info['sex'], info['lane']]) + '.bam'
        return(os.path.join(self.directories.results, file_name))

    def mapping_list(self):
        return [os.path.join(self.directories.results, f) for
                f in os.listdir(self.directories.results) if
                f.endswith('.bam')]

    def picard_sort(self, bam_file_name):
        output_file_name = bam_file_name.replace('.bam', '_sorted.bam')
        return os.path.join(self.directories.results, output_file_name)

    def picard_sort_list(self):
        return [os.path.join(self.directories.results, f) for
                f in os.listdir(self.directories.results) if
                f.endswith('_sorted.bam')]

    def picard_add_read_groups(self, bam_file_name):
        output_file_name = bam_file_name.replace('_sorted.bam', '_read_groups.bam')
        return os.path.join(self.directories.results, output_file_name)

    def picard_add_read_groups_list(self):
        return [os.path.join(self.directories.results, f) for
                f in os.listdir(self.directories.results) if
                f.endswith('_read_groups.bam')]
