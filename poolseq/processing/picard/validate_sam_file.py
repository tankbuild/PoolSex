import os
import poolseq.genotoul as genotoul
from poolseq.processing import file_utils


class ValidateSamFile():

    def __init__(self, data):
        self.qsub_file_path = os.path.join(data.directories.qsub, 'picard_validate.sh')
        self.shell_file_path = []
        self.output_file_path = []

    def generate_shell_files(self, data, parameters, sex):
        qsub_file = file_utils.wa_open(self.qsub_file_path)
        base_file_name = sex
        base_shell_name = 'picard_validate_' + base_file_name
        shell_file_path = os.path.join(data.directories.shell, base_shell_name + '.sh')
        shell_file = open(shell_file_path, 'w')
        output_file_path = os.path.join(data.directories.output, base_file_name + '_validation.txt')
        input_file_path = os.path.join(data.directories.output, base_file_name + '.bam')
        genotoul.print_header(shell_file,
                              name=base_shell_name,
                              mem=parameters.mem,
                              h_vmem=parameters.h_vmem)
        genotoul.print_java_module(shell_file)
        shell_file.write(parameters.java +
                         ' -Xmx' + parameters.java_mem +
                         ' -Djava.io.tmpdir=' + parameters.java_temp_dir +
                         ' -jar ' + parameters.picard +
                         ' ValidateSamFile' +
                         ' I=' + input_file_path +
                         ' O=' + output_file_path +
                         ' TMP_DIR=' + parameters.java_temp_dir +
                         ' MAX_OPEN_TEMP_FILES=' + parameters.max_open_temp_files)
        shell_file.close()
        self.shell_file_path.append(shell_file_path)
        self.output_file_path.append(output_file_path)
        qsub_file.write('qsub ' + shell_file_path + '\n')
        qsub_file.close()
