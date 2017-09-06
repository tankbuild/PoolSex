import os
import itertools


def reads_file_info(reads_file_path):

    dir_path, file_path = os.path.split(reads_file_path)
    file_path = file_path.replace('.fastq.gz', '')
    fields = file_path.split('_')

    infos = {}
    infos['species'] = fields[0] + '_' + fields[1]
    infos['sex'] = fields[2]
    infos['lane'] = fields[3]
    infos['mate'] = fields[4]

    return infos


def find_pairs(reads_files_paths):

    infos = {path: reads_file_info(path) for path in reads_files_paths}

    pairs = []

    for file_1, file_2 in itertools.combinations(infos.keys(), 2):
        if (infos[file_1]['sex'] == infos[file_2]['sex'] and
                infos[file_1]['lane'] == infos[file_2]['lane'] and
                infos[file_1]['mate'] != infos[file_2]['mate']):
            pairs.append((file_1, file_2))

    return pairs
