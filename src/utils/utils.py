def find_column(input_text, lexpos):
    line_start = input_text.rfind("\n", 0, lexpos) + 1
    return (lexpos - line_start) + 1


def find_last_line(input_text):
    if not input_text:
        return 0
    line_no = input_text.count("\n")
    return line_no


def display_errors(error_list):
    if error_list:
        for e in error_list:
            print(e)
        exit(1)