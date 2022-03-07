#from cool.utils.config import *
#import cool.structs.mips_ast_hierarchy as mips
import code_gen.mips_nodes as mips
import cmp.visitor as visitor

class MIPSWriter(object):
    def __init__(self):
        self.tabs = 0
        self.output = []

    def emit(self, msg):
        self.output.append(self.tabs*" " + msg)

    def black(self):
        self.output.append('')

    def visit(self, node:mips.ProgramNode):
        self.emit(".data")
        self.black()
        for data in node.data:
            self.emit(str(data))

        self.black()
        self.emit(".text")
        self.emit(".globl main")
        self.black()
        for proc in node.text:
            self.emit(f'{proc.label}:')
            self.tabs += 4
            for inst in proc.instructions:
                self.emit(str(inst))
            self.tabs -= 4





     