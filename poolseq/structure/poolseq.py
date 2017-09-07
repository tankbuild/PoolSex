import os


class Poolseq():

    def __init__(self, directories):
        self.directories = directories

    def settings(self):
        return os.path.join(self.directories.poolseq, 'settings.txt')
