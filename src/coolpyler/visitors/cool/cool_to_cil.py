from typing import List, Optional, Tuple

import coolpyler.ast.cil.base as cil
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.utils.visitor as visitor


def contructor_for(name: str):
    return f"{name}_init"


class CoolToCilVisitor(object):
    def __init__(self, errors=None):
        if errors is None:
            errors = []
        self.errors = errors

        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.locals = []
        self.named_locals = {}
        self.instructions = []

        self.params = {}

    def get_data(self):
        return f"data_{len(self.dotdata)}"

    def get_param(self, name: str):
        return f"param_{name}"

    def get_local(self, name: Optional[str] = None):
        return f"local_{len(self.locals) if name is None else name}"

    @visitor.on("node")
    def visit(self, node: type_checked.CoolAstNode) -> cil.CILAstNode:  # type: ignore
        pass

    @visitor.when(type_checked.CoolProgramNode)
    def visit(self, node: type_checked.CoolProgramNode):  # type: ignore

        for cool_class in node.classes:
            dottype = self.visit(cool_class)
            self.dottypes.append(dottype)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(type_checked.CoolClassNode)
    def visit(self, node: type_checked.CoolClassNode):  # type: ignore
        # TODO
        methods = node.type.all_methods()
        attributes = node.type.all_attributes()
        dottype = cil.TypeNode(node.type, attributes, methods)

        constructor_locals, constructor_instructions = [], []
        for feat in node.features:
            self.locals, self.named_locals = [], {}
            self.visit(feat)
            if isinstance(feat, type_checked.CoolAttrDeclNode):
                constructor_locals.extend(self.locals)
                constructor_instructions.extend(self.instructions)
            if isinstance(feat, type_checked.CoolMethodDeclNode):
                params = [cil.ParamNode(self.get_param("self"))] + [
                    cil.ParamNode(self.get_param(name))
                    for name in feat.method_info.param_names
                ]
                self.dotcode.append(
                    cil.FunctionNode(
                        feat.method_info.name, params, self.locals, self.instructions
                    )
                )

        self.dotcode.append(
            cil.FunctionNode(
                contructor_for(node.type.name),
                cil.ParamNode(self.get_param("self")),
                constructor_locals,
                constructor_instructions,
            )
        )
        return dottype

    @visitor.when(type_checked.CoolAttrDeclNode)
    def visit(self, node: type_checked.CoolAttrDeclNode) -> str:  # type: ignore
        sid = self.visit(node.body)
        self.instructions.append(cil.SetAttrNode(self.get_param("self"), node.attr_info.name, sid))
        return sid

    @visitor.when(type_checked.CoolMethodDeclNode)
    def visit(self, feat: type_checked.CoolMethodDeclNode) -> str:  # type: ignore
        return self.visit(feat.body)

    @visitor.when(type_checked.CoolAssignNode)
    def visit(self, node: type_checked.CoolAssignNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolStaticDispatchNode)
    def visit(self, node: type_checked.CoolStaticDispatchNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolDispatchNode)
    def visit(self, node: type_checked.CoolDispatchNode) -> str:  # type: ignore
        return_local = self.get_local()
        self.locals.append(cil.LocalNode(return_local))

        sid = self.visit(node.expr)
        # Translate all call arguments to cil
        args = [cil.ArgNode(sid)]
        for arg_expr in node.args:
            arg_sid = self.visit(arg_expr)
            args.append(cil.ArgNode(arg_sid))

        self.instructions.append(cil.DynamicCallNode(node.expr.type, node.id, sid))
        return return_local

    @visitor.when(type_checked.CoolIfThenElseNode)
    def visit(self, node: type_checked.CoolIfThenElseNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolWhileNode)
    def visit(self, node: type_checked.CoolWhileNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolBlockNode)
    def visit(self, node: type_checked.CoolBlockNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolLetInNode)
    def visit(self, node: type_checked.CoolLetInNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolLetDeclNode)
    def visit(self, node: type_checked.CoolLetDeclNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolCaseNode)
    def visit(self, node: type_checked.CoolCaseNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolCaseBranchNode)
    def visit(self, node: type_checked.CoolCaseBranchNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolNewNode)
    def visit(self, node: type_checked.CoolNewNode) -> str:  # type: ignore
        # TODO
        pass

    @visitor.when(type_checked.CoolParenthNode)
    def visit(self, node: type_checked.CoolParenthNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolTildeNode)
    def visit(self, node: type_checked.CoolTildeNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolNotNode)
    def visit(self, node: type_checked.CoolNotNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolIsVoidNode)
    def visit(self, node: type_checked.CoolIsVoidNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolLeqNode)
    def visit(self, node: type_checked.CoolLeqNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolEqNode)
    def visit(self, node: type_checked.CoolEqNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolLeNode)
    def visit(self, node: type_checked.CoolLeNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolPlusNode)
    def visit(self, node: type_checked.CoolPlusNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolMinusNode)
    def visit(self, node: type_checked.CoolMinusNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolMultNode)
    def visit(self, node: type_checked.CoolMultNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolDivNode)
    def visit(self, node: type_checked.CoolDivNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolIntNode)
    def visit(self, node: type_checked.CoolIntNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolBoolNode)
    def visit(self, node: type_checked.CoolBoolNode) -> str:  # type: ignore
        pass

    @visitor.when(type_checked.CoolStringNode)
    def visit(self, node: type_checked.CoolStringNode) -> str:  # type: ignore
        data_id = self.get_data()
        return_sid = self.get_local()

        self.dotdata.append(cil.DataNode(data_id, node.value))
        self.locals.append(cil.LocalNode(return_sid))

        self.instructions.append(cil.LoadNode(return_sid, data_id))
        return return_sid

    @visitor.when(type_checked.CoolVarNode)
    def visit(self, node: type_checked.CoolVarNode) -> str:  # type: ignore
        local_sid = self.get_local(node.value)
        if local_sid in self.named_locals:
            return local_sid

        param_sid = self.get_param(node.value)
        if param_sid in self.params:
            return param_sid

        self.instructions.append(
            cil.GetAttrNode(self.get_param("self"), node.value, local_sid)
        )
        return local_sid
