import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Mpileup2sync(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            genotoul.print_header(shell_file,
                                  name=instance_data['job_id'],
                                  threads=parameters.threads)
            genotoul.print_java_module(shell_file)
            shell_file.write(parameters.java +
                             ' -Xmx' + parameters.java_mem + ' \\\n' +
                             '-jar ' + parameters.popoolation + ' \\\n' +
                             '--input ' + self.input[instance]['results'] + ' \\\n' +
                             '--output' + instance_data['results'] + ' \\\n' +
                             '--fastq-type sanger' + ' \\\n' +
                             '--min-qual 20' + ' \\\n' +
                             '--threads ' + parameters.threads)
            shell_file.close()
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + self.input[instance]['job_id'] + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
