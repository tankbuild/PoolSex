from directory_structure import *
from settings import *
import genotoul


files = [f for f in os.listdir(output_dir) if f.endswith('_sorted.bam')]

qsub_p = os.path.join(qsub_dir, 'picard_merge.sh')
qsub_f = open(qsub_p, 'w')

groups = defaultdict(list)

for f in files:
    sex = f.split('_')[0]
    groups[sex].append(f)

for sex, input_files in groups.items():

    output_file = os.path.join(output_dir, sex + '.bam')

    shell_p = os.path.join(shell_dir, 'picard_merge_' + sex + '.sh')
    shell_f = open(shell_p, 'w')

    shell_f.write('#!/bin/sh\n')
    shell_f.write('#$ -N picard_merge\n')
    shell_f.write('#$ -l mem=' + mem + '\n')
    shell_f.write('#$ -l h_vmem=' + h_vmem + '\n\n')
    shell_f.write('module load bioinfo/Java8\n\n')
    shell_f.write('java -Xmx' + java_memory + ' -jar ' +
                  '/usr/local/bioinfo/src/picard-tools/current/picard.jar MergeSamFiles ')
    for i_file in input_files:
        shell_f.write('I=' + os.path.join(output_dir, i_file) + ' ')
    shell_f.write('O=' + output_file)
    shell_f.close()

    qsub_f.write('qsub ' + shell_p + '\n')
