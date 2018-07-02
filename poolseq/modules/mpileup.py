import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Mpileup(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            input_file_paths = sorted([d['results'] for d in self.input.values()])
            genotoul.print_header(shell_file,
                                  name=instance_data['job_id'],
                                  threads=parameters.threads)
            genotoul.print_java_module(shell_file)
            shell_file.write(parameters.samtools +
                             ' mpileup -B -Q 0' + ' \\\n' +
                             '-f ' + data.genome_path + ' \\\n' +
                             '-o ' + instance_data['results'] + ' \\\n' +
                             ' '.join([i for i in input_file_paths]))
            shell_file.close()
            hold_ids = [d['job_id'] for d in self.input.values()]
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + ','.join(hold_ids) + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
