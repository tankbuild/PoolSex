import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class VariantCalling():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'crisp_variant_calling.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_shell_name = 'crisp_variant_calling'
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output + 'results.vcf')
        male_file_path = os.path.join(data.directories.output, 'male_no_duplicates.bam')
        female_file_path = os.path.join(data.directories.output, 'female_no_duplicates.bam')
        pool_size = 2 * int(parameters.number_of_individuals)
        genotoul.print_header(shell_file,
                              name=base_shell_name)
        shell_file.write(parameters.crisp +
                         ' --bam ' + male_file_path +
                         ' --bam ' + female_file_path +
                         ' --VCF ' + output_file_path +
                         ' --ref ' + data.genome_path +
                         ' --poolsize ' + str(pool_size) +
                         ' --minc ' + parameters.min_number_of_reads)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        self.output_file_path.append(output_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
