import os
from collections import defaultdict
import poolseq.genotoul as genotoul


class AddReadGroups():

    def __init__(self, data, files_info):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'picard_add_read_groups.sh')
        self.shell_file_path = defaultdict(lambda: dict())
        self.output_file_path = []
        self.job_id = []
        self.prefix = 'picard_add_read_groups'

    def generate_shell_files(self, data, parameters, sex, lane):
        base_file_name = '_'.join([sex, lane])
        base_shell_name = self.prefix + '_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.results, base_file_name + '_read_groups.bam')
        input_file_path = os.path.join(data.directories.results, base_file_name + '_sorted.bam')
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem)
        self.job_id.append(base_shell_name)
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
        self.shell_file_path[sex][lane] = shell_file_path
        self.output_file_path.append(output_file_path)
