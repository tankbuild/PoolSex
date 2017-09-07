import os
import itertools
import poolseq.genotoul as genotoul


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
        file_pairs = self.find_pairs(self.structure.data.reads())
        qsub_file = open(self.structure.qsub.mapping(), 'w')
        for pair in file_pairs:
            info = self.get_info(pair[0])
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

    def get_info(self, reads_file_path):
        dir_path, file_path = os.path.split(reads_file_path)
        file_path = file_path.replace('.fastq.gz', '')
        fields = file_path.split('_')
        info = {}
        info['species'] = fields[0] + '_' + fields[1]
        info['sex'] = fields[2]
        info['lane'] = fields[3]
        info['mate'] = fields[4]
        return info

    def find_pairs(self, reads_files_paths):
        info = {path: self.get_info(path) for path in reads_files_paths}
        pairs = []
        for file_1, file_2 in itertools.combinations(info.keys(), 2):
            if (info[file_1]['sex'] == info[file_2]['sex'] and
                    info[file_1]['lane'] == info[file_2]['lane'] and
                    info[file_1]['mate'] != info[file_2]['mate']):
                pairs.append((file_1, file_2))
        return pairs
