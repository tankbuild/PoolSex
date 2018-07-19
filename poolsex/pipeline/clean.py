from poolsex.data import variables


def remove_modules_files(modules, step=variables.modules.index, check=False):
    manual_input = 'y'
    if check:
        manual_input = None
        while manual_input not in ['y', 'n']:
            manual_input = input('You are about to erase some of the results files. Do you want to continue ? (y/n) : ')
            if manual_input not in ['y', 'n']:
                print('** Error: "' + manual_input + '"" not recognized. Expected y/n')
    if manual_input == 'y':
        clean = False
        for name, module in modules.items():
            if name == step:
                clean = True
            if clean:
                module.clean_module_files()
    else:
        return
