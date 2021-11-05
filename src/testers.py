import os
from parser import parse


def find_files(file_directory):
    files = os.listdir(file_directory)
    file_dict = {}

    for file in files:
        if file.endswith('cl'):
            f_name = file.split('.')[0]
        else:
            f_name = file.split('_')[0]

        try:
            file_dict[f_name].append(file)
        except KeyError:
            file_dict[f_name] = [file]

    return file_dict


def parser_tester(file_directory):
    file_dict = find_files(file_directory)
    # print(file_dict)

    for program in file_dict:
        print(program)
        files = file_dict[program]
        if files[0].endswith('cl'):
            f_cl, f_errors = files
        else:
            f_errors, f_cl = files

        program_cl_route = file_directory + '/' + f_cl
        program_errors_route = file_directory + '/' + f_errors
        with open(program_cl_route, 'r', encoding='UTF-8') as f:
            tree, errors = parse(f.read())

        with open(program_errors_route, 'r', encoding='UTF-8') as f:
            text = f.read()
            print(text)
            print(errors)
