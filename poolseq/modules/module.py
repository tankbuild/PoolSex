import os
from collections import defaultdict


class Module():

    def __init__(self, data, files_info, name, dependency=None):
        self.prefix = data.modules[name]['prefix']
        self.sex = data.modules[name]['sex']
        self.lane = data.modules[name]['lane']
        self.mate = data.modules[name]['mate']
        self.results_format = data.modules[name]['results_format']
        self.instances = defaultdict(lambda: {'shell': None, 'results': None, 'job_id': None,
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
        self.instances[instance_name]['results'] = os.path.join(data.directories.results, full_file_name + '.' + self.results_format)
        self.instances[instance_name]['job_id'] = full_file_name
        if sex:
            self.instances[instance_name]['sex'] = sex
        if lane:
            self.instances[instance_name]['lane'] = lane
        if mates:
            self.instances[instance_name]['mates'] = mates

    def clean_module_files(self, data):
        for instance in self.instances.values():
            if os.path.isfile(instance['results']):
                os.remove(instance['results'])
            if os.path.isfile(instance['shell']):
                os.remove(instance['shell'])
            output_files = [os.path.join(data.directories.output, f) for
                            f in os.listdir(data.directories.output) if
                            f.split('.')[0] == instance['job_id']]
            for output_file in output_files:
                os.remove(output_file)

    def was_successful(self, data):
        success = True
        for instance in self.instances.values():
            output_files = [os.path.join(data.directories.output, f) for
                            f in os.listdir(data.directories.output) if
                            f.split('.')[0] == instance['job_id'] and
                            f.split('.')[1][0] == 'o']
            if len(output_files) == 0:
                success = False
            elif len(output_files) == 1:
                if not self.test_output_file(output_files[0]):
                    success = False
            else:
                edit_times = {file: os.path.getmtime(file) for file in output_files}
                last_file = max(edit_times, key=edit_times.get)
                if not self.test_output_file(last_file):
                    success = False
        return success

    def test_output_file(self, output_file_path):
        success = True
        file = open(output_file_path)
        line = 'a'
        while line:
            temp = file.readline()
            if temp:
                line = temp
            else:
                break
        if not line.startswith('Epilog : job finished'):
            success = False
        return success
