import os

temp = os.path.dirname(os.path.abspath(__file__))

# Directories
ROOT_DIR = os.path.join(*temp.split('/')[:-1])  # Splat (*) unpacks list arguments
GENOMES_DIR = os.path.join(ROOT_DIR, 'genomes')
QSUB_DIR = os.path.join(ROOT_DIR, 'qsub')
READS_DIR = os.path.join(ROOT_DIR, 'reads')
RESULTS_DIR = os.path.join(ROOT_DIR, 'results')
SCRIPTS_DIR = os.path.join(ROOT_DIR, 'scripts')
SHELL_DIR = os.path.join(ROOT_DIR, 'shell')

# Genome
temp = [f for f in os.listdir(GENOMES_DIR) if f.endswith('.fasta')]
if len(temp) == 0:
    print(' Error: genome file not found')
elif len(temp) > 1:
    print(' Error: found ' + str(len(temp)) + ' genome files. There should be only 1.')
GENOME_FILE = temp[0]
GENOME_PATH = os.path.join(GENOMES_DIR, GENOME_FILE)

# Reads
READS_FILE = [f for f in os.listdir(READS_DIR) if f.endswith('.fastq.gz')]
if len(READS_FILE) < 2:
    print('- Error: reads files not found')
READS_PATH = [os.path.join(READS_DIR, f) for f in os.listdir(READS_DIR) if
              f.endswith('.fastq.gz')]

# Qsub files paths
BWA_INDEX_SH = os.path.join(QSUB_DIR, 'bwa_index.sh')
REMAPPING_SH = os.path.join(QSUB_DIR, 'mapping.sh')


# Shell files (for batch qsub)
def remapping_sh(info):
    file_name = '_'.join(['mapping', info['sex'], info['lane']]) + '.sh'
    return(os.path.join(SHELL_DIR, file_name))


# Output files
def remapping_output(info):
    file_name = '_'.join([info['sex'], info['lane']]) + '.bam'
    return(os.path.join(RESULTS_DIR, file_name))
