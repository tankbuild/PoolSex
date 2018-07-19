
class Directories:
    def __init__(self):
        self.root = 'root'
        self.genome = 'genome'
        self.qsub = 'qsub'
        self.output = 'output'
        self.reads = 'reads'
        self.results = 'results'
        self.poolseq = 'poolseq'
        self.shell = 'shell'


class Files:
    def __init__(self):
        self.qsub = 'qsub'
        self.settings = 'settings'
        self.reads = 'reads'
        self.genome = 'genome'


class Parameters:
    def __init__(self):
        self.scheduler = 'scheduler'
        self.threads = 'threads'
        self.mem = 'mem'
        self.h_vmem = 'h_vmem'
        self.bwa = 'bwa'
        self.samtools = 'samtools'
        self.popoolation = 'popoolation'
        self.picard = 'picard'
        self.java = 'java'
        self.java_mem = 'java_mem'
        self.java_temp_dir = 'java_temp_dir'
        self.java_temp_dir_name = 'java_temp_dir_name'
        self.max_file_handles = 'max_file_handles'


class Modules:
    def __init__(self):
        self.index = 'index'
        self.mapping = 'mapping'
        self.sort = 'sort'
        self.groups = 'groups'
        self.merge = 'merge'
        self.duplicates = 'duplicates'
        self.mpileup = 'mpileup'
        self.mpileup2sync = 'mpileup2sync'
        self.clean_temp = 'clean_temp'


class ModulesOptions:
    def __init__(self):
        self.prefix = 'prefix',
        self.clean_temp = 'clean_temp',
        self.results_format = 'results_format',
        self.sex = 'sex',
        self.lane = 'lane',
        self.mate = 'mate',
        self.pairwise = 'pairwise',
        self.options = 'options'
        self.dependencies = 'dependencies'
        self.command = 'command'


class InstanceOptions:
    def __init__(self):
        self.name = 'name'
        self.shell = 'shell'
        self.shell_name = 'shell_name'
        self.output = 'output'
        self.error = 'error'
        self.results = 'results'
        self.input = 'input'
        self.dependencies = 'dependencies'
        self.sex = 'sex'
        self.lane = 'lane'
        self.mates = 'mates'


class SubmitOptions:
    def __init__(self):
        self.name = 'name'
        self.threads = 'threads'
        self.mem = 'mem'
        self.h_vmem = 'h_vmem'
        self.output = 'output'
        self.error = 'error'


class Schedulers:
    def __init__(self):
        self.sge = 'sge'
        self.slurm = 'slurm'


class SchedulersOptions:
    def __init__(self):
        self.parameters = 'parameters'
        self.parameter_prefix = 'parameter_prefix'
        self.modules = 'modules'
        self.job_id_regex = 'job_id_regex'
        self.submit_command = 'submit_command'
        self.hold_command = 'hold_command'


class Commands:
    def __init__(self):
        self.init = 'init'
        self.run = 'run'
        self.restart = 'restart'
        self.clean = 'clean'


class Variables:
    def __init__(self):
        self.directories = Directories()
        self.files = Files()
        self.parameters = Parameters()
        self.modules = Modules()
        self.modules_options = ModulesOptions()
        self.instance_options = InstanceOptions()
        self.submit_options = SubmitOptions()
        self.schedulers = Schedulers()
        self.schedulers_options = SchedulersOptions()
        self.commands = Commands()


variables = Variables()
