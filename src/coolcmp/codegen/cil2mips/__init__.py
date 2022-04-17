from .cil2mips_visitor import CILToMipsVisitor


def build_mips(ast, context, scope):
    return CILToMipsVisitor().visit(ast)
