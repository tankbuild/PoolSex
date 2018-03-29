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
                            'mpileup2sync': self.modules.mpileup2sync}
        self.run_list[self.parser.arguments.command]()

    def init(self):
        self.generate_pipeline_shell_files()

    def clean(self):
        user_check = user_check_clean()
        if not user_check:
            return
        if not self.parser.arguments.step:
            step = 0
        else:
            step = self.steps.index(self.parser.arguments.step)
        for i in range(step, len(self.steps)):
            self.module_list[self.steps[i]].clean_module_files(self.data)

    def restart(self):
        if not self.parser.arguments.step:
            pass
            # output_files = [os.path.join(self.output_folder, f) for
            #                 f in os.listdir(self.output_folder) if
            #                 instance in f and f.split('.')[1][0] == 'o']
            # for output_file in output_files:
            #     pass
        else:
            step_n = self.steps.index(self.parser.arguments.step)
        self.clean()
        self.generate_pipeline_shell_files(step=step_n)

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
        qsub_file_path = os.path.join(self.data.directories.qsub, 'run_pipeline.sh')
        qsub_file = open(qsub_file_path, 'w')
        if step < 1:
            self.modules.index.generate_shell_files(self.data, self.parameters, qsub_file)
        if step < 2:
            if step < 1:
                self.modules.mapping.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.mapping.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
        if step < 3:
            if step < 2:
                self.modules.sort.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.sort.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
        if step < 4:
            if step < 3:
                self.modules.groups.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.groups.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
        if step < 5:
            if step < 4:
                self.modules.merge.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.merge.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
        if step < 6:
            if step < 5:
                self.modules.duplicates.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.duplicates.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
        if step < 7:
            if step < 6:
                self.modules.mpileup.generate_shell_files(self.data, self.parameters, qsub_file)
            else:
                self.modules.mpileup.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
            self.modules.mpileup2sync.generate_shell_files(self.data, self.parameters, qsub_file)
        else:
            self.modules.mpileup2sync.generate_shell_files(self.data, self.parameters, qsub_file, hold=False)
