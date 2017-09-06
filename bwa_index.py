from directory_structure import *
import genotoul


def generate_shell_file():
    qsub_file = open(BWA_INDEX_SH, 'w')
    genotoul.header(qsub_file, name='bwa_index')
    qsub_file.write('bwa index ' + GENOME_PATH + '\n')
    qsub_file.close()
