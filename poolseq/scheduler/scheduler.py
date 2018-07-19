import re
import subprocess
from poolseq.data import variables


class Scheduler:

    def __init__(self, name, data):
        self.parameters_flags = data.schedulers[name][variables.schedulers_options.parameters]
        self.parameter_prefix = data.schedulers[name][variables.schedulers_options.parameter_prefix]
        self.modules = data.schedulers[name][variables.schedulers_options.modules]
        self.job_id_regex = data.schedulers[name][variables.schedulers_options.job_id_regex]
        self.submit_command = data.schedulers[name][variables.schedulers_options.submit_command]
        self.hold_command = data.schedulers[name][variables.schedulers_options.hold_command]

    def write_header(self, file, module, parameters, instance_data):
        file.write('#!/bin/sh' + '\n')
        for option in module.data[variables.modules_options.options]:
            value = None
            if option in parameters.keys():
                value = parameters[option]
            elif option in [variables.submit_options.output, variables.submit_options.error]:
                value = instance_data[option]
            elif option == variables.submit_options.name:
                value = instance_data[variables.instance_options.shell_name]
            if self.parameters_flags[option] and value:
                file.write(self.parameter_prefix + self.parameters_flags[option] + value + '\n')
        file.write('\n')
        file.write('module purge' + '\n')
        file.write('\n')
        for module_to_load in self.modules[module.name]:
            file.write('module load ' + module_to_load + '\n')
        if len(self.modules[module.name]) > 0:
            file.write('\n')

    def write_shell_file(self, module, instance_data, data, parameters):
        shell_file = open(instance_data[variables.instance_options.shell], 'w')
        self.write_header(shell_file, module, parameters, instance_data)
        shell_file.write(module.data[variables.modules_options.command](data, parameters, instance_data))
        shell_file.close()

    def submit(self, instance_data, hold_ids=None):
        dependencies = [h for instance, h in hold_ids.items() if
                        instance_data[variables.instance_options.dependencies] and
                        instance in instance_data[variables.instance_options.dependencies]]
        command = self.submit_command + ' '
        if hold_ids:
            command += self.hold_command + ','.join(dependencies) + ' '
        command += instance_data[variables.instance_options.shell]
        try:
            print('Submitting job \"' + instance_data[variables.instance_options.shell_name] + '\"')
            output = subprocess.check_output(command, shell=True).decode()
            job_id = self.get_job_id(output)
        except subprocess.CalledProcessError:
            job_id = None
            print(' - Error: could not submit file \"' + instance_data[variables.instance_options.shell] + '\". Command submitted: ' + command + '\"')
        return job_id

    def get_job_id(self, line):
        search_results = re.search(self.job_id_regex, line)
        if search_results and len(search_results.groups()) == 1:
            return search_results.group(1)
        else:
            print(' - Error: could not retrieve job id from line : \"' + line[:-1] + '\".')
            exit(1)
