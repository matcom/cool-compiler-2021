"""

"""


def find_column(input_text: str, token_lexpos: int) -> int:
    """
    Used for compute column in case of error.
    """
    line_start = input_text.rfind('\n', 0, token_lexpos) + 1

    return (token_lexpos - line_start) + 1
