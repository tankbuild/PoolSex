import os
from poolseq.data.directories import Directories


class Data():

    def __init__(self, root_dir):
        self.directories = Directories(root_dir)
        self.genome_path = self.get_genome_path()
        self.reads_paths = self.get_reads_path()

    def get_genome_path(self):
        temp = [f for f in os.listdir(self.directories.genomes) if f.endswith('.fasta')]
        if len(temp) == 0:
            print(' Error: genome file not found')
        elif len(temp) > 1:
            print(' Error: found ' + str(len(temp)) + ' genome files. There should be only 1.')
        file = temp[0]
        return os.path.join(self.directories.genomes, file)

    def get_reads_path(self):
        files = [f for f in os.listdir(self.directories.reads) if f.endswith('.fastq.gz')]
        if len(files) < 2:
            print('- Error: reads files not found')
        return [os.path.join(self.directories.reads, f) for
                f in os.listdir(self.directories.reads) if
                f.endswith('.fastq.gz') or f.endswith('.fasta.gz') or
                f.endswith('.fastq') or f.endswith('.fasta')]
