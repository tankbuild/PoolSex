import os
from poolsex.data import variables


def generate_directories(data):
    if not os.path.isdir(data.directories[variables.directories.qsub]):
        os.mkdir(data.directories[variables.directories.qsub])
    if not os.path.isdir(data.directories[variables.directories.output]):
        os.mkdir(data.directories[variables.directories.output])
    if not os.path.isdir(data.directories[variables.directories.results]):
        os.mkdir(data.directories[variables.directories.results])
    if not os.path.isdir(data.directories[variables.directories.shell]):
        os.mkdir(data.directories[variables.directories.shell])


def generate_settings_file(data, parameters):
    settings_file = open(data.files[variables.files.settings], 'w')
    settings_file.write('# Scheduler' + '\n')
    settings_file.write('scheduler=' + data.parameters[variables.parameters.scheduler] + '\n')
    settings_file.write('# Resources' + '\n')
    settings_file.write('threads=' + data.parameters[variables.parameters.threads] + '\n')
    settings_file.write('java_mem=' + data.parameters[variables.parameters.java_mem] + '\n')
    settings_file.write('mem=' + data.parameters[variables.parameters.mem] + '\n')
    settings_file.write('h_vmem=' + data.parameters[variables.parameters.h_vmem] + '\n')
    settings_file.write('# Path to executables' + '\n')
    settings_file.write('java=' + data.parameters[variables.parameters.java] + '\n')
    settings_file.write('bwa=' + data.parameters[variables.parameters.bwa] + '\n')
    settings_file.write('samtools=' + data.parameters[variables.parameters.samtools] + '\n')
    settings_file.write('picard=' + data.parameters[variables.parameters.picard] + '\n')
    settings_file.write('popoolation=' + data.parameters[variables.parameters.popoolation] + '\n')
    settings_file.write('# Java option for Picard' + '\n')
    settings_file.write('max_file_handles=' + data.parameters[variables.parameters.max_file_handles] + '\n')
