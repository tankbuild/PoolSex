import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Index(Module):

    def generate_shell_files(self, data, parameters, qsub_file):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            genotoul.print_header(shell_file,
                                  name=self.prefix)
            shell_file.write(parameters.bwa + ' index ' +
                             data.genome_path + '\n')
            shell_file.close()
            qsub_file.write('qsub ' + instance_data['shell'] + '\n')
