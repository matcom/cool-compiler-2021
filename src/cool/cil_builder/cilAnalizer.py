from cool.cil_builder.cool_to_cil_visitor import COOLToCILVisitor
from cool.mips_builder.cil_to_mips_visitor import CILtoMIPSVisitor

def run_code_gen_pipeline(cool_ast,context,scope):
    cool_to_cilVisitor = COOLToCILVisitor(context)
    cil_ast = cool_to_cilVisitor.visit(cool_ast,scope)

    cil_to_mipsVisitor = CILtoMIPSVisitor(context)
    mips_text = cil_to_mipsVisitor.visit(cil_ast)
    
    return mips_text