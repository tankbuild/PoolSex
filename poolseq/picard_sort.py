from directory_structure import *
import os

qsub_file = open(PICARD_SORT_SH, 'w')

for file in files:

    input_file = os.path.join(output_dir, file)
    output_file = os.path.join(output_dir, file.replace('.bam', '_sorted.bam'))

    shell_p = os.path.join(shell_dir, 'picard_sort_' + file.replace('.bam', '.sh'))
    shell_f = open(shell_p, 'w')

    shell_f.write('#!/bin/sh\n')
    shell_f.write('#$ -N picard_sort\n')
    shell_f.write('#$ -l mem=' + mem + '\n')
    shell_f.write('#$ -l h_vmem=' + h_vmem + '\n\n')
    shell_f.write('module load bioinfo/Java8\n\n')
    shell_f.write('java -Xmx' + java_memory + ' -jar ' +
                  '/usr/local/bioinfo/src/picard-tools/current/picard.jar SortSam ' +
                  'I=' + input_file + ' ' +
                  'O=' + output_file + ' ' +
                  'SORT_ORDER=coordinate')
    shell_f.close()

    qsub_f.write('qsub ' + shell_p + '\n')
