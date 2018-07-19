import os
from poolsex.data.variables import variables

names = {
    variables.files.qsub: 'run_pipeline.sh',
    variables.files.settings: 'settings.txt'
}


def get_files_info(directories):

    '''
    Files names are defined in this function.
    The function returns a dictionary giving the full path to each file.
    '''

    files = {
        variables.files.qsub: os.path.join(directories[variables.directories.qsub], names[variables.files.qsub]),
        variables.files.settings: os.path.join(directories[variables.directories.root], names[variables.files.settings]),
        variables.files.genome: os.path.join(directories[variables.directories.genome],
                                             [f for f in os.listdir(directories[variables.directories.genome]) if f.endswith('.fasta')][0]),
        variables.files.reads: [os.path.join(directories[variables.directories.reads], f) for
                                f in os.listdir(directories[variables.directories.reads]) if
                                f.endswith('.fastq.gz') or f.endswith('.fasta.gz') or
                                f.endswith('.fastq') or f.endswith('.fasta')]
    }

    return files
