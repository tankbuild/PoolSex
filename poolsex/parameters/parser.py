import argparse
import sys
import os
from poolsex.parameters.test_folders import is_valid_full_folder, is_valid_init_folder


class Parser():

    def __init__(self, arguments):
        self.parser = argparse.ArgumentParser(
            description='Analysis of pooled sequencing data for sex determination',
            usage='''python3 poolsex.py <command> [options]

Commands: init     Create a full input directory from a minimal input directory
          run      Generate shell scripts and run the pipeline from an input directory
          clean    Cleanup all files generated by this pipeline in a directory
          restart  Restart the pipeline from the last completed step
\n\n''')
        self.parser.add_argument('command', help='Command to run')
        self.parser.add_argument('--input-folder', '-i',
                                 help='Path to a poolsex input folder')
        self.parser.add_argument('--step', '-s',
                                 help='Step to restart from',
                                 default=None)
        self.parser.add_argument('--dry-run', '-d', action='store_true',
                                 help='If --dry-run is specified, the pipeline will generate the shell files without running the jobs',
                                 default=False)
        self.parser.add_argument('--clean-temp', '-c', action='store_true',
                                 help='If --clean-temp is specified, results files from intermediate steps will be deleted after completion of the pipeline.',
                                 default=False)
        self.arguments = self.parser.parse_args(sys.argv[1:2])
        if not self.arguments.command:
            print('\n** Error: no command specified\n')
            self.parser.print_usage()
            print()
            exit(1)
        if not hasattr(self, self.arguments.command):
            print('\n** Error: invalid command "' + self.arguments.command + '"' + '\n')
            self.parser.print_usage()
            print()
            exit(1)
        getattr(self, self.arguments.command)()

    def init(self):
        '''
        Initiate analysis from a minimal input folder with given structure.
        '''
        parser = argparse.ArgumentParser(
            description='Create a full input directory from a minimal input directory',
            usage='''python3 poolsex.py init -i input_folder

Options: -i  --input-folder  Path to a poolsex minimal input folder with the following structure:
          .
          ├─── genome
          |     ├────── <species_name>_genome.<fasta/fa/fna>
          └─── reads
                ├────── <sex>_<lane>_<mate_number>.<fasta/fastq><.gz>
                ├────── <sex>_<lane>_<mate_number>.<fasta/fastq><.gz>
                └────── ...
''')
        parser.add_argument('--input-folder', '-i',
                            help='Path to a poolsex input folder')
        parser.parse_args(sys.argv[2:])
        self.arguments = self.parser.parse_args(sys.argv[1:])  # This is done here to separate "-h" for each parser
        self.test_input_folder(parser, full=False)

    def run(self):
        '''
        Initiate analysis from a minimal input folder with given structure.
        '''
        parser = argparse.ArgumentParser(
            description='Generate shell scripts and run the pipeline from an input directory',
            usage='''python3 poolsex.py run -i input_folder [--dry-run]

Options: -i  --input-folder  Path to a poolsex input folder
         -d  --dry-run       If --dry-run is specified, the pipeline will generate the shell files without running the jobs
         -c  --clean-temp    If --clean-temp is specified, results files from intermediate steps will be deleted after completion of the pipeline.
''')
        parser.add_argument('--input-folder', '-i',
                            help='Path to a poolsex input folder')
        parser.add_argument('--dry-run', '-d', action='store_true',
                            help='If --dry-run is specified, the pipeline will generate the shell files without running the jobs',
                            default=False)
        parser.add_argument('--clean-temp', '-c', action='store_true',
                            help='If --clean-temp is specified, results files from intermediate steps will be deleted after completion of the pipeline.',
                            default=False)
        parser.parse_args(sys.argv[2:])
        self.arguments = self.parser.parse_args(sys.argv[1:])  # This is done here to separate "-h" for each parser
        self.test_input_folder(parser)

    def clean(self):
        '''
        Clean an analysis directory.
        '''
        parser = argparse.ArgumentParser(
            description='Cleanup all files generated by this pipeline in a directory',
            usage='''python3 poolsex.py clean -i input_folder

Options: -i  --input-folder  Path to a poolsex input folder
''')
        parser.add_argument('--input-folder', '-i',
                            help='Path to a poolsex input folder')
        parser.parse_args(sys.argv[2:])
        self.arguments = self.parser.parse_args(sys.argv[1:])  # This is done here to separate "-h" for each parser
        self.test_input_folder(parser)

    def restart(self):
        '''
        Restart the analysis from either the last completed step or from a given step
        '''
        parser = argparse.ArgumentParser(
            description='Restart the pipeline from the last completed step',
            usage='''python3 poolsex.py restart -i input_folder [-s step --run-jobs]

Options: -i  --input-folder  Path to a poolsex input folder
         -s  --step          Step to restart from (index, mapping, sort, groups, merge, duplicates, mpileup, mpileup2sync)
         -d  --dry-run       If --dry-run is specified, the pipeline will generate the shell files without running the jobs
         -c  --clean-temp    If --clean-temp is specified, results files from intermediate steps will be deleted after completion of the pipeline.
''')
        parser.add_argument('--input-folder', '-i',
                            help='Path to a poolsex input folder')
        parser.add_argument('--step', '-s',
                            help='Step to restart from')
        parser.add_argument('--dry-run', '-d', action='store_true',
                            help='If --dry-run is specified, the pipeline will generate the shell files without running the jobs.',
                            default=False)
        parser.add_argument('--clean-temp', '-c', action='store_true',
                            help='If --clean-temp is specified, results files from intermediate steps will be deleted after completion of the pipeline.',
                            default=False)
        parser.parse_args(sys.argv[2:])
        self.arguments = self.parser.parse_args(sys.argv[1:])  # This is done here to separate "-h" for each parser
        self.test_input_folder(parser)

    def test_input_folder(self, parser, full=True):
        '''
        Encapsulate tests for a valid input folder
        '''
        if not self.arguments.input_folder:
            print('\n** Error: no input folder specified\n')
            parser.print_usage()
            print()
            exit(1)
        elif not os.path.isdir(self.arguments.input_folder):
            print('\n** Error: input folder "' + self.arguments.input_folder + '"' + ' does not exist' + '\n')
            parser.print_usage()
            print()
            exit(1)
        else:
            if full:
                if not is_valid_full_folder(self.arguments.input_folder):
                    print('\n** Error: input folder "' + self.arguments.input_folder + '"' + ' is not a valid input folder' + '\n')
                    parser.print_usage()
                    print()
                    exit(1)
            else:
                if not is_valid_init_folder(self.arguments.input_folder):
                    print('\n** Error: input folder "' + self.arguments.input_folder + '"' + ' is not a valid input folder' + '\n')
                    parser.print_usage()
                    print()
                    exit(1)
