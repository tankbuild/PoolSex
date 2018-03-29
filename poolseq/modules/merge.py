import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Merge(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            input_file_paths = [d['results'] for
                                d in self.input.values() if
                                d['sex'] == instance_data['sex']]
            shell_file = open(instance_data['shell'], 'w')
            if len(input_file_paths) > 1:
                genotoul.print_header(shell_file,
                                      name='_'.join([self.prefix, instance]),
                                      mem=parameters.mem,
                                      h_vmem=parameters.h_vmem)
                genotoul.print_java_module(shell_file)
                shell_file.write(parameters.java +
                                 ' -Xmx' + parameters.java_mem + ' \\\n' +
                                 '-jar ' + parameters.picard + ' \\\n' +
                                 'MergeSamFiles' + ' \\\n')
                for input_file_path in input_file_paths:
                    shell_file.write('I=' + input_file_path + ' \\\n')
                shell_file.write('O=' + instance_data['results'])
            else:
                genotoul.print_header(shell_file,
                                      name='_'.join([self.prefix, instance]))
                shell_file.write('ln -s ' + input_file_paths[0] +
                                 ' ' + instance_data['results'])
            shell_file.close()
            hold_ids = [d['job_id'] for
                        d in self.input.values() if
                        d['sex'] == instance_data['sex']]
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + ','.join(hold_ids) + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
