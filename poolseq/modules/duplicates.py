import os
import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class Duplicates(Module):

    def generate_shell_files(self, data, parameters, qsub_file, hold=True):
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            log_file_path = os.path.join(data.directories.results, instance + '_duplicates.txt')
            genotoul.print_header(shell_file,
                                  name='_'.join([self.prefix, instance]),
                                  mem=parameters.mem,
                                  h_vmem=parameters.h_vmem)
            genotoul.print_java_module(shell_file)
            shell_file.write(parameters.java +
                             ' -Xmx' + parameters.java_mem + ' \\\n' +
                             '-Djava.io.tmpdir=' + parameters.java_temp_dir + ' \\\n' +
                             '-jar ' + parameters.picard + ' \\\n' +
                             'MarkDuplicates' + ' \\\n' +
                             'I=' + self.input[instance]['results'] + ' \\\n' +
                             'O=' + instance_data['results'] + ' \\\n' +
                             'M=' + log_file_path + ' \\\n' +
                             'TMP_DIR=' + parameters.java_temp_dir + ' \\\n' +
                             'MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=' + parameters.max_file_handles + ' \\\n' +
                             'REMOVE_DUPLICATES=true')
            shell_file.close()
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + self.input[instance]['job_id'] + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
