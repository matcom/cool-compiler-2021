from .types_data_visitor import DotTypesDataVisitor
from .code_visitor import DotCodeVisitor


def build_cil(ast, context, scope):
    cil = DotTypesDataVisitor(context).visit(ast)

    DotCodeVisitor(cil, context).visit(ast, scope)

    return cil
