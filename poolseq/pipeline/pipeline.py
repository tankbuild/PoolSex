import os
from collections import defaultdict
from poolseq.data import Data
from poolseq.parameters import Parameters
from poolseq.parser import Parser
from poolseq.modules import Modules


class Pipeline():

    def __init__(self, arguments):
        self.parser = Parser(arguments)
        self.data = Data(self.parser.arguments.input_folder)
        self.parameters = Parameters(self.data)
        self.files_info = self.get_files_info(self.data)
        self.modules = Modules(self.data, self.files_info)
        self.run_list = {'init': self.init, 'clean': self.clean, 'restart': self.restart}
        self.steps = ('index', 'map', 'sort', 'groups', 'merge', 'duplicates', 'mpileup', 'sync')
        self.run_list[self.parser.arguments.command]()

    def init(self):
        self.generate_pipeline_shell_file(self.data, 5)

    def clean(self):
        if not self.parser.arguments.step:
            step = 0
        else:
            step = self.steps.index(self.parser.arguments.step)
        if step < 1:
            files = [os.path.join(self.data.directories.genomes, f) for
                     f in os.listdir(self.data.directories.genomes)]
            for file in files:
                if file != self.data.genome_path:
                    os.remove(file)
        if step < 2:
            self.clean_module_files(self.modules.mapping)
        if step < 3:
            self.clean_module_files(self.modules.sort)
        if step < 4:
            self.clean_module_files(self.modules.groups)
        if step < 5:
            self.clean_module_files(self.modules.merge)
        if step < 6:
            self.clean_module_files(self.modules.duplicates)
        if step < 7:
            self.clean_module_files(self.modules.mpileup)
        self.clean_module_files(self.modules.mpileup2sync)

    def restart(self):
        pass
        # if not self.parser.arguments.step:
        #     pass
        # else:
        #     step_n = self.steps.index(self.parser.arguments.step)
        # self.processing.generate_shell_files(self.data, self.parameters, step=step_n)

    def get_files_info(self, data):
        files_info = defaultdict(lambda: defaultdict(lambda: list()))
        for file in data.reads_paths:
            dir_path, file_name = os.path.split(file)
            file_name = file_name.split('.')[0]
            fields = file_name.split('_')
            sex = fields[0]
            lane = fields[1]
            mate = fields[2]
            files_info[sex][lane].append(mate)
        return files_info

    def clean_module_files(self, module):
        for instance in module.instances.values():
            if os.path.isfile(instance['output']):
                os.remove(instance['output'])

    def generate_pipeline_shell_file(self, data, step):
        if not step:
            step = 0
        qsub_file_path = os.path.join(data.directories.qsub, 'run_pipeline.sh')
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
