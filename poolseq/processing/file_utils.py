import os


def wa_open(file_path):
    if os.path.isfile(file_path):
        file = open(file_path, 'a')
    else:
        file = open(file_path, 'w')
    return file
