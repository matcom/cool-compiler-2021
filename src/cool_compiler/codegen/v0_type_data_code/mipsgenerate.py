from cool_compiler.types.type import Type
from ...cmp import visitor
from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from . import type_data_code_ast as ASTR
from .type_data_code_ast import result, super_value


class MipsGenerate: 
    def __init__(self, errors) -> None:
        self.errors = errors
        self.data =[]
        self.text=[]



    @visitor.on('node')
    def visit(node):
        pass

    @visitor.when(ASTR.Program)
    def visit(self, node: ASTR.Program):
        self.Program = node
        for Function in node.functions:
            Function.visit(node)
        pass
    
    @visitor.when(ASTR.Local)
    def visit(self, node: ASTR.Local):
        s =""
        s = str(node.x) + ":" + " .word" + " 11"
        self.data.append(s)
        pass
    
    @visitor.when(ASTR.Data)
    def visit (self , node:ASTR.Data) :
        pass

    
    @visitor.when(ASTR.ALLOCATE)
    def visit (self,node : ASTR.ALLOCATE):
        
        
        pass


    @visitor.when(ASTR.Arg)
    def visit (self,node : ASTR.Arg):
        pass


    
    @visitor.when(ASTR.Call)
    def visit (self,node : ASTR.Call):
        pass



