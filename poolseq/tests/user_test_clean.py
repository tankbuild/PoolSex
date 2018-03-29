

def user_check_clean():

    manual_input = None
    while manual_input not in ['y', 'n']:
        manual_input = input('You are about to erase some of the results files. Do you want to continue ? (y/n) : ')
        if manual_input not in ['y', 'n']:
            print('** Error: "' + manual_input + '"" not recognized. Expected y/n')
    if manual_input == 'y':
        return True
    else:
        return False
