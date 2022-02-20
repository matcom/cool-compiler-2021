from .cil_visitor import CILVisitor
from .types_data_visitor import DotTypesDataVisitor
from .code_visitor import DotCodeVisitor


def build_cil(ast, context, scope):
    cil = DotTypesDataVisitor(context).visit(ast)

    DotCodeVisitor(cil).visit(ast, scope)

    return cil
