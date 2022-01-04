from dataclasses import dataclass

from ast.ccil_ast import ExpressionNode


@dataclass
class LocalVar:
    cool_name: str
    ccil_name: str
    boundExpression: ExpressionNode | None


def make_id(name: str, main_num: int, snd_num: int = -1, thrd_num: int = -1):
    main_num_str = str(main_num)
    snd_num_str = ""
    thrd_num_str = ""

    if snd_num != -1:
        snd_num_str = f"_{snd_num}"
    if thrd_num != -1:
        thrd_num_str = f"_{thrd_num}"

    return f"{name}_{main_num_str}{snd_num_str}{thrd_num_str}"
