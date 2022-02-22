from .utils import visitor
from .utils.mips_utils import *
from .ast_CIL import *


class Mips:
    def __init__(self, file_name: str):
        self.asm_file = f"{file_name}.asm"
        self.str_out = ""

    def write_line_in_asm(self, to_write: str):
        self.str_out += to_write
        with open(self.asm_file, "a") as f:
            f.write(to_write)

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(CILProgram)
    def visit(self, cil: CILProgram):
        NotImplemented

    # MAYBE IT SHOULD BE ERASED
    @visitor.when(CILDeclaration)
    def visit(self, cil: CILDeclaration):
        NotImplemented

    @visitor.when(CILFuncDeclaration)
    def visit(self, cil: CILFuncDeclaration):
        NotImplemented

    @visitor.when(CILSimpleAssignInstruction)
    def visit(self, cil: CILSimpleAssignInstruction):
        NotImplemented

    @visitor.when(CILBinaryInstruction)
    def visit(self, cil: CILBinaryInstruction):
        if isinstance(cil, CILArithBinaryInstruction):
            self.visit_arithB(cil)
        if isinstance(cil, CILBooleanBinaryInstruction):
            self.visit_boolB(cil)

    def visit_boolB(self, node: CILBooleanBinaryInstruction):
        if isinstance(node, CILLessInstruction):
            pass  # do something
        if isinstance(node, CILEqualInstruction):
            pass  # do something
        if isinstance(node, CILLessEqualInstruction):
            pass  # do something

    def visit_arithB(self, node: CILArithBinaryInstruction):
        if isinstance(node, CILPlusInstruction):  # add $dest, $r0, $r1
            pass
        if isinstance(node, CILMinusInstruction):  # sub $dest, $r0, $r1
            pass
        # mult $a0, $a1\n")
        # mfhi $t0\n")
        # mflo $t1\n")
        if isinstance(node, CILStarInstruction):
            pass
        # check div /0 error
        # div $a0, $a1\n")
        # mfhi $t0\n")
        # mflo $t1\n")
        if isinstance(node, CILDivInstruction):
            pass

    @visitor.when(CILGETATTRInst)
    def visit(self, cil: CILGETATTRInst):
        NotImplemented

    @visitor.when(CILSETATTRInst)
    def visit(self, cil: CILSETATTRInst):
        NotImplemented

    @visitor.when(CILGETINDEXInst)
    def visit(self, cil: CILGETINDEXInst):
        NotImplemented

    @visitor.when(CILSETINDEXInst)
    def visit(self, cil: CILSETINDEXInst):
        NotImplemented

    @visitor.when(CILALLOCATEInst)
    def visit(self, cil: CILALLOCATEInst):
        NotImplemented

    @visitor.when(CILTYPEOFInst)
    def visit(self, cil: CILTYPEOFInst):
        NotImplemented

    @visitor.when(CILARRAYInst)
    def visit(self, cil: CILARRAYInst):
        NotImplemented

    @visitor.when(CILCALLInst)
    def visit(self, cil: CILCALLInst):
        NotImplemented

    @visitor.when(CILVCALLInst)
    def visit(self, cil: CILVCALLInst):
        NotImplemented

    @visitor.when(CILARGInst)
    def visit(self, cil: CILARGInst):
        NotImplemented

    @visitor.when(CILLABELInst)
    def visit(self, cil: CILLABELInst):
        NotImplemented

    @visitor.when(CILGOTOInst)
    def visit(self, cil: CILGOTOInst):
        NotImplemented

    @visitor.when(CILIFGOTOInst)
    def visit(self, cil: CILIFGOTOInst):
        NotImplemented

    @visitor.when(CILRETURNInst)
    def visit(self, cil: CILRETURNInst):
        NotImplemented

    @visitor.when(CILLOADInst)
    def visit(self, cil: CILLOADInst):
        NotImplemented

    @visitor.when(CILSTRInst)
    def visit(self, cil: CILSTRInst):
        NotImplemented

    @visitor.when(CILLENGTHInst)
    def visit(self, cil: CILLENGTHInst):
        NotImplemented

    @visitor.when(CILCONCATInst)
    def visit(self, cil: CILCONCATInst):
        NotImplemented

    @visitor.when(CILSUBSTRINGInst)
    def visit(self, cil: CILSUBSTRINGInst):
        NotImplemented

    @visitor.when(CILREADIntInst)
    def visit(self, cil: CILREADIntInst):
        NotImplemented

    @visitor.when(CILREADStringInst)
    def visit(self, cil: CILREADStringInst):
        NotImplemented

    @visitor.when(CILPRINTInst)
    def visit(self, cil: CILPRINTInst):
        NotImplemented

    @visitor.when(CILVoidInstruction)
    def visit(self, cil: CILVoidInstruction):
        NotImplemented
