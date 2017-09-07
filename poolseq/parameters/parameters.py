

class Parameters():

    def __init__(self, structure):
        self.threads = None
        self.java_mem = None
        self.mem = None
        self.h_vmem = None
        self.bwa = None
        self.gatk = None
        self.picard = None
        self.java = None
        self.load(structure)

    def load(self, structure):
        settings_file = open(structure.poolseq.settings())
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
