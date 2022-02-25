
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
                        self.errors.append(f"({dec_node.line_father},{dec_node.column_father}) - SemanticError: Basic type as parent")
                    self.context.get_type(dec_node.id, dec_node.line).set_parent(self.context.get_type(dec_node.parent,dec_node.line),node.line)
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - SemanticError: " + e)
        
        cycles = self.context.circular_dependency()
        for cycle in cycles:
            self.errors.append(f"({cycle[0][0].line},{cycle[0][0].column}) - SemanticError: Class {cycle[0][0]}, is involved in an inheritance cycle.")
            return

        for decl in classes:
            self.current_type = self.context.get_type(decl.id)
            for feature in decl.features:
                self.visit(feature)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        try:
            self.current_type = self.context.create_type(node.id, node.type_line)
        except SemanticError as e:
            self.errors.append(f"({node.type_line},{node.type_column}) - SemanticError: " + str(e))
            return

    @visitor.when(AttrDeclarationNode)
    def visit(self, node):        
        try:
            attr_type = SELF_TYPE() if node.type == "SELF_TYPE" else self.context.get_type(node.type,-1) #change -1 for line number
            if node.id == "self":
                self.errors.append(f"({node.line},{node.column}) - SemanticError: Trying to assign value to self")
                raise SemanticError('', -1)  #change -1 for line number
            self.current_type.define_attribute(node.id, attr_type, -1) #change -1 for line number
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        arg_names = [param[0] for param in node.params]
        arg_types = []
        for param in node.params:
            try:
                arg_types.append(self.context.get_type(param[1],node.line) )
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
                arg_types.append(ErrorType())
        try:
            ret_type = SELF_TYPE() if node.type =="SELF_TYPE" else self.context.get_type(node.type,node.line)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
            ret_type = ErrorType()
        try:
            self.current_type.define_method(node.id, arg_names, arg_types, ret_type, node.line)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))