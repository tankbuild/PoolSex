import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class Merge():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'picard_merge.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters, sex, lanes):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_file_name = sex
        base_shell_name = 'picard_merge_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, base_file_name + '.bam')
        lane_file_paths = [os.path.join(data.directories.output, sex + '_' + lane + '.bam') for
                           lane in lanes]
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem)
        genotoul.print_java_module(shell_file)
        shell_file.write(parameters.java +
                         ' -Xmx' + parameters.java_mem +
                         ' -jar ' + parameters.picard +
                         ' MergeSamFiles')
        for lane_file_path in lane_file_paths:
            shell_file.write(' I=' + lane_file_path)
        shell_file.write(' O=' + output_file_path +
                         ' SORT_ORDER=coordinate')
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        self.output_file_path.append(output_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
