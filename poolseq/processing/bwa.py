import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class Bwa():

    def __init__(self, structure, parameters):
        self.structure = structure
        self.parameters = parameters

    def index(self):
        qsub_file = open(self.structure.qsub.bwa_index(), 'w')
        shell_file = open(self.structure.shell.bwa_index(), 'w')
        genotoul.print_header(shell_file, name='bwa_index')
        shell_file.write(self.parameters.bwa + ' index ' +
                         self.structure.data.genome() + '\n')
        shell_file.close()
        qsub_file.write('qsub ' + self.structure.shell.bwa_index())
        qsub_file.close()

    def mapping(self):
        file_pairs = file_utils.find_pairs(self.structure.data.reads())
        qsub_file = open(self.structure.qsub.mapping(), 'w')
        for pair in file_pairs:
            info = file_utils.get_info(pair[0])
            shell_file_path = self.structure.shell.mapping(info)
            shell_file = open(shell_file_path, 'w')
            genotoul.print_header(shell_file,
                                  name='mapping_' + info['sex'] + '_' + info['lane'],
                                  threads=self.parameters.threads)
            shell_file.write(self.parameters.bwa + ' mem' +
                             ' -t ' + str(self.parameters.threads) +
                             ' ' + self.structure.data.genome() +
                             ' ' + pair[0] +
                             ' ' + pair[1] +
                             ' | samtools view -b -' +
                             ' > ' + self.structure.output.mapping(info) + '\n')
            shell_file.close()
            qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
