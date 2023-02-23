import sys
sys.path.append('../')
from ..ast import *
from . import visitor
import queue

def sort_types(types):
        q = queue.deque()
        result = []
        for tp in types:
            if types[tp].parent is None:
                if tp != "Object":
                    types[tp].set_parent(types["Object"])

        q.append("Object")
        while len(q) != 0:
            tp = q.popleft()
            result.append(tp)
            for son in types[tp].sons:
                q.append(son.name)
        return result 

class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        nodec={ def_class.id:def_class for def_class in node.declarations}
        sorted_types = sort_types(self.context.types)
        for stypes in sorted_types:
            if stypes in nodec:
                self.visit(nodec[stypes])

    @visitor.when(ProgramNode)
    def visit(self, node):
        nodec={ def_class.id:def_class for def_class in node.declarations}
        sorted_types = sort_types(self.context.types)
        for stypes in sorted_types:
            if stypes in nodec:
                self.visit(nodec[stypes])

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id,-1) #change -1 for line number
        for feature in node.features:
            self.visit(feature)