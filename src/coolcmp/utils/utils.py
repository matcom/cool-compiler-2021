"""

"""


def find_column(input_text: str, token_lexpos: int) -> int:
    """
    Used for compute column of tokens. Assumed that tabs have length 4.
    """
    line_start = input_text.rfind('\n', 0, token_lexpos) + 1
    return (token_lexpos - line_start) + input_text.count('\t', line_start, token_lexpos) * 3 + 1
