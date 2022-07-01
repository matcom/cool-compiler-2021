from .cil_to_mips import CilToMipsVisitor
from .cool_to_cil import CoolToCilVisitor

class MyCodeGenerator:
    def __init__(self, context):
        self.context = context

    def compile(self, cool_ast, scope):
        cool_to_cil = CoolToCilVisitor(self.context)
        cil_ast = cool_to_cil.visit(cool_ast,scope)
        cil_to_mips = CilToMipsVisitor()
        mips_code = cil_to_mips.visit(cil_ast)
        return mips_code