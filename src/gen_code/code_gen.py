

from .cil import ast_to_cil
from .mips import programMIPS


def generate_code(ast):
    cil_ast = ast_to_cil(ast)
    mips_program = programMIPS(cil_ast)
    return str(mips_program)
