from collections import defaultdict, OrderedDict
import os
from poolsex.modules import Module
from poolsex.data import variables


def create_modules(data):

    files_info = defaultdict(lambda: defaultdict(lambda: list()))
    for file in data.files[variables.files.reads]:
        dir_path, file_name = os.path.split(file)
        file_name = file_name.split('.')[0]
        fields = file_name.split('_')
        sex = fields[0]
        lane = fields[1]
        mate = fields[2]
        files_info[sex][lane].append(mate)

    modules = OrderedDict()
    for module, module_data in data.modules.items():
        modules[module] = Module(module, module_data, data, files_info)

    for name, module in modules.items():
        if module.data[variables.modules_options.dependencies]:
            for instance, instance_data in module.instances.items():

                if 'unique' in modules[module.data[variables.modules_options.dependencies]].instances.keys():

                    input_files = modules[module.data[variables.modules_options.dependencies]].instances['unique'][variables.instance_options.results]
                    modules[name].instances[instance][variables.instance_options.input] = input_files

                    dependencies = modules[module.data[variables.modules_options.dependencies]].instances['unique'][variables.instance_options.name]
                    modules[name].instances[instance][variables.instance_options.dependencies] = dependencies

                else:

                    if not instance_data[variables.instance_options.sex]:

                        input_files = [i[variables.instance_options.results] for
                                       i in modules[module.data[variables.modules_options.dependencies]].instances.values()]
                        modules[name].instances[instance][variables.instance_options.input] = input_files

                        dependencies = [i[variables.instance_options.name] for
                                        i in modules[module.data[variables.modules_options.dependencies]].instances.values()]
                        modules[name].instances[instance][variables.instance_options.dependencies] = dependencies

                    else:

                        if not instance_data[variables.instance_options.lane]:

                            input_files = [i[variables.instance_options.results] for
                                           i in modules[module.data[variables.modules_options.dependencies]].instances.values() if
                                           i[variables.instance_options.sex] == instance_data[variables.instance_options.sex]]
                            modules[name].instances[instance][variables.instance_options.input] = input_files

                            dependencies = [i[variables.instance_options.name] for
                                            i in modules[module.data[variables.modules_options.dependencies]].instances.values() if
                                            i[variables.instance_options.sex] == instance_data[variables.instance_options.sex]]
                            modules[name].instances[instance][variables.instance_options.dependencies] = dependencies

                        else:

                            input_files = [i[variables.instance_options.results] for
                                           i in modules[module.data[variables.modules_options.dependencies]].instances.values() if
                                           i[variables.instance_options.sex] == instance_data[variables.instance_options.sex] and
                                           i[variables.instance_options.lane] == instance_data[variables.instance_options.lane]]
                            modules[name].instances[instance][variables.instance_options.input] = input_files

                            dependencies = [i[variables.instance_options.name] for
                                            i in modules[module.data[variables.modules_options.dependencies]].instances.values() if
                                            i[variables.instance_options.sex] == instance_data[variables.instance_options.sex] and
                                            i[variables.instance_options.lane] == instance_data[variables.instance_options.lane]]
                            modules[name].instances[instance][variables.instance_options.dependencies] = dependencies
                if input_files:
                    input_files.sort()

    return modules
