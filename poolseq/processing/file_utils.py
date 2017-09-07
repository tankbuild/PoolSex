import os
import itertools


def get_info(reads_file_path):
    dir_path, file_path = os.path.split(reads_file_path)
    file_path = file_path.replace('.fastq.gz', '')
    fields = file_path.split('_')
    info = {}
    info['species'] = fields[0] + '_' + fields[1]
    info['sex'] = fields[2]
    info['lane'] = fields[3]
    info['mate'] = fields[4]
    return info


def find_pairs(reads_files_paths):
    info = {path: get_info(path) for path in reads_files_paths}
    pairs = []
    for file_1, file_2 in itertools.combinations(info.keys(), 2):
        if (info[file_1]['sex'] == info[file_2]['sex'] and
                info[file_1]['lane'] == info[file_2]['lane'] and
                info[file_1]['mate'] != info[file_2]['mate']):
            pairs.append((file_1, file_2))
    return pairs
