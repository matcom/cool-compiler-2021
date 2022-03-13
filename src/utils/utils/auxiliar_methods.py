from os import read

def erase_multiline_comment(str):
    errors = []
    result = ''
    i = 0
    row = 1
    column = 1

    comm_init = 0
    comm_end = 0

    while i < len(str):
        if str[i] == '\n':
            result += '\n'
            row += 1
            column = 1
            i += 1
            continue
            
        elif str[i] == '\t':
            result += '    '
            column += 4
            i += 1
            continue

        if comm_init == 0:
            if i + 1 < len(str):
                if str[i] == '(' and str[i + 1] == '*':
                    comm_init += 1
                    result += '  '
                    column += 2
                    i += 2
                    continue
                elif str[i] == '*' and str[i + 1] == ')':
                    errors.append(f'({row}, {column}) - LexicographicError: EOF in comment')
                    result += '  '
                    column += 2
                    i += 2
                    continue
            result += str[i]
            column += 1
            i += 1
        
        else:
            if i + 1 < len(str):
                if str[i] == '(' and str[i + 1] == '*':
                    comm_init += 1
                    result += '  '
                    column += 2
                    i += 2
                    continue
                elif str[i] == '*' and str[i + 1] == ')':
                    comm_end += 1
                    if comm_end > comm_init:
                        errors.append(f'({row}, {column}) - LexicographicError: EOF in comment')
                    elif comm_end  == comm_init:
                        comm_init = 0 
                        comm_end = 0

                    result += '  '
                    column += 2
                    i += 2
                    continue
            result += ' '
            column += 1
            i += 1

    if comm_init > comm_end:
        errors.append(f'({row}, {column}) - LexicographicError: EOF in comment')

    return errors, result

