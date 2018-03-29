import os
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

    def clean_module_files(self, data):
        '''
        Special implementation of clean_module_files for bwa index because
        output files are special (multiple index files)
        '''
        for instance, instance_data in self.instances.items():
            if os.path.isfile(instance_data['results']):
                os.remove(instance_data['results'])
            if os.path.isfile(instance_data['shell']):
                os.remove(instance_data['shell'])
            output_files = [os.path.join(self.output_folder, f) for
                            f in os.listdir(self.output_folder) if
                            instance in f]
            for output_file in output_files:
                os.remove(output_file)
            results_files = [os.path.join(data.directories.genomes, f) for
                             f in os.listdir(data.directories.genomes)]
            for results_file in results_files:
                if results_file != self.data.genome_path:
                    os.remove(results_file)
