from .utils import visitor
from .ast_hierarchy import *
from .ast_CIL import *

class CILVisitor:
    def __init__(self):
        self.locals_counter=1
        self.attr_counter=1
        self.labels_counter=1

    #Chack local |LOCAL
    def locals_creator(self):
        current_local=f"local {self.locals_counter}"
        self.locals_counter+=1
        return current_local  

    def labels_creator(self):
        current_label=f"label {self.labels_counter}"
        self.labels_counter+=1
        return current_label

    def attr_creator(self,name):
        current_attr=f"{name}_{self.attr_counter}"
        self.attr_counter+=1
        return current_attr


    @visitor.on("node")
    def visit(self, node, cil_obj):
        pass

    @visitor.when(ProgramNode)
    def visit(self,node:ProgramNode,func:CILNode):NotImplemented

    @visitor.when(ClassDeclarationNode)
    def visitor(self,node:ClassDeclarationNode,func:CILNode):NotImplemented

    @visitor.when(FuncDeclarationNode)
    def visit(self,node:FuncDeclarationNode,func:CILProgram):NotImplemented

    @visitor.when(AttrDeclarationNode)
    def visit(self,node:AttrDeclarationNode,func:CILFuncDeclaration):
        val=self.visit(node.val,func)
        name=self.attr_creator(node.id)
        func.add_locals([name])
        func.add_instruction([CILALLOCATEInst(name,node.type),CILSimpleAssignInstruction(name,val)],0)
        return name

    @visitor.when(AtomicNode)
    def visit(self,node:AtomicNode,func:CILFuncDeclaration):
        if isinstance(node,ConstantNumNode):
            type="INT"
            value=node.lex
        if isinstance(node,BoolNode):
            type="BOOL"
            value=1 if node.lex=="true" else 0
        if isinstance(node,InstantiateNode):pass #not implemented
        if isinstance(node,StringNode):pass #not implemented
        if isinstance(node,VariableNode):pass #not implemented

        current_local=self.locals_creator()
        func.add_locals([current_local])
        func.add_instruction([CILALLOCATEInst(current_local,type),CILSETATTRInst(current_local,0,value)],0)

    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode,func:CILFuncDeclaration):
        if isinstance(node,ArithBinaryNode):return self.visit_binary_arith(node,func)
        if isinstance(node,BooleanBinaryNode):return self.visit_binary_boolean(node,func)

    def visit_binary_arith(self,node:ArithBinaryNode,func:CILFuncDeclaration):
        current_local=self.locals_creator()
        func.add_locals([current_local])
        func.add_instruction([CILALLOCATEInst(current_local,"INT")],0)

        left=self.visit(node.left,func)
        right=self.visit(node.right,func)
        if isinstance(node,PlusNode):
            func.add_instruction([CILPlusInstruction(current_local,left,right)])
        if isinstance(node,MinusNode):
            func.add_instruction([CILMinusInstruction(current_local,left,right)])
        if isinstance(node,StarNode):
            func.add_instruction([CILStarInstruction(current_local,left,right)])
        if isinstance(node,DivNode):
            func.add_instruction([CILDivInstruction(current_local,left,right)])
        return current_local    
        
    def visit_binary_boolean(self,node:BooleanBinaryNode,func:CILFuncDeclaration):
        current_local=self.locals_creator()
        func.add_locals([current_local])
        func.add_instruction([CILALLOCATEInst(current_local,"BOOL")],0)

        left=self.visit(node.left,func)
        right=self.visit(node.right,func)
        
        if isinstance(node,LessNode):
            func.add_instruction(CILLessInstruction(current_local,left,right))     
        if isinstance(node,LessEqualNode):
            func.add_instruction(CILLessEqualInstruction(current_local,left,right))     
        if isinstance(node,EqualNode):
            func.add_instruction(CILEqualInstruction(current_local,left,right))     
        return current_local

    @visitor.when(NotNode)
    def visit(self,node:NotNode,func:CILFuncDeclaration):
        current_local=self.locals_creator()
        func.add_locals([current_local])
        func.add_instruction([CILALLOCATEInst(current_local,"BOOL")],0)
        val=self.visit(node.expr,func)
        not_val=0 if val else 1
        func.add_instruction([CILSimpleAssignInstruction(current_local,not_val)])
        return current_local
    
    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, func:CILFuncDeclaration):
        current_local=self.locals_creator()
        func.add_locals([current_local])
        func.add_instruction([CILALLOCATEInst(current_local,"BOOL"),CILSETATTRInst(current_local,0,0)],0)
        _=self.visit(node.expr,func)
        return current_local

    @visitor.when(AssignNode)
    def visit(self,node:AssignNode,func:CILFuncDeclaration):NotImplemented

    @visitor.when(IntCompNode)
    def visit(self,node:IntCompNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(CallNode)
    def visit(self,node:CallNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(CaseNode)
    def visit(self,node:CaseNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(LetNode)
    def visit(self,node:LetNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(BlockNode)
    def visit(self,node:BlockNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(LoopNode)
    def visit(self,node:LoopNode,func:CILFuncDeclaration):NotImplemented

    @visitor.when(ConditionalNode)
    def visit(self,node:ConditionalNode,func:CILFuncDeclaration):NotImplemented
    
    @visitor.when(AttrDeclarationNode)
    def visit(self,node:BlockNode,func:CILNode):NotImplemented
