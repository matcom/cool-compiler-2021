from utils.utils import Utils
from code_generation.mips.visitor import CilToMips
from code_generation.cil.visitor import Visitor as CILVisitor

class CodeGeneration:

    def __init__(self, ast, context, scope, debug_path, debug=True):
        self.ast = ast
        self.context = context
        self.scope = scope
        self.debug = debug
        self.debug_path = debug_path

    def code_generation(self):
        
        cool_to_cil = CILVisitor(self.context)
        cil_ast = cool_to_cil.visit(self.ast, self.scope)

        inherit_graph = self.context.build_inheritance_graph()
        data_code, text_code = CilToMips(inherit_graph).visit(cil_ast)
        mips_code = self.get_code(data_code, text_code)

        return mips_code

    def get_code(self, data_code, text_code):
        mips_code = '\n'.join(text_code) + '\n' + '\n'.join(data_code)
        Utils.Write(self.debug_path, '.mips', mips_code) if self.debug else None

        return mips_code
