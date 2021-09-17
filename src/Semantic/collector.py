import Utils.visitor as visitor

from Utils.token import Token
from Utils.context import Context
from Utils.errors import SemanticError, TypeException
from Parser.ast import ProgramNode, ClassNode

class Type_Collector:
    def __init__(self, errors):
        self.type_level = {}
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()

        for def_class in node.class_list:
            self.visit(def_class)
      
        node.class_list.sort(key = lambda node: self.get_type_level(node.type))
        return self.context

    @visitor.when(ClassNode)
    def visit(self, node):
        try:
            self.context.create_type(node.type.value)
            self.type_level[node.type.value] = node.parent
        except TypeException as error:
            self.errors.append(SemanticError(node.type.line, node.type.column, error))

    def get_type_level(self, type):
            try:
                parent = self.type_level[type.value]
            except KeyError:
                return 0
            
            if parent == 0:
                self.errors.append(SemanticError(type.line, type.column, f'Class {type.value}, or an ancestor of {type.value}, is involved in an inheritance cycle.'))
            elif not isinstance(parent, int):
                self.type_level[type.value] = 0 if parent else 1
                if isinstance(parent, Token):
                    self.type_level[type.value] = self.get_type_level(parent) + 1
            
            return self.type_level[type.value]