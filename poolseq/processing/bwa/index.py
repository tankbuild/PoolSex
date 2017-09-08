import os
import poolseq.genotoul as genotoul


class Index():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'bwa_index.sh')
        self.shell_file_path = os.path.join(data.directories.shell, 'bwa_index.sh')

    def generate_files(self, data, parameters):
        qsub_file = open(self.qsub_file_path, 'w')
        shell_file = open(self.shell_file_path, 'w')
        genotoul.print_header(shell_file, name='bwa_index')
        shell_file.write(parameters.bwa + ' index ' +
                         data.genome_path + '\n')
        shell_file.close()
        qsub_file.write('qsub ' + self.shell_file_path)
        qsub_file.close()
