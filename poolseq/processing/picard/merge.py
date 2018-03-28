import os
import poolseq.genotoul as genotoul


class Merge():

    def __init__(self, data, files_info):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'picard_merge.sh')
        self.shell_file_path = {}
        self.output_file_path = []
        self.job_id = []
        self.prefix = 'picard_merge'

    def generate_shell_files(self, data, parameters, sex, lanes):
        base_file_name = sex
        base_shell_name = self.prefix + '_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.results, base_file_name + '.bam')
        lane_file_paths = [os.path.join(data.directories.results, sex + '_' + lane + '_read_groups.bam') for
                           lane in lanes]
        self.job_id.append(base_shell_name)
        if len(lane_file_paths) > 1:
            genotoul.print_header(shell_file,
                                  name=base_shell_name,
                                  mem=parameters.mem,
                                  h_vmem=parameters.h_vmem)
            genotoul.print_java_module(shell_file)
            shell_file.write(parameters.java +
                             ' -Xmx' + parameters.java_mem +
                             ' -jar ' + parameters.picard +
                             ' MergeSamFiles')
            for lane_file_path in lane_file_paths:
                shell_file.write(' I=' + lane_file_path)
            shell_file.write(' O=' + output_file_path)
        else:
            genotoul.print_header(shell_file,
                                  name=base_shell_name)
            shell_file.write('ln -s ' + lane_file_paths[0] +
                             ' ' + output_file_path)
        shell_file.close()
        self.shell_file_path[sex] = shell_file_path
        self.output_file_path.append(output_file_path)
