import os
import poolseq.genotoul as genotoul


class Mpileup():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'samtools_mpileup.sh')
        self.shell_file_path = os.path.join(data.directories.shell, 'samtools_mpileup.sh')
        self.job_id = 'samtools_mpileup'

    def generate_shell_files(self, data, parameters, sexes):
        shell_file = open(self.shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, 'pool.mpileup')
        input_file_path = [os.path.join(data.directories.output, sex + '_no_duplicates.bam')for sex in sexes]
        genotoul.print_header(shell_file,
                              threads=parameters.threads,
                              name=self.job_id)
        shell_file.write(parameters.samtools +
                         ' mpileup -B' +
                         ' -f ' + data.genome_path +
                         ' -o ' + output_file_path +
                         ' ' + ' '.join([i for i in input_file_path]))
        shell_file.close()
