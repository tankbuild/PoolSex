import os


class Output():

    def __init__(self, directories):
        self.directories = directories

    def mapping(self, info=None):
        if not info:
            return [os.path.join(self.directories.results, f) for
                    f in os.listdir(self.directories.results) if
                    f.endswith('.bam')]
        else:
            file_name = '_'.join([info['sex'], info['lane']]) + '.bam'
            return(os.path.join(self.directories.results, file_name))

    def picard_sort(self, bam_file_name):
        output_file_name = bam_file_name.replace('.bam', '_sorted.bam')
        return output_file_name
