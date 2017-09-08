from poolseq.data import Data
from poolseq.processing import Processing
from poolseq.parameters import Parameters


class Pipeline():

    def __init__(self, root_dir):
        self.data = Data(root_dir)
        self.parameters = Parameters(self.data)
        self.processing = Processing(self.data)

    def run(self):
        self.processing.generate_shell_files(self.data, self.parameters)
