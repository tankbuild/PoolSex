import os
from collections import defaultdict
from poolseq.processing.bwa import Bwa
from poolseq.processing.picard import Picard
from poolseq.processing.samtools import Samtools
from poolseq.processing.popoolation import Popoolation


class Processing():

    def __init__(self, data):
        self.files_info = self.get_files_info(data)
        self.bwa = Bwa(data, self.files_info)
        self.picard = Picard(data, self.files_info)
        self.samtools = Samtools(data, self.files_info)
        self.popoolation = Popoolation(data, self.files_info)
        self.sexes = self.files_info.keys()

    def generate_shell_files(self, data, parameters, step=None):
        self.reset_qsub_files(data)
        self.reset_shell_files(data)
        self.bwa.index.generate_files(data, parameters)
        for sex, lanes in self.files_info.items():
            self.picard.merge.generate_shell_files(data,
                                                   parameters,
                                                   sex,
                                                   lanes)
            self.picard.mark_duplicates.generate_shell_files(data,
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
        self.samtools.mpileup.generate_shell_files(data, parameters, self.sexes)
        self.popoolation.mpileup2sync.generate_shell_files(data, parameters)
        self.generate_pipeline_shell_file(data, step)

    def get_files_info(self, data):
        files_info = defaultdict(lambda: defaultdict(lambda: list()))
        for file in data.reads_paths:
            dir_path, file_name = os.path.split(file)
            file_name = file_name.split('.')[0]
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

    def reset_shell_files(self, data):
        shell_files = [os.path.join(data.directories.shell, f) for
                       f in os.listdir(data.directories.shell) if
                       f.endswith('.sh')]
        for shell_file in shell_files:
            os.remove(shell_file)

    def generate_pipeline_shell_file(self, data, step):
        qsub_file_path = os.path.join(data.directories.qsub, 'run_pipeline.sh')
        qsub_file = open(qsub_file_path, 'w')
        if step < 1:
            qsub_file.write('qsub ' + self.bwa.index.shell_file_path + '\n')
        for sex, lanes in self.files_info.items():
            for lane, mates in lanes.items():
                if step < 2:
                    qsub_file.write('qsub ')
                    if step < 1:
                        qsub_file.write('-hold_jid ' + self.bwa.index.job_id + ' ')
                    qsub_file.write(self.bwa.mapping.shell_file_path[sex][lane] + '\n')
                if step < 3:
                    qsub_file.write('qsub ')
                    if step < 2:
                        qsub_file.write('-hold_jid ' + '_'.join([self.bwa.mapping.prefix, sex, lane]) + ' ')
                        qsub_file.write(self.picard.sort.shell_file_path[sex][lane] + '\n')
                if step < 4:
                    qsub_file.write('qsub ')
                    if step < 3:
                        qsub_file.write('-hold_jid ' + '_'.join([self.picard.sort.prefix, sex, lane]) + ' ')
                    qsub_file.write(self.picard.add_read_groups.shell_file_path[sex][lane] + '\n')
            if step < 5:
                qsub_file.write('qsub ')
                if step < 4:
                    qsub_file.write('-hold_jid ' + ','.join(['_'.join([self.picard.add_read_groups.prefix, sex, lane]) for lane in lanes]) + ' ')
                qsub_file.write(self.picard.merge.shell_file_path[sex] + '\n')
            if step < 6:
                qsub_file.write('qsub ')
                if step < 5:
                    qsub_file.write('-hold_jid ' + self.picard.merge.prefix + '_' + sex + ' ')
                qsub_file.write(self.picard.mark_duplicates.shell_file_path[sex] + '\n')
        if step < 7:
            qsub_file.write('qsub ')
            if step < 6:
                qsub_file.write('-hold_jid ' + ','.join(['_'.join([self.picard.mark_duplicates.prefix, sex]) for sex in self.sexes]) + ' ')
            qsub_file.write(self.samtools.mpileup.shell_file_path + '\n')
        qsub_file.write('qsub ')
        if step < 7:
            qsub_file.write('-hold_jid ' + self.samtools.mpileup.job_id + ' ')
        qsub_file.write(self.popoolation.mpileup2sync.shell_file_path + '\n')
