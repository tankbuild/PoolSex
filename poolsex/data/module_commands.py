import os
from poolsex.data.variables import variables


def index(data, parameters, instance_data):
    command = (parameters[variables.parameters.bwa] +
               ' index ' +
               data.files[variables.files.genome] +
               '\n')
    return command


def mapping(data, parameters, instance_data):
    r1_file_path = os.path.join(data.directories[variables.files.reads],
                                instance_data[variables.instance_options.name] +
                                '_' +
                                instance_data[variables.instance_options.mates][0] +
                                '.fastq.gz')
    r2_file_path = os.path.join(data.directories[variables.files.reads],
                                instance_data[variables.instance_options.name] +
                                '_' +
                                instance_data[variables.instance_options.mates][1] +
                                '.fastq.gz')
    command = (parameters[variables.parameters.bwa] + ' mem \\\n' +
               ' -t ' + str(parameters[variables.parameters.threads]) + ' \\\n' +
               data.files[variables.files.genome] + ' \\\n' +
               r1_file_path + ' \\\n' +
               r2_file_path + ' \\\n' +
               '| samtools view -bh -' + ' \\\n' +
               '> ' + instance_data[variables.instance_options.results] + '\n')
    return command


def sort(data, parameters, instance_data):
    command = (parameters[variables.parameters.java] +
               ' -Xmx' + parameters[variables.parameters.java_mem] + ' \\\n' +
               '-jar ' + parameters[variables.parameters.picard] + ' \\\n' +
               'SortSam' + ' \\\n' +
               'I=' + ' '.join(instance_data[variables.instance_options.input]) + ' \\\n' +
               'O=' + instance_data[variables.instance_options.results] + ' \\\n' +
               'SORT_ORDER=coordinate' + '\n')
    return command


def groups(data, parameters, instance_data):
    command = (parameters[variables.parameters.java] +
               ' -Xmx' + parameters[variables.parameters.java_mem] + ' \\\n' +
               '-jar ' + parameters[variables.parameters.picard] + ' \\\n' +
               'AddOrReplaceReadGroups' + ' \\\n' +
               'I=' + ' '.join(instance_data[variables.instance_options.input]) + ' \\\n' +
               'O=' + instance_data[variables.instance_options.results] + ' \\\n' +
               'RGID=' + instance_data[variables.instance_options.sex] + '_' + instance_data[variables.instance_options.lane] + ' \\\n' +
               'RGLB=' + instance_data[variables.instance_options.sex] + ' \\\n' +
               'RGPL=illumina' + ' \\\n' +
               'RGSM=' + instance_data[variables.instance_options.sex] + '_' + instance_data[variables.instance_options.lane] + ' \\\n' +
               'RGPU=' + instance_data[variables.instance_options.sex] + '\n')
    return command


def merge(data, parameters, instance_data):
    if len(instance_data[variables.instance_options.input]) == 1:
        command = 'ln -s ' + instance_data[variables.instance_options.input][0] + ' ' + instance_data[variables.instance_options.results]
    else:
        command = (parameters[variables.parameters.java] +
                   ' -Xmx' + parameters[variables.parameters.java_mem] + ' \\\n' +
                   '-jar ' + parameters[variables.parameters.picard] + ' \\\n' +
                   'MergeSamFiles' + ' \\\n')
        for input_file in instance_data[variables.instance_options.input]:
            command += 'I=' + input_file + ' \\\n'
        command += 'O=' + instance_data[variables.instance_options.results] + ' \n'
    return command


def duplicates(data, parameters, instance_data):
    log_file_path = os.path.join(data.directories[variables.directories.results],
                                 instance_data[variables.instance_options.name] + '_duplicates.txt')
    command = (parameters[variables.parameters.java] +
               ' -Xmx' + parameters[variables.parameters.java_mem] + ' \\\n' +
               '-jar ' + parameters[variables.parameters.picard] + ' \\\n' +
               'MarkDuplicates' + ' \\\n' +
               'I=' + ' '.join(instance_data[variables.instance_options.input]) + ' \\\n' +
               'O=' + instance_data[variables.instance_options.results] + ' \\\n' +
               'M=' + log_file_path + ' \\\n' +
               'TMP_DIR=' + parameters[variables.parameters.java_temp_dir] + ' \\\n' +
               'MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=' + parameters[variables.parameters.max_file_handles] + ' \\\n' +
               'REMOVE_DUPLICATES=true' + '\n')
    return command


def mpileup(data, parameters, instance_data):
    command = (parameters[variables.parameters.samtools] +
               ' mpileup -B -Q 0 \\\n' +
               '-f ' + data.files[variables.files.genome] + ' \\\n' +
               '-o ' + instance_data[variables.instance_options.results] + ' \\\n' +
               ' '.join(instance_data[variables.instance_options.input]) + '\n')
    return command


def mpileup2sync(data, parameters, instance_data):
    command = (parameters[variables.parameters.java] +
               ' -Xmx' + parameters[variables.parameters.java_mem] + ' \\\n' +
               '-jar ' + '/usr/local/bioinfo/src/PoPoolation2/popoolation2_1201/' + parameters[variables.parameters.popoolation] + ' \\\n' +
               '--input ' + ' '.join(instance_data[variables.instance_options.input]) + ' \\\n' +
               '--output ' + instance_data[variables.instance_options.results] + ' \\\n' +
               '--fastq-type sanger' + ' \\\n' +
               '--min-qual 20' + ' \\\n' +
               '--threads ' + str(parameters[variables.parameters.threads]) + '\n')
    return command


def clean_temp(data, parameters, instance_data):
    command = ('rm -rf ' + ' \\\n'.join(instance_data[variables.instance_options.input]) + '\n')
    return command
