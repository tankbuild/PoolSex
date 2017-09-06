from directory_structure import *
import settings
import genotoul
import utils


def generate_shell_files():

    file_pairs = utils.find_pairs(READS_PATH)
    qsub_file = open(MAPPING_SH, 'w')
    for pair in file_pairs:
        info = utils.reads_file_info(pair[0])
        shell_file_path = mapping_sh(info)
        shell_file = open(shell_file_path, 'w')
        genotoul.header(shell_file,
                        name='mapping_' + info['sex'] + '_' + info['lane'],
                        threads=settings.threads)
        shell_file.write('bwa mem' +
                         ' -t ' + str(settings.threads) +
                         ' ' + GENOME_PATH +
                         ' ' + pair[0] +
                         ' ' + pair[1] +
                         ' | samtools view -b -' +
                         ' >' + mapping_output(info) + '\n')
        shell_file.close()
        qsub_file.write('qsub ' + shell_file_path + '\n')