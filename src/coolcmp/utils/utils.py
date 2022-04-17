"""

"""


def find_column(input_text: str, token_lexpos: int) -> int:
    """
    Used for compute column of tokens. Assumed that tabs have length 4.
    """
    line_start = input_text.rfind('\n', 0, token_lexpos) + 1
    return (token_lexpos - line_start) + input_text.count('\t', line_start, token_lexpos) * 3 + 1


def extract_feat_name(name: str) -> str:
    """
    Returns the name of a feature when has the name of a class in front.
    Example:
        Object_type_name -> type_name
        IO_out_string -> out_string
    """
    return name[name.find('_') + 1:]


def extract_class_name(name: str) -> str:
    """
    Returns the name of a class when has the name of a feature back.
    Example:
        Object_type_name -> Object
        IO_out_string -> IO
    """
    return name[:name.find('_')]


def split_class_and_feat(name: str) -> tuple[str, str]:
    """
    Splits the full feature name in class name and feature name
    Example:
        Object_type_name -> (Object, type_name)
        IO_out_string -> (IO, out_string)
    """
    return extract_class_name(name), extract_feat_name(name)
