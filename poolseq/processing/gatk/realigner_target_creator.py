import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class RealignerTargetCreator():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'gatk_realigner_target_creator.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters, sex):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_file_name = sex
        base_shell_name = 'gatk_realigner_target_creator_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.results, base_file_name + '.intervals')
        input_file_path = os.path.join(data.directories.results, base_file_name + '_no_duplicates.bam')
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem)
        genotoul.print_java_module(shell_file)
        shell_file.write(parameters.java +
                         ' -Xmx' + parameters.java_mem +
                         ' -jar ' + parameters.gatk +
                         ' -T RealignerTargetCreator' +
                         ' -I ' + input_file_path +
                         ' -o ' + output_file_path +
                         ' -R ' + data.genome_path)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        self.output_file_path.append(output_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
