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
        self.run_list[self.parser.arguments.command]()

    def init(self):
        self.processing.generate_shell_files(self.data, self.parameters)

    def clean(self):
        output_files = (os.path.join(self.data.directories.output, f) for
                        f in os.listdir(self.data.directories.output) if
                        os.path.isfile(os.path.join(self.data.directories.output, f)) or
                        os.path.isdir(os.path.join(self.data.directories.output, f)))
        shell_files = (os.path.join(self.data.directories.shell, f) for
                       f in os.listdir(self.data.directories.shell) if
                       os.path.isfile(os.path.join(self.data.directories.shell, f)))
        qsub_files = (os.path.join(self.data.directories.qsub, f) for
                      f in os.listdir(self.data.directories.qsub) if
                      os.path.isfile(os.path.join(self.data.directories.qsub, f)))
        for file in output_files:
            os.remove(file)
        for file in shell_files:
            os.remove(file)
        for file in qsub_files:
            os.remove(file)

    def restart(self):
        pass
