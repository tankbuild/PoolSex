import os


class Parameters():

    def __init__(self, data):
        self.threads = '16'
        self.mem = '21G'
        self.h_vmem = '25G'
        self.bwa = 'bwa'
        self.crisp = 'crisp'
        self.samtools = 'samtools'
        self.popoolation = 'mpileup2sync.jar'
        self.gatk = 'GenomeAnalysisTK.jar'
        self.picard = 'picard.jar'
        self.java = 'java'
        self.java_mem = '20G'
        self.java_temp_dir = os.path.join(data.directories.results, 'tmp')
        self.max_open_temp_files = '800'
        self.max_file_handles = '1000'
        self.number_of_individuals = '1'
        self.min_number_of_reads = '4'
        self.load(data)

    def load(self, data):
        settings_file = open(data.files.settings)
        settings = {name: value for
                    name, value in (line[:-1].split('=') for
                                    line in settings_file if
                                    line and not line.startswith('#'))}
        for name, value in settings.items():
            try:
                setattr(self, name, value)
            except KeyError:
                print('** Error: parameter "' + name + '" does not exist.')
            except ValueError:
                print('** Error: could not affect value "' + str(value) +
                      '" to parameter "' + name + '".')
