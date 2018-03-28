import os
from collections import defaultdict


class Module():

    def __init__(self, data, files_info, name, dependency=None):
        self.prefix = data.modules[name]['prefix']
        self.sex = data.modules[name]['sex']
        self.lane = data.modules[name]['lane']
        self.mate = data.modules[name]['mate']
        self.output_format = data.modules[name]['output_format']
        self.instances = defaultdict(lambda: {'shell': None, 'output': None, 'job_id': None,
                                              'sex': None, 'lane': None, 'mates': None, })
        self.get_instances(data, files_info)
        if dependency:
            self.input = dependency.instances
        else:
            self.input = None

    def get_instances(self, data, files_info):
        full_file_name = self.prefix
        if self.sex:
            for sex, lanes in files_info.items():
                instance_sex = sex
                file_sex = '_'.join([full_file_name, sex])
                if self.lane:
                    for lane, mates in lanes.items():
                        instance_lane = '_'.join([instance_sex, lane])
                        file_lane = '_'.join([file_sex, lane])
                        if self.mate:
                            self.fill_instance(data, instance_lane, file_lane, sex=sex, lane=lane, mates=mates)
                        else:
                            self.fill_instance(data, instance_lane, file_lane, sex=sex, lane=lane)
                else:
                    self.fill_instance(data, instance_sex, file_sex, sex=sex)
        else:
            self.fill_instance(data, 'unique', full_file_name)

    def fill_instance(self, data, instance_name, full_file_name, sex=None, lane=None, mates=None):
        self.instances[instance_name]['shell'] = os.path.join(data.directories.shell, full_file_name + '.sh')
        self.instances[instance_name]['output'] = os.path.join(data.directories.results, full_file_name + '.' + self.output_format)
        self.instances[instance_name]['job_id'] = full_file_name
        if sex:
            self.instances[instance_name]['sex'] = sex
        if lane:
            self.instances[instance_name]['lane'] = lane
        if mates:
            self.instances[instance_name]['mates'] = mates
