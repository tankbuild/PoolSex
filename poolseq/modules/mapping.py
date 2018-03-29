import os
import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Mapping(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            r1_file_path = os.path.join(data.directories.reads,
                                        instance + '_' + instance_data['mates'][0] + '.fastq.gz')
            r2_file_path = os.path.join(data.directories.reads,
                                        instance + '_' + instance_data['mates'][1] + '.fastq.gz')
            genotoul.print_header(shell_file,
                                  name='_'.join([self.prefix, instance]),
                                  threads=parameters.threads)
            shell_file.write(parameters.bwa + ' mem \\\n' +
                             '-t ' + str(parameters.threads) + ' \\\n' +
                             '' + data.genome_path + ' \\\n' +
                             '' + r1_file_path + ' \\\n' +
                             '' + r2_file_path + ' \\\n' +
                             '| samtools view -b -' + '\\\n' +
                             '> ' + instance_data['results'] + '\n')
            shell_file.close()
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + self.input['unique']['job_id'] + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
