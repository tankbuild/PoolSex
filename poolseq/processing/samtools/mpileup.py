import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class Mpileup():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'samtools_mpileup.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters, sex):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_file_name = sex
        base_shell_name = 'samtools_mpileup_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, base_file_name + '.vcf')
        input_file_path = os.path.join(data.directories.output, base_file_name + '_no_duplicates.bam')
        genotoul.print_header(shell_file,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem,
                              name=base_shell_name)
        shell_file.write(parameters.samtools +
                         ' mpileup' +
                         ' -f ' + data.genome_path +
                         ' -o ' + output_file_path +
                         ' -Auv' +
                         ' -t DP,AD' +
                         ' ' + input_file_path)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
