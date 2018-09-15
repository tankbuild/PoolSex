import os
from poolsex.data import variables


def get_parameters(data):

    try:
        settings_file = open(data.files[variables.files.settings])
        settings = {name: value for
                    name, value in (line[:-1].split('=') for
                                    line in settings_file if
                                    line and not line.startswith('#'))}
    except OSError:
        settings = {}

    parameters = data.parameters

    for name, value in settings.items():
        try:
            parameters[name] = value
        except KeyError:
            print('** Error: parameter "' + name + '" does not exist.')
        except ValueError:
            print('** Error: could not affect value "' + str(value) +
                  '" to parameter "' + name + '".')

    parameters[variables.parameters.java_temp_dir] = os.path.join(data.directories[variables.directories.results],
                                                                  parameters[variables.parameters.java_temp_dir_name])

    return parameters
