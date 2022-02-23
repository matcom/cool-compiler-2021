import itertools

import coolpyler.ast.cil.base as cil
import coolpyler.ast.mips.base as mips
import coolpyler.utils.visitor as visitor


class CilToMIPS:
    def __init__(self):
        self.types_table = []
        self.location = dict()

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cil.ProgramNode)
    def visit(self, node: cil.ProgramNode):
        pass

    @visitor.when(cil.TypeNode)
    def visit(self, node: cil.TypeNode):
        pass

    @visit.when(cil.FunctionNode)
    def visit(self, node: cil.FunctionNode):
        pass

    @visit.when(cil.DataNode)
    def visit(self, node: cil.DataNode):
        pass

    @visit.when(cil.ParamNode)
    def visit(self, node: cil.ParamNode):
        pass

    @visit.when(cil.LocalNode)
    def visit(self, node: cil.LocalNode):
        pass

    @visit.when(cil.PlusNode)
    def visit(self, node: cil.PlusNode):
        pass

    @visit.when(cil.MinusNode)
    def visit(self, node: cil.MinusNode):
        pass

    @visit.when(cil.StarNode)
    def visit(self, node: cil.StarNode):
        pass

    @visit.when(cil.DivNode)
    def visit(self, node: cil.DivNode):
        pass

    @visit.when(cil.GetAttrNode)
    def visit(self, node: cil.GetAttrNode):
        pass

    @visit.when(cil.SetAttrNode)
    def visit(self, node: cil.SetAttrNode):
        pass

    @visit.when(cil.GetIndexNode)
    def visit(self, node: cil.GetIndexNode):
        pass

    @visit.when(cil.SetIndexNode)
    def visit(self, node: cil.SetIndexNode):
        pass

    @visit.when(cil.AllocateNode)
    def visit(self, node: cil.AllocateNode):
        pass

    @visit.when(cil.TypeOfNode)
    def visit(self, node: cil.TypeOfNode):
        pass

    @visit.when(cil.LabelNode)
    def visit(self, node: cil.LabelNode):
        pass

    @visit.when(cil.GotoNode)
    def visit(self, node: cil.GotoNode):
        pass

    @visit.when(cil.GotoIfNode)
    def visit(self, node: cil.GotoIfNode):
        pass

    @visit.when(cil.StaticCallNode)
    def visit(self, node: cil.StaticCallNode):
        pass

    @visit.when(cil.DynamicCallNode)
    def visit(self, node: cil.DynamicCallNode):
        pass

    @visit.when(cil.ArgNode)
    def visit(self, node: cil.ArgNode):
        pass

    @visit.when(cil.ReturnNode)
    def visit(self, node: cil.ReturnNode):
        pass

    @visit.when(cil.LoadNode)
    def visit(self, node: cil.LoadNode):
        pass

    @visit.when(cil.LengthNode)
    def visit(self, node: cil.LengthNode):
        pass

    @visit.when(cil.ConcatNode)
    def visit(self, node: cil.ConcatNode):
        pass

    @visit.when(cil.PrefixNode)
    def visit(self, node: cil.PrefixNode):
        pass

    @visit.when(cil.SubstringNode)
    def visit(self, node: cil.SubstringNode):
        pass

    @visit.when(cil.ToStrNode)
    def visit(self, node: cil.ToStrNode):
        pass

    @visit.when(cil.ReadNode)
    def visit(self, node: cil.ReadNode):
        pass

    @visit.when(cil.PrintNode)
    def visit(self, node: cil.PrintNode):
        pass
