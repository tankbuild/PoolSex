import os
from poolsex.data import directories_names, files_names, variables


def is_valid_init_folder(folder_path):

    is_valid = True
    subfolders = [d for d in os.listdir(folder_path)
                  if os.path.isdir(os.path.join(folder_path, d))]

    if directories_names[variables.directories.genome] in subfolders:
        temp = [f for f in os.listdir(os.path.join(folder_path, directories_names[variables.directories.genome]))
                if f.endswith('.fasta') or f.endswith('.fa') or f.endswith('.fna')]
        if len(temp) == 0:
            print('\n** Error: genome file not found')
            is_valid = False
        elif len(temp) > 1:
            print('\n** Error: expected one genome file, but found ' + str(len(temp)) + ' ("' + '", "'.join(temp) + '").')
            is_valid = False
    else:
        print('\n** Error: \"genome\" directory is missing.')
        is_valid = False

    if directories_names[variables.directories.reads] in subfolders:
        temp = [f for f in os.listdir(os.path.join(folder_path, directories_names[variables.directories.reads])) if
                f.endswith('.fasta') or f.endswith('.fastq') or
                f.endswith('.fasta.gz') or f.endswith('.fastq.gz')]
        if len(temp) < 2:
            print('\n** Error: expected at least two reads files (one per sex) but found ' + str(len(temp)) + '')
            is_valid = False
        elif len(temp) % 2 != 0:
            print('\n** Error: expected an even number of reads files, but found ' + str(len(temp)) + '')
            is_valid = False
        else:
            for file in temp:
                fields = file.split('_')
                if len(fields) != 3:
                    print('\n** Error: reads file "' + file + '" has incorrect name. Expected <sex>_<lane>_<mate_number>.<fasta/fastq><.gz>')
                    is_valid = False
    else:
        print('\n** Error: \"reads\" directory is missing.')
        is_valid = False

    return is_valid


def is_valid_full_folder(folder_path):

    is_valid = is_valid_init_folder(folder_path)

    subfolders = [d for d in os.listdir(folder_path)
                  if os.path.isdir(os.path.join(folder_path, d))]

    if directories_names[variables.directories.qsub] not in subfolders:
        print('\n** Error: "' + directories_names[variables.directories.qsub] + '" folder not found in the input folder')
        is_valid = False
    else:
        qsub_subfolders = [d for d in os.listdir(os.path.join(folder_path, directories_names[variables.directories.qsub]))
                           if os.path.isdir(os.path.join(folder_path, directories_names[variables.directories.qsub], d))]
        if directories_names[variables.directories.output] not in qsub_subfolders:
            print('\n** Error: "' + directories_names[variables.directories.qsub] + '/' + directories_names[variables.directories.output] + '" folder not found in the input folder')
            is_valid = False
    if directories_names[variables.directories.shell] not in subfolders:
        print('\n** Error: "' + directories_names[variables.directories.shell] + '" folder not found in the input folder')
        is_valid = False
    if directories_names[variables.directories.results] not in subfolders:
        print('\n** Error: "' + directories_names[variables.directories.results] + '" folder not found in the input folder')
        is_valid = False

    if not os.path.isfile(os.path.join(folder_path, files_names[variables.files.settings])):
        print('\n** Error: settings file not found')
        is_valid = False

    return is_valid
