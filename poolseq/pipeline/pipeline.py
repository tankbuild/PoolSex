import os
from collections import defaultdict
from poolseq.data import Data
from poolseq.parameters import Parameters
from poolseq.parser import Parser
from poolseq.modules import Modules
from poolseq.tests import user_check_clean


class Pipeline():

    def __init__(self, arguments):
        self.parser = Parser(arguments)
        self.data = Data(self.parser.arguments.input_folder)
        self.qsub_file_path = os.path.join(self.data.directories.qsub, 'run_pipeline.sh')
        self.parameters = Parameters(self.data)
        self.files_info = self.get_files_info()
        self.modules = Modules(self.data, self.files_info)
        self.run_list = {'init': self.init, 'clean': self.clean, 'restart': self.restart}
        self.steps = ('index', 'mapping', 'sort', 'groups', 'merge', 'duplicates', 'mpileup', 'mpileup2sync')
        self.module_list = {'index': self.modules.index,
                            'mapping': self.modules.mapping,
                            'sort': self.modules.sort,
                            'groups': self.modules.groups,
                            'merge': self.modules.merge,
                            'duplicates': self.modules.duplicates,
                            'mpileup': self.modules.mpileup,
                            'mpileup2sync': self.modules.mpileup2sync,
                            'clean_temp': self.modules.clean_temp}
        self.run_list[self.parser.arguments.command]()

    def init(self):
        self.generate_pipeline_shell_files()
        self.submit_jobs()

    def clean(self, step=0):
        user_check = user_check_clean()
        if not user_check:
            return
        else:
            for i in range(step, len(self.steps)):
                self.module_list[self.steps[i]].clean_module_files(self.data)

    def restart(self):
        if not self.parser.arguments.step:
            for step in self.steps:
                success = self.module_list[step].was_successful(self.data)
                if not success:
                    step_n = self.steps.index(step)
                    break
        else:
            step_n = self.steps.index(self.parser.arguments.step)
        print('Restarting from step: ' + self.steps[step_n])
        self.clean(step=step_n)
        self.generate_pipeline_shell_files(step=step_n)
        self.submit_jobs()

    def get_files_info(self):
        files_info = defaultdict(lambda: defaultdict(lambda: list()))
        for file in self.data.reads_paths:
            dir_path, file_name = os.path.split(file)
            file_name = file_name.split('.')[0]
            fields = file_name.split('_')
            sex = fields[0]
            lane = fields[1]
            mate = fields[2]
            files_info[sex][lane].append(mate)
        return files_info

    def generate_pipeline_shell_files(self, step=0):
        if not step:
            step = 0
        qsub_file = open(self.qsub_file_path, 'w')
        qsub_file.write('cd ' + self.data.directories.output + '\n')
        for i in range(step, len(self.steps)):
            if i == step and i != 0:
                self.module_list[self.steps[step]].generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
            else:
                self.module_list[self.steps[i]].generate_shell_files(self.data, self.parameters, qsub_file)
        if self.parser.arguments.clean_temp:
            self.module_list['clean_temp'].generate_shell_files(self.module_list, qsub_file)

    def submit_jobs(self):
        if self.parser.arguments.run_jobs:
            print('Submitting jobs ...')
            os.system('chmod +x ' + self.qsub_file_path)
            os.system(self.qsub_file_path)
