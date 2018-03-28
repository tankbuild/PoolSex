import os
import poolseq.genotoul as genotoul


class Mpileup2sync():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'popoolation_mpileup2sync.sh')
        self.shell_file_path = os.path.join(data.directories.shell, 'popoolation_mpileup2sync.sh')

    def generate_shell_files(self, data, parameters):
        shell_file = open(self.shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.results, 'pool.sync')
        input_file_path = os.path.join(data.directories.results, 'pool.mpileup')
        genotoul.print_header(shell_file,
                              threads=parameters.threads,
                              name='popoolation_mpileup2sync')
        shell_file.write(parameters.java +
                         ' -Xmx' + parameters.java_mem +
                         ' -jar ' + parameters.popoolation +
                         ' --input ' + input_file_path +
                         ' --output' + output_file_path +
                         ' --fastq-type sanger' +
                         ' --min-qual 20' +
                         ' --threads ' + parameters.threads)
        shell_file.close()
