from poolseq.data.variables import variables

parameters = {
    variables.parameters.scheduler: 'slurm',
    variables.parameters.threads: '16',
    variables.parameters.mem: '42G',
    variables.parameters.h_vmem: '45G',
    variables.parameters.bwa: 'bwa',
    variables.parameters.samtools: 'samtools',
    variables.parameters.popoolation: 'mpileup2sync.jar',
    variables.parameters.picard: '$PICARD',
    variables.parameters.java: 'java',
    variables.parameters.java_mem: '40G',
    variables.parameters.java_temp_dir_name: 'tmp',
    variables.parameters.java_temp_dir: None,
    variables.parameters.max_file_handles: '1000',
}


def get_parameters_info():

    '''
    Default parameters values are defined in this function.
    The function returns a dictionary giving the default value of each parameter.
    '''

    return parameters
