import os
from poolseq.data import directory_names as dir_names


def is_valid_init_folder(folder_path):

    is_valid = True
    subfolders = [d for d in os.listdir(folder_path)
                  if os.path.isdir(os.path.join(folder_path, d))]

    if dir_names.genome in subfolders:
        temp = [f for f in os.listdir(os.path.join(folder_path, dir_names.genome))
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

    if dir_names.reads in subfolders:
        temp = [f for f in os.listdir(os.path.join(folder_path, dir_names.reads)) if
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
