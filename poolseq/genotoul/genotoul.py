

def print_header(shell_file,
                 name=None,
                 threads=None,
                 mem=None,
                 h_vmem=None):

    shell_file.write('#!/bin/sh' + '\n')
    if name:
        shell_file.write('#$ -N ' + str(name) + '\n')
    if threads:
        shell_file.write('#$ -pe parallel_smp ' + str(threads) + '\n')
    if mem:
        shell_file.write('#$ -l mem=' + str(mem) + '\n')
    if h_vmem:
        shell_file.write('#$ -l mem=' + str(h_vmem) + '\n')
    shell_file.write('\n')


def print_java_module(shell_file):

    shell_file.write('module load bioinfo/Java8' + '\n\n')
