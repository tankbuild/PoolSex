import os


class Output():

    def __init__(self, directories):
        self.directories = directories

    def mapping(self, info=None):
        if not info:
            return [f for f in os.listdir(self.directories.results) if
                    f.endswith('.bam')]
        else:
            file_name = '_'.join([info['sex'], info['lane']]) + '.bam'
            return(os.path.join(self.directories.results, file_name))
