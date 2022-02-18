from CIL.builder import *
from Tools import visitor

from Parser.ast import * 
import CIL.ast as cil

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
        self.code = builder_basic_functions(self)
        self.types = builder_types(self.context)

        for def_class in node.class_list:
            self.visit(def_class)

        return cil.ProgramNode(self.types, self.data.values(), self.code)
    
    @visitor.when(ClassNode)
    def visit(self, node):
        self.current_type = self.context.types[node.type.value]       
        for feature in node.feature_list:
            self.visit(feature)

    @visitor.when(IntegerNode)
    def visit(self, node):
        self.computed_value = node.lexer.value