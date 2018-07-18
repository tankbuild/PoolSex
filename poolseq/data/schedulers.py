from poolseq.data.variables import variables

schedulers = {
    # SGE environment
    variables.schedulers.sge: {variables.schedulers_options.parameter_prefix: '#$ ',
                               variables.schedulers_options.parameters: {variables.submit_options.name: '-N ',
                                                                         variables.submit_options.threads: '-pe parallel_smp ',
                                                                         variables.submit_options.mem: '-l mem=',
                                                                         variables.submit_options.h_vmem: '-l h_vmem=',
                                                                         variables.submit_options.output: '-o ',
                                                                         variables.submit_options.error: '-e '},
                               variables.schedulers_options.modules: {variables.modules.index: [],
                                                                      variables.modules.mapping: [],
                                                                      variables.modules.sort: ['bioinfo/Java8'],
                                                                      variables.modules.groups: ['bioinfo/Java8'],
                                                                      variables.modules.merge: ['bioinfo/Java8'],
                                                                      variables.modules.duplicates: ['bioinfo/Java8'],
                                                                      variables.modules.mpileup: [],
                                                                      variables.modules.mpileup2sync: ['bioinfo/Java8'],
                                                                      variables.modules.clean_temp: []},
                               variables.schedulers_options.job_id_regex: r'Your job (\d+) .+$',
                               variables.schedulers_options.submit_command: 'qsub',
                               variables.schedulers_options.hold_command: '-hold_jid '},
    # SLURM environment
    variables.schedulers.slurm: {variables.schedulers_options.parameter_prefix: '#SBATCH ',
                                 variables.schedulers_options.parameters: {variables.submit_options.name: '-J ',
                                                                           variables.submit_options.threads: '--cpus-per-task=',
                                                                           variables.submit_options.mem: '--mem=',
                                                                           variables.submit_options.h_vmem: None,
                                                                           variables.submit_options.output: '-o ',
                                                                           variables.submit_options.error: '-e '},
                                 variables.schedulers_options.modules: {variables.modules.index: ['bioinfo/bwa-0.7.17'],
                                                                        variables.modules.mapping: ['bioinfo/bwa-0.7.17', 'bioinfo/samtools-1.8'],
                                                                        variables.modules.sort: ['bioinfo/picard-2.18.2'],
                                                                        variables.modules.groups: ['bioinfo/picard-2.18.2'],
                                                                        variables.modules.merge: ['bioinfo/picard-2.18.2'],
                                                                        variables.modules.duplicates: ['bioinfo/picard-2.18.2'],
                                                                        variables.modules.mpileup: ['bioinfo/samtools-1.8'],
                                                                        variables.modules.mpileup2sync: ['bioinfo/popoolation2_1201'],
                                                                        variables.modules.clean_temp: []},
                                 variables.schedulers_options.job_id_regex: r'Submitted batch job (\d+)$',
                                 variables.schedulers_options.submit_command: 'sbatch',
                                 variables.schedulers_options.hold_command: '--dependency=afterany:'}
}


def get_schedulers_info():

    '''
    All the information about schedulers is defined in this function:
    - parameter_prefix: prefix before scheduler parameters in shell file
    - parameters: scheduler parameters names (None if the parameter doesn't exist)
    - modules: list of modules to load for each part of the pipeline
    - job_id_regex: regular expression to recover job id from submission message
    - submit_command: base command used to submit a job
    - hold_command: base command used to define dependencies
    '''

    return schedulers
