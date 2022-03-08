import itertools as itt

import app.shared.visitor as visitor
import app.cil.ast_cil as cil
from app.mips import mips
from random import choice
from collections import defaultdict


class CILToMIPSVisitor:
    def __init__(self):
        self._types = {}
        self._data_section = {}
        self._functions = {}
        self._actual_function = None
        self._name_func_map = {}
        self._pushed_args = 0
        self._labels_map = {}

    def get_var_location(self, name):
        return self._actual_function.get_var_location(name)

    def register_function(self, name, function):
        self._functions[name] = function

    def init_function(self, function):
        self._actual_function = function
        self._labels_map = {}

    def finish_functions(self):
        self._actual_function = None

    def push_arg(self):
        self._pushed_args += 1

    def clean_pushed_args(self):
        self._pushed_args = 0

    def in_entry_function(self):
        return self._actual_function.label == 'main'

    def register_label(self, cil_label, mips_label):
        self._labels_map[cil_label] = mips_label

    def get_mips_label(self, label):
        return self._labels_map[label]

    @visitor.on('node')
    def collect_labels_in_func(self, node):
        pass

    @visitor.when(cil.LabelNode)
    def collect_labels_in_func(self, node):
        self.register_label(node.label, f'{self._actual_function.label}_{node.label}')


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil.InstructionNode)
    def visit(self, node):
        print(type(node))

    @visitor.when(cil.ProgramNode)
    def visit(self, node:cil.ProgramNode):
        return cil.ProgramNode.visit(node,self,mips)

    @visitor.when(cil.TypeNode)
    def visit(self, node):
        cil.TypeNode.visit(node,self,mips)

    @visitor.when(cil.DataNode)
    def visit(self, node):
        cil.DataNode.visit(node,self,mips)

    @visitor.when(cil.FunctionNode)
    def visit(self, node:cil.FunctionNode):
        cil.FunctionNode.visit(node,self,mips)

    @visitor.when(cil.ArgNode)
    def visit(self, node):
        return cil.ArgNode.visit(node,self,mips)

    @visitor.when(cil.StaticCallNode)
    def visit(self, node):
        return cil.StaticCallNode.visit(node,self,mips)

    @visitor.when(cil.AssignNode)
    def visit(self, node):
        return cil.AssignNode.visit(node,self,mips)

    @visitor.when(cil.AllocateNode)
    def visit(self, node):
        return cil.AllocateNode.visit(node,self,mips)

    @visitor.when(cil.ReturnNode)
    def visit(self, node):
        return cil.ReturnNode.visit(node,self,mips)

    @visitor.when(cil.LoadNode)
    def visit(self, node):
        return cil.LoadNode.visit(node,self,mips)

    @visitor.when(cil.PrintIntNode)
    def visit(self, node):
        return cil.PrintIntNode.visit(node,self,mips)

    @visitor.when(cil.PrintStrNode)
    def visit(self, node):
        return cil.PrintStrNode.visit(node,self,mips)

    @visitor.when(cil.TypeNameNode)
    def visit(self, node):
        return cil.TypeNameNode.visit(node,self,mips)

    @visitor.when(cil.ExitNode)
    def visit(self, node):
        return cil.ExitNode.visit(node,self,mips)

    @visitor.when(cil.GetAttribNode)
    def visit(self, node):
        return cil.GetAttribNode.visit(node,self,mips)

    @visitor.when(cil.SetAttribNode)
    def visit(self, node):
        return cil.SetAttribNode.visit(node,self,mips)

    @visitor.when(cil.CopyNode)
    def visit(self, node):
        return cil.CopyNode.visit(node,self,mips)

    @visitor.when(cil.EqualNode)
    def visit(self, node):
        return cil.EqualNode.visit(node,self,mips)

    @visitor.when(cil.EqualStrNode)
    def visit(self, node):
        return cil.EqualStrNode.visit(node,self,mips)

    @visitor.when(cil.LabelNode)
    def visit(self, node):
        return cil.LabelNode.visit(node,self,mips)

    @visitor.when(cil.GotoIfNode)
    def visit(self, node):
        return cil.GotoIfNode.visit(node,self,mips)

    @visitor.when(cil.GotoNode)
    def visit(self, node):
        return cil.GotoNode.visit(node,self,mips)

    @visitor.when(cil.TypeOfNode)
    def visit(self, node):
        return cil.TypeOfNode.visit(node,self,mips)


    @visitor.when(cil.DynamicCallNode)
    def visit(self, node):
        return cil.DynamicCallNode.visit(node,self,mips)


    @visitor.when(cil.ErrorNode)
    def visit(self, node):
        return cil.ErrorNode.visit(node,self,mips)

    @visitor.when(cil.NameNode)
    def visit(self, node):
        return cil.NameNode.visit(node,self,mips)

    @visitor.when(cil.PlusNode)
    def visit(self, node):
        return cil.PlusNode.visit(node,self,mips)
    @visitor.when(cil.MinusNode)
    def visit(self, node):
        return cil.MinusNode.visit(node,self,mips)

    @visitor.when(cil.StarNode)
    def visit(self, node):
        return cil.StarNode.visit(node,self,mips)

    @visitor.when(cil.DivNode)
    def visit(self, node):
        return cil.DivNode.visit(node,self,mips)

    @visitor.when(cil.ComplementNode)
    def visit(self, node):
        return cil.ComplementNode.visit(node,self,mips)

    @visitor.when(cil.LessEqualNode)
    def visit(self, node):
        return cil.LessEqualNode.visit(node,self,mips)

    @visitor.when(cil.LessNode)
    def visit(self, node):
        return cil.LessNode.visit(node,self,mips)

    @visitor.when(cil.ReadStrNode)
    def visit(self, node):
        return cil.ReadStrNode.visit(node,self,mips)

    @visitor.when(cil.LengthNode)
    def visit(self, node):
        return cil.LengthNode.visit(node,self,mips)

    @visitor.when(cil.ReadIntNode)
    def visit(self, node):
        return cil.ReadIntNode.visit(node,self,mips)

    @visitor.when(cil.ConcatNode)
    def visit(self, node):
        return cil.ConcatNode.visit(node,self,mips)

    @visitor.when(cil.SubstringNode)
    def visit(self, node):
        return cil.SubstringNode.visit(node,self,mips)

