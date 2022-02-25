from .cil_visitor import CilVisitor
from .mips_visitor import MipsVisitor
from ..semantic.helpers import Context


def run_pipeline(context: Context, ast, scope):
    cool_to_cil = CilVisitor(context)
    cil_ast = cool_to_cil.visit(ast, scope)

    inherit_graph = context.build_inheritance_graph()

    data_code, text_code = MipsVisitor(inherit_graph).visit(cil_ast)

    return make_code(data_code, text_code)


def make_code(data_code, text_code) -> str:
    ans = '\n'.join(text_code) + '\n' + '\n'.join(data_code)

    return ans
