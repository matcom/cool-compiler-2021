

def find_column(input_text, token):
    line_start = input_text.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def find_last_line(input_text):
    if not input_text:
        return 0
    line_no = input_text.count('\n')
    return line_no
