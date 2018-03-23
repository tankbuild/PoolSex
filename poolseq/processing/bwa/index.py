import os
import poolseq.genotoul as genotoul


class Index():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'bwa_index.sh')
        self.shell_file_path = os.path.join(data.directories.shell, 'bwa_index.sh')
        self.job_id = 'bwa_index'

    def generate_files(self, data, parameters):
        shell_file = open(self.shell_file_path, 'w')
        genotoul.print_header(shell_file, name='bwa_index')
        shell_file.write(parameters.bwa + ' index ' +
                         data.genome_path + '\n')
        shell_file.close()
