import os
from poolseq.data.directories import Directories
from poolseq.data.files import Files


class Data():

    def __init__(self, root_dir):
        self.directories = Directories(root_dir)
        self.files = Files(root_dir)
        self.genome_path = self.get_genome_path()
        self.reads_paths = self.get_reads_path()
        self.modules = {'index': {'prefix': 'index', 'output_format': '', 'sex': False, 'lane': False, 'mate': False},
                        'mapping': {'prefix': 'mapping', 'output_format': 'bam', 'sex': True, 'lane': True, 'mate': True},
                        'sort': {'prefix': 'sort', 'output_format': 'bam', 'sex': True, 'lane': True, 'mate': False},
                        'groups': {'prefix': 'groups', 'output_format': 'bam', 'sex': True, 'lane': True, 'mate': False},
                        'merge': {'prefix': 'merge', 'output_format': 'bam', 'sex': True, 'lane': False, 'mate': False},
                        'duplicates': {'prefix': 'duplicates', 'output_format': 'bam', 'sex': True, 'lane': False, 'mate': False},
                        'mpileup': {'prefix': 'mpileup', 'output_format': 'pileup', 'sex': False, 'lane': False, 'mate': False},
                        'mpileup2sync': {'prefix': 'mpileup2sync', 'output_format': 'sync', 'sex': False, 'lane': False, 'mate': False}}

    def get_genome_path(self):
        file = [f for f in os.listdir(self.directories.genomes) if f.endswith('.fasta')][0]
        return os.path.join(self.directories.genomes, file)

    def get_reads_path(self):
        return [os.path.join(self.directories.reads, f) for
                f in os.listdir(self.directories.reads) if
                f.endswith('.fastq.gz') or f.endswith('.fasta.gz') or
                f.endswith('.fastq') or f.endswith('.fasta')]
