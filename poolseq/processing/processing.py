import os
from collections import defaultdict
from poolseq.processing.bwa import Bwa
from poolseq.processing.picard import Picard
from poolseq.processing.gatk import Gatk


class Processing():

    def __init__(self, data):
        self.bwa = Bwa(data)
        self.picard = Picard(data)
        self.gatk = Gatk(data)
        self.files_info = self.get_files_info(data)

    def generate_shell_files(self, data, parameters):
        self.reset_qsub_files(data)
        self.bwa.index.generate_files(data, parameters)
        self.gatk.index.generate_shell_files(data, parameters)
        files_info = self.files_info
        for sex, lanes in files_info.items():
            self.picard.merge.generate_shell_files(data,
                                                   parameters,
                                                   sex,
                                                   lanes)
            self.picard.validate_sam_file.generate_shell_files(data,
                                                               parameters,
                                                               sex)
            self.picard.mark_duplicates.generate_shell_files(data,
                                                             parameters,
                                                             sex)
            self.picard.build_bam_index.generate_shell_files(data,
                                                             parameters,
                                                             sex)
            self.gatk.indel_realigner.generate_shell_files(data,
                                                           parameters,
                                                           sex)
            self.gatk.haplotype_caller.generate_shell_files(data,
                                                            parameters,
                                                            sex)
            for lane, mates in lanes.items():
                self.bwa.mapping.generate_shell_files(data,
                                                      parameters,
                                                      sex,
                                                      lane,
                                                      mates)
                self.picard.sort.generate_shell_files(data,
                                                      parameters,
                                                      sex,
                                                      lane)
                self.picard.add_read_groups.generate_shell_files(data,
                                                                 parameters,
                                                                 sex,
                                                                 lane)

    def get_files_info(self, data):
        files_info = defaultdict(lambda: defaultdict(lambda: list()))
        for file in data.reads_paths:
            dir_path, file_name = os.path.split(file)
            file_name = file_name.replace('.fastq.gz', '')
            fields = file_name.split('_')
            sex = fields[0]
            lane = fields[1]
            mate = fields[2]
            files_info[sex][lane].append(mate)
        return files_info

    def reset_qsub_files(self, data):
        qsub_files = [os.path.join(data.directories.qsub, f) for
                      f in os.listdir(data.directories.qsub) if
                      f.endswith('.sh')]
        for qsub_file in qsub_files:
            os.remove(qsub_file)
