from core.tools import visitor
import core.mips.MipsAst as mips

class MIPSAstFormatter:
    @visitor.on('node')
    def visit(self, node):
        pass

