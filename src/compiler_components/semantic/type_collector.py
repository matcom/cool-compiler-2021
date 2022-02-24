
import sys, os
sys.path.append('../')

from . import visitor
from ..ast import *
import queue
from .structures import *


class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        classes = []
        for decl in node.declarations:
            self.visit(decl)
            classes.append(decl)
        for dec_node in node.declarations:
            try:
                if dec_node.parent is not None:
                    if dec_node.parent in ["String","Int","Bool"]:
                        self.errors.append(SemanticError("Basic type as parent", dec_node.line))
                    self.context.get_type(dec_node.id, dec_node.line).set_parent(self.context.get_type(dec_node.parent,dec_node.line),node.line)
            except SemanticError as e:
                self.errors.append(e)
        
        cycles = self.context.circular_dependency()
        for cycle in cycles:
            self.errors.append(SemanticError(f"Class {cycle[0][0]},  is involved in an inheritance cycle.",cycle[0][1]))
            return

        for decl in classes:
            for feature in decl.features:
                self.visit(feature)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.create_type(node.id,node.line)
        except SemanticError as e:
            self.errors.append(e)
            return
        #for feature in node.features:
            #self.visit(feature)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):        
        try:
            attr_type = SELF_TYPE() if node.type == "SELF_TYPE" else self.context.get_type(node.type,-1) #change -1 for line number
            if node.id == "self":
                    raise SemanticError('Trying to assign value to self' ,-1)  #change -1 for line number
            
            self.current_type.define_attribute(node.id, attr_type, -1) #change -1 for line number
        except SemanticError as e:
            self.errors.append(e)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names = [param[0] for param in node.params]
        arg_types = []
        for param in node.params:
            try:
                arg_types.append(self.context.get_type(param[1],node.line) )
            except SemanticError as e:
                self.errors.append(e)
                arg_types.append(ErrorType())
        try:
            ret_type = SELF_TYPE() if node.type =="SELF_TYPE" else self.context.get_type(node.type,node.line)
        except SemanticError as e:
            self.errors.append(e)
            ret_type = ErrorType()
        try:
            self.current_type.define_method(node.id, arg_names, arg_types, ret_type, node.line)
        except SemanticError as e:
            self.errors.append(e)