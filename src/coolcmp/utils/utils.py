"""

"""


def find_column(input_text: str, token_lexpos: int) -> int:
    """
    Used for compute column of tokens. Assumed that tabs have length 4.
    """
    line_start = input_text.rfind('\n', 0, token_lexpos) + 1
    return (token_lexpos - line_start) + input_text.count('\t', line_start, token_lexpos) * 3 + 1


def extract_meth_name(name: str):
    """
    Returns the name of a method when has the name of a class in front.
    Example:
        Object_type_name -> type_name
        IO_out_string -> out_string
    """
    return name[name.find('_') + 1:]