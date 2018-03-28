import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Groups(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            genotoul.print_header(shell_file,
                                  name='_'.join([self.prefix, instance]),
                                  mem=parameters.mem,
                                  h_vmem=parameters.h_vmem)
            genotoul.print_java_module(shell_file)
            shell_file.write(parameters.java +
                             ' -Xmx' + parameters.java_mem + ' \\\n' +
                             '-jar ' + parameters.picard + ' \\\n' +
                             'AddOrReplaceReadGroups' + ' \\\n' +
                             'I=' + self.input[instance]['output'] + ' \\\n' +
                             'O=' + instance_data['output'] + ' \\\n' +
                             'RGID=' + instance_data['sex'] + '_' + instance_data['lane'] + ' \\\n' +
                             'RGLB=' + instance_data['sex'] + ' \\\n' +
                             'RGPL=illumina' + ' \\\n' +
                             'RGSM=' + instance_data['sex'] + '_' + instance_data['lane'] + ' \\\n' +
                             'RGPU=' + instance_data['sex'])
            shell_file.close()
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + self.input[instance]['job_id'] + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
