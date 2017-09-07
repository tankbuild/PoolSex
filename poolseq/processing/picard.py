import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class Picard():

    def __init__(self, structure, parameters):
        self.structure = structure
        self.parameters = parameters

    def sort(self):
        qsub_file = open(self.structure.qsub.picard_sort(), 'w')
        for bam_file in self.structure.output.mapping_list():
            bam_file_name = os.path.split(bam_file)[1]
            shell_file_path = self.structure.shell.picard_sort(bam_file_name)
            shell_file = open(shell_file_path, 'w')
            genotoul.print_header(shell_file,
                                  name='picard_sort_' + bam_file_name.replace('.bam', ''),
                                  mem=self.parameters.mem,
                                  h_vmem=self.parameters.h_vmem)
            genotoul.print_java_module(shell_file)
            shell_file.write(self.parameters.java +
                             ' -Xmx' + self.parameters.java_mem +
                             ' -jar ' + self.parameters.picard +
                             ' SortSam' +
                             ' I=' + bam_file +
                             ' O=' + self.structure.output.picard_sort(bam_file_name) +
                             ' SORT_ORDER=coordinate')
            shell_file.close()
            qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()

    def merge(self):
        pass

    def add_read_groups(self):
        qsub_file = open(self.structure.qsub.picard_add_read_groups(), 'w')
        for bam_file in self.structure.output.picard_sort_list():
            bam_file_name = os.path.split(bam_file)[1].replace('_sorted', '')
            shell_file_path = self.structure.shell.picard_add_read_groups(bam_file_name)
            shell_file = open(shell_file_path, 'w')
            info = file_utils.get_info(bam_file)
            genotoul.print_header(shell_file,
                                  name='picard_add_read_groups_' + bam_file_name.replace('.bam', ''),
                                  mem=self.parameters.mem,
                                  h_vmem=self.parameters.h_vmem)
            genotoul.print_java_module(shell_file)
            shell_file.write(self.parameters.java +
                             ' -Xmx' + self.parameters.java_mem +
                             ' -jar ' + self.parameters.picard +
                             ' AddOrReplaceReadGroups' +
                             ' I=' + bam_file +
                             ' O=' + self.structure.output.picard_add_read_groups(bam_file_name) +
                             ' RGID=' + info['sex'] + '_' + info['lane'] +
                             ' RGLB=' + info['sex'] +
                             ' RGPL=illumina' +
                             ' RGSM=' + info['sex'] + '_' + info['lane'] +
                             ' RGPU=' + info['sex'])
            shell_file.close()
            qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()

    def validate(self):
        pass
