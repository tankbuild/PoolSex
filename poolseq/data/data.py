import os
from poolseq.data.directories import Directories
from poolseq.data.files import Files


class Data():

    def __init__(self, root_dir):
        self.directories = Directories(root_dir)
        self.files = Files(root_dir)
        self.genome_path = self.get_genome_path()
        self.reads_paths = self.get_reads_path()
        self.modules = {'index': {'prefix': 'index', 'results_format': '', 'sex': False, 'lane': False, 'mate': False, 'pairwise': False},
                        'mapping': {'prefix': 'mapping', 'results_format': 'bam', 'sex': True, 'lane': True, 'mate': True, 'pairwise': False},
                        'sort': {'prefix': 'sort', 'results_format': 'bam', 'sex': True, 'lane': True, 'mate': False, 'pairwise': False},
                        'groups': {'prefix': 'groups', 'results_format': 'bam', 'sex': True, 'lane': True, 'mate': False, 'pairwise': False},
                        'merge': {'prefix': 'merge', 'results_format': 'bam', 'sex': True, 'lane': False, 'mate': False, 'pairwise': False},
                        'duplicates': {'prefix': 'duplicates', 'results_format': 'bam', 'sex': True, 'lane': False, 'mate': False, 'pairwise': False},
                        'mpileup': {'prefix': 'mpileup', 'results_format': 'pileup', 'sex': False, 'lane': False, 'mate': False, 'pairwise': True},
                        'mpileup2sync': {'prefix': 'mpileup2sync', 'results_format': 'sync', 'sex': False, 'lane': False, 'mate': False, 'pairwise': True},
                        'clean_temp': {'prefix': 'clean_temp', 'results_format': '', 'sex': False, 'lane': False, 'mate': False, 'pairwise': False}}

    def get_genome_path(self):
        file = [f for f in os.listdir(self.directories.genomes) if f.endswith('.fasta')][0]
        return os.path.join(self.directories.genomes, file)

    def get_reads_path(self):
        return [os.path.join(self.directories.reads, f) for
                f in os.listdir(self.directories.reads) if
                f.endswith('.fastq.gz') or f.endswith('.fasta.gz') or
                f.endswith('.fastq') or f.endswith('.fasta')]
