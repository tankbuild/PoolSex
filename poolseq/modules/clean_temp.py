import poolseq.genotoul as genotoul
from poolseq.modules.module import Module


class CleanTemp(Module):

    def generate_shell_files(self, modules, qsub_file, hold=True):
        modules_to_keep = ['index', 'duplicates', 'mpileup2sync', 'clean_temp']
        for instance, instance_data in self.instances.items():
            shell_file = open(instance_data['shell'], 'w')
            genotoul.print_header(shell_file,
                                  name=instance_data['job_id'])
            for module, module_data in modules.items():
                if module not in modules_to_keep:
                    shell_file.write('rm -rf ' + ' '.join((instance['results']) for
                                                          instance in module_data.instances.values()) + '\n')
            shell_file.close()
            qsub_file.write('qsub ')
            hold_ids = [d['job_id'] for d in self.input.values()]
            qsub_file.write('qsub ')
            if hold:
                qsub_file.write('-hold_jid ' + ','.join(hold_ids) + ' ')
            qsub_file.write(instance_data['shell'] + '\n')
