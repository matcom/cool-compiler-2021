from dataclasses import dataclass

from asts.ccil_ast import ExpressionNode


@dataclass
class Feature:
    cool_name: str
    ccil_name: str
    attribute: bool

    @property
    def is_attribute(self):
        return self.attribute


@dataclass
class LocalVar:
    cool_name: str
    ccil_name: str
    boundExpression: ExpressionNode | None

    @property
    def get_name(self):
        assert self.ccil_name != ""
        return self.ccil_name

    @staticmethod
    def new_temporal_var(name: str, boundExpression: ExpressionNode):
        return LocalVar("", name, boundExpression)

    @staticmethod
    def new_user_defined_var(
        name: str, ccil_name: str, boundExpression: ExpressionNode | None = None
    ):
        return LocalVar(name, ccil_name, boundExpression)


def make_id(
    name: str, main_num: int, aux_name: str = "", snd_num: int = -1, thrd_num: int = -1
):
    main_num_str = str(main_num)
    snd_num_str = ""
    thrd_num_str = ""

    if aux_name != "":
        aux_name = f"_{aux_name}"
    if snd_num != -1:
        snd_num_str = f"_{snd_num}"
    if thrd_num != -1:
        thrd_num_str = f"_{thrd_num}"

    return f"{name}{aux_name}_{main_num_str}{snd_num_str}{thrd_num_str}"
