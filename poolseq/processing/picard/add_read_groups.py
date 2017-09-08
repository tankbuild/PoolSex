import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class AddReadGroups():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'picard_add_read_groups.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters, sex, lane):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_file_name = '_'.join([sex, lane])
        base_shell_name = 'picard_add_read_groups_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, base_file_name + '_read_groups.bam')
        input_file_path = os.path.join(data.directories.output, base_file_name + '_sorted.bam')
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem)
        genotoul.print_java_module(shell_file)
        shell_file.write(parameters.java +
                         ' -Xmx' + parameters.java_mem +
                         ' -jar ' + parameters.picard +
                         ' AddOrReplaceReadGroups' +
                         ' I=' + input_file_path +
                         ' O=' + output_file_path +
                         ' RGID=' + sex + '_' + lane +
                         ' RGLB=' + sex +
                         ' RGPL=illumina' +
                         ' RGSM=' + sex + '_' + lane +
                         ' RGPU=' + sex)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        self.output_file_path.append(output_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
