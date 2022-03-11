from ntpath import join
from CodeGen.Intermediate.Generator import COOLToCILVisitor
from CodeGen.Intermediate.cil import Scope
from CodeGen.Assembler.Generator import CILToSPIMVisitor
from CodeGen.Assembler.mips import MIPSVisitor
from Semantic.Semantic import COOL_Semantic_Checker 
from Parser.Parser import COOL_Parser
from Semantic.scope import COOL_Scope
from Lexer.Lexer import COOL_Lexer
import sys

class COOL_Compiler:

    def __init__(self):
        self.cool_lexer = COOL_Lexer()
        self.cool_parser = COOL_Parser(self.cool_lexer)
    
    def run(self, code):
        # Lexic & Sintactic Analizer
        ast = self.cool_parser.run(code)
        
        if self.cool_lexer.errors:
            exit(1)

        if self.cool_parser.errors:
            for error in self.cool_parser.error_list:
                sys.stdout.write(f'{error}\n')
            exit(1)
        
        # Semantic Analyzer
        cool_checker = COOL_Semantic_Checker()
        scope = cool_checker.visit(ast)
        
        if cool_checker.errors:
            exit(1)
        
        # Intermediate Code Gen
        cool_intermediate_code = COOLToCILVisitor(scope)
        cil_code = cool_intermediate_code.visit(ast, scope)
        
        # MIPS Code Gen
        cil_smips_code = CILToSPIMVisitor()
        (data, text) = cil_smips_code.visit(cil_code)
        
        mips_data = ".data"
        for d in data:
            mips_data += str(d)
        mips_text = "\n\n.text\n.globl main"
        for t in text:
            mips_text += str(t)
        
        return mips_data + mips_text


def main(file):
    with open(file, "r") as fd:
        data = fd.read()
    data = data.replace('\t', "    ")

    _cmp = COOL_Compiler()
    mips_instr = _cmp.run(data)
    
    with open('code.mips', "r") as fd:
        mips_instr += fd.read()
    
    output_file = file.split('.')
    output_file[-1] = 'mips'
    mips_exec = ".".join(output_file)
    
    with open(mips_exec, "w") as fd:
        fd.write(mips_instr)
        

if __name__ == '__main__':
    main(sys.argv[1])