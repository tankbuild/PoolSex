from poolseq.structure import Directories, Data, Output, Qsub, Shell, Poolseq


class Structure():

    def __init__(self):
        self.directories = Directories()
        self.data = Data(self.directories)
        self.output = Output(self.directories)
        self.qsub = Qsub(self.directories)
        self.shell = Shell(self.directories)
        self.poolseq = Poolseq(self.directories)
