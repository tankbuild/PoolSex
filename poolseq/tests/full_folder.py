import os
from poolseq.data import directory_names as dir_names
from poolseq.tests.init_folder import is_valid_init_folder


def is_valid_full_folder(folder_path):

    is_valid = is_valid_init_folder(folder_path)

    subfolders = [d for d in os.listdir(folder_path)
                  if os.path.isdir(os.path.join(folder_path, d))]

    if dir_names.qsub not in subfolders:
        print('\n** Error: "' + dir_names.qsub + '" folder not found in the input folder')
        is_valid = False
    else:
        qsub_subfolders = [d for d in os.listdir(os.path.join(folder_path, dir_names.qsub))
                           if os.path.isdir(os.path.join(folder_path, dir_names.qsub, d))]
        if dir_names.output not in qsub_subfolders:
            print('\n** Error: "' + dir_names.qsub + '/' + dir_names.output + '" folder not found in the input folder')
            is_valid = False
    if dir_names.shell not in subfolders:
        print('\n** Error: "' + dir_names.shell + '" folder not found in the input folder')
        is_valid = False
    if dir_names.results not in subfolders:
        print('\n** Error: "' + dir_names.results + '" folder not found in the input folder')
        is_valid = False

    return is_valid
