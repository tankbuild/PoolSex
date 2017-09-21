import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class Index():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'crisp_index.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_shell_name = 'samtools_index'
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        genotoul.print_header(shell_file,
                              name=base_shell_name)
        shell_file.write(parameters.samtools +
                         ' faidx ' + data.genome_path)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
