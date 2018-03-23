import os
from collections import defaultdict
import poolseq.genotoul as genotoul


class Mapping():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'mapping.sh')
        self.shell_file_path = defaultdict(lambda: dict())
        self.output_file_path = []
        self.job_id = []
        self.prefix = 'bwa_mapping'

    def generate_shell_files(self, data, parameters, sex, lane, mates):
        base_file_name = '_'.join([sex, lane])
        base_shell_name = self.prefix + '_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, base_file_name + '_mapping.bam')
        r1_file_path = os.path.join(data.directories.reads,
                                    base_file_name + '_' + mates[0] + '.fastq.gz')
        r2_file_path = os.path.join(data.directories.reads,
                                    base_file_name + '_' + mates[1] + '.fastq.gz')
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              threads=parameters.threads)
        self.job_id.append(base_shell_name)
        shell_file.write(parameters.bwa + ' mem' +
                         ' -t ' + str(parameters.threads) +
                         ' ' + data.genome_path +
                         ' ' + r1_file_path +
                         ' ' + r2_file_path +
                         ' | samtools view -b -' +
                         ' > ' + output_file_path + '\n')
        shell_file.close()
        self.shell_file_path[sex][lane] = shell_file_path
        self.output_file_path.append(output_file_path)
