import os
import itertools
from collections import defaultdict
from poolsex.data import variables


class Module():

    def __init__(self, name, module_data, data, files_info):
        self.data = module_data
        self.name = name
        self.instances = defaultdict(lambda: {variables.instance_options.name: None,
                                              variables.instance_options.shell: None,
                                              variables.instance_options.shell_name: None,
                                              variables.instance_options.output: None,
                                              variables.instance_options.error: None,
                                              variables.instance_options.input: None,
                                              variables.instance_options.dependencies: None,
                                              variables.instance_options.results: None,
                                              variables.instance_options.sex: None,
                                              variables.instance_options.lane: None,
                                              variables.instance_options.mates: None})
        self.get_instances(data, files_info)

    def get_instances(self, data, files_info):
        if self.data[variables.modules_options.sex]:
            for sex, lanes in files_info.items():
                if self.data[variables.modules_options.lane]:
                    for lane, mates in lanes.items():
                        instance_name = '_'.join([sex, lane])
                        if self.data[variables.modules_options.mate]:
                            self.fill_instance(data, instance_name, sex=sex, lane=lane, mates=mates)
                        else:
                            self.fill_instance(data, instance_name, sex=sex, lane=lane)
                else:
                    instance_name = sex
                    self.fill_instance(data, instance_name, sex=sex)
        else:
            if self.data[variables.modules_options.pairwise]:
                for sex1, sex2 in itertools.combinations(sorted(files_info.keys()), 2):
                    instance_name = '_'.join([sex1, sex2])
                    self.fill_instance(data, instance_name)
            else:
                self.fill_instance(data, 'unique')

    def fill_instance(self, data, instance_name, sex=None, lane=None, mates=None):
        if instance_name != 'unique':
            suffix = '_' + instance_name
        else:
            suffix = ''
        self.instances[instance_name][variables.instance_options.shell] = os.path.join(data.directories[variables.directories.shell], self.data[variables.modules_options.prefix] + suffix + '.sh')
        self.instances[instance_name][variables.instance_options.shell_name] = self.data[variables.modules_options.prefix] + suffix
        self.instances[instance_name][variables.instance_options.output] = os.path.join(data.directories[variables.directories.output], self.data[variables.modules_options.prefix] + suffix + '.output')
        self.instances[instance_name][variables.instance_options.error] = os.path.join(data.directories[variables.directories.output], self.data[variables.modules_options.prefix] + suffix + '.error')
        if self.data[variables.modules_options.results_format]:
            self.instances[instance_name][variables.instance_options.results] = os.path.join(data.directories[variables.directories.results],
                                                                                             self.data[variables.modules_options.prefix] +
                                                                                             suffix +
                                                                                             '.' + self.data[variables.modules_options.results_format])
        self.instances[instance_name][variables.instance_options.name] = instance_name
        self.instances[instance_name][variables.instance_options.sex] = sex
        self.instances[instance_name][variables.instance_options.lane] = lane
        self.instances[instance_name][variables.instance_options.mates] = mates

    def clean_module_files(self):
        for instance in self.instances.values():
            if instance[variables.instance_options.results] and os.path.isfile(instance[variables.instance_options.results]):
                os.remove(instance[variables.instance_options.results])
            if instance[variables.instance_options.shell] and os.path.isfile(instance[variables.instance_options.shell]):
                os.remove(instance[variables.instance_options.shell])
            if instance[variables.instance_options.output] and os.path.isfile(instance[variables.instance_options.output]):
                os.remove(instance[variables.instance_options.output])
            if instance[variables.instance_options.error] and os.path.isfile(instance[variables.instance_options.error]):
                os.remove(instance[variables.instance_options.error])

    def was_successful(self):
        for instance in self.instances.values():
            try:
                file = open(instance[variables.directories.output])
            except OSError:
                return False
            line = 'a'
            while line:
                temp = file.readline()
                if temp:
                    line = temp
                else:
                    break
            if not line.startswith('Epilog : job finished'):
                return False
        return True
