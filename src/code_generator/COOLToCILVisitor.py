from cil_ast import *
import BaseCOOLToCILVisitor
from utils import visitor

class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(AllocateNode('Main', instance))
        self.register_instruction(ArgNode(instance))
        self.register_instruction(CallNode(self.to_function_name('main', 'Main'), result))
        self.register_instruction(ReturnNode(0))
        self.current_function = None
       # self.create_built_in()
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return ProgramNode(self.dottypes, self.dotdata, self.dotcode)