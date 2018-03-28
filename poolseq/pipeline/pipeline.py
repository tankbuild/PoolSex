import os
from poolseq.data import Data
from poolseq.processing import Processing
from poolseq.parameters import Parameters
from poolseq.parser import Parser


class Pipeline():

    def __init__(self, arguments):
        self.parser = Parser(arguments)
        self.data = Data(self.parser.arguments.input_folder)
        self.parameters = Parameters(self.data)
        self.processing = Processing(self.data)
        self.run_list = {'init': self.init, 'clean': self.clean, 'restart': self.restart}
        self.steps = ('index', 'map', 'sort', 'groups', 'merge', 'duplicates', 'mpileup', 'sync')
        self.run_list[self.parser.arguments.command]()

    def init(self):
        self.processing.generate_shell_files(self.data, self.parameters)

    def clean(self):
        if not self.parser.arguments.step:
            step = 0
        else:
            step = self.steps.index(self.parser.arguments.step)
        print(step)
        if step < 1:
            files = [os.path.join(self.data.directories.genomes, f) for
                     f in os.listdir(self.data.directories.genomes)]
            for file in files:
                if file != self.data.genome_path:
                    os.remove(file)
        if step < 2:
            print(self.processing.bwa.mapping.output_file_path)
            for file in self.processing.bwa.mapping.output_file_path:
                os.remove(file)
        if step < 3:
            for file in self.processing.picard.sort.output_file_path:
                os.remove(file)
        if step < 4:
            for file in self.processing.picard.add_read_groups.output_file_path:
                os.remove(file)
        if step < 5:
            for file in self.processing.picard.merge.output_file_path:
                os.remove(file)
        if step < 6:
            for file in self.processing.picard.mark_duplicates.output_file_path:
                os.remove(file)
        if step < 7:
            for file in self.processing.samtools.mpileup.output_file_path:
                os.remove(file)
        for file in self.processing.samtools.mpileup.output_file_path:
            os.remove(file)

    def restart(self):
        if not self.parser.arguments.step:
            pass
        else:
            step_n = self.steps.index(self.parser.arguments.step)
        self.processing.generate_shell_files(self.data, self.parameters, step=step_n)
