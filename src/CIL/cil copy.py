from CIL.builder import builder_main, builder_types
import Utils.visitor as visitor
import CIL.ast as cil

from Parser.ast import *

class CIL:
    def __init__(self, context):
        self.context = context
        self.label_count = 0

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.data = {}
        
        self.code = [builder_main()]
        self.types = builder_types(self.context)

        for def_class in node.class_list:
            self.visit(def_class)

        return cil.ProgramNode(self.types.values(), self.data.values(), self.code)

    @visitor.when(ClassNode)
    def visit(self, node):
        self.current = self.context.get_type(node.type.value)
        self.init = cil.CodeNode(f'{self.current.name}.init', [], [], [])

        for feature in node.feature_list:
            self.visit(feature)

    @visitor.when(MethodNode)
    def visit(self, node):
        self.locals = {}
        self.locals_data = {}
        self.instructions = []
        self.params = [cil.ParamNode('self')]

        self.visit(node.expr)

        self.instructions.append(cil.ReturnNode(None))

        self.code.append(cil.CodeNode( f'{self.current.name}_{node.id.value}',
            self.params, self.locals.values(), self.instructions))

    @visitor.when(AttributeNode)
    def visit(self, node):
        if node.expr:
            self.visit(node.expr)
    
    @visitor.when(StringNode)
    def visit(self, node):
        pass

    def add_local(self, name=None):
        if not name :
            name = f'local_{len(self.locals)}'     
        local = cil.LocalNode(name)
        self.locals[name] = local
        return local

    def add_data(self, value):
        try:
            return self.data[]