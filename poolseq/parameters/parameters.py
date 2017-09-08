import os


class Parameters():

    def __init__(self, data):
        self.threads = '16'
        self.mem = '21G'
        self.h_vmem = '25G'
        self.bwa = 'bwa'
        self.gatk = 'GenomeAnalysisTK.jar'
        self.picard = 'picard.jar'
        self.java = 'java'
        self.java_mem = '20G'
        self.java_temp_dir = os.path.join(data.directories.output, 'tmp')
        self.load(data)

    def load(self, data):
        settings_file_path = os.path.join(data.directories.root, 'settings.txt')
        settings_file = open(settings_file_path)
        settings = {name: value for
                    name, value in (line[:-1].split('=') for
                                    line in settings_file)}
        for name, value in settings.items():
            try:
                setattr(self, name, value)
            except KeyError:
                print('** Error: parameter "' + name + '" does not exist.')
            except ValueError:
                print('** Error: could not affect value "' + str(value) +
                      '" to parameter "' + name + '".')
