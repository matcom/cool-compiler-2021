from collections import defaultdict
from typing import List, Optional, Tuple

import coolpyler.ast.cil.base as cil
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.utils.visitor as visitor

VALUE_ATTR="value"
TRUE_VALUE="true"
FALSE_VALUE="false"

def contructor_for(name: str):
    return f"{name}_init"

def is_value(value):
    value = repr(value)
    return value.isnumeric() or value == "false" or value == "true"


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

        self.label = defaultdict(lambda: 0)

    def get_label(self, name: str):
        label = f"label_{name}_{self.label[name]}"
        self.label[name] += 1
        return label

    def get_param(self, name: str):
        return f"param_{name}"

    def get_local(self, name: Optional[str] = None):
        return f"local_{len(self.locals) if name is None else name}"

    def register_local(self, name:Optional[str]=None):
        local = self.get_local(name)
        self.locals.append(cil.LocalNode(local))
        if name is not None:
            self.named_locals[name] = local
        return local

    def register_data(self, name:str, value:str):
        data_id = f"data_{len(self.dotdata)}_{name}"
        self.dotdata.append(cil.DataNode(data_id, value))
        return data_id

    def register_new(self, type:str, *args, dest: Optional[str] = None):
        if dest is None:
            dest = self.register_local()
        for arg in args:
            self.instructions.append(cil.ArgNode(arg))
        self.instructions.append(cil.StaticCallNode(contructor_for(type), dest))
        return dest

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(type_checked.CoolProgramNode)
    def visit(self, node: type_checked.CoolProgramNode):
        main_type = "Main"
        main_method = "main"
        main_local = self.get_local("main")
        return_local = self.get_local("return")
        self.dotcode.append(
            cil.FunctionNode(
                "main",
                [],
                [cil.LocalNode(main_local), cil.LocalNode(return_local)],
                [
                    cil.StaticCallNode(contructor_for(main_type), main_local),
                    cil.ArgNode(main_local),
                    cil.StaticCallNode(f"{main_type}_{main_method}", return_local),
                    cil.ReturnNode(return_local),
                ],
            )
        )

        for cool_class in node.classes:
            dottype = self.visit(cool_class)
            self.dottypes.append(dottype)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(type_checked.CoolClassNode)
    def visit(self, node: type_checked.CoolClassNode):
        # TODO
        methods = node.type.all_methods()
        attributes = node.type.all_attributes()
        dottype = cil.TypeNode(node.type.name, attributes, methods)

        self_local = self.get_local("self")
        constructor_locals, constructor_instructions = (
            [cil.LocalNode(self_local)],
            [cil.AllocateNode(node.type.name, self_local)],
        )
        for feat in node.features:
            self.instructions, self.locals, self.named_locals = [], [], {}

            if isinstance(feat, type_checked.CoolAttrDeclNode):
                sid = self.visit(feat.body)
                self.instructions.append(
                    cil.SetAttrNode(self_local, feat.attr_info.name, sid)
                )
                constructor_locals.extend(self.locals)
                constructor_instructions.extend(self.instructions)

            if isinstance(feat, type_checked.CoolMethodDeclNode):
                param_list = [self.get_param("self")] + [
                    self.get_param(name) for name in feat.method_info.param_names
                ]
                self.params = set(param_list)
                sid = self.visit(feat.body)
                self.instructions.append(cil.ReturnNode(sid))
                self.dotcode.append(
                    cil.FunctionNode(
                        f"{node.type.name}_{feat.method_info.name}",
                        [cil.ParamNode(name) for name in param_list],
                        self.locals,
                        self.instructions,
                    )
                )

        self.dotcode.append(
            cil.FunctionNode(
                contructor_for(node.type.name),
                [],
                constructor_locals,
                constructor_instructions + [cil.ReturnNode(self_local)],
            )
        )
        return dottype

    @visitor.when(type_checked.CoolAssignNode)
    def visit(self, node: type_checked.CoolAssignNode) -> str:
        rhs_local = self.visit(node.expr)

        try:
            local_sid = self.named_locals[node.id]
            self.instructions.append(cil.AssignNode(local_sid, rhs_local))
            return local_sid
        except KeyError:
            local_sid = self.register_local(node.id)

        param_sid = self.get_param(node.id)
        if param_sid in self.params:
            self.instructions.append(cil.AssignNode(param_sid, rhs_local))
            return param_sid

        self.instructions.append(
            cil.SetAttrNode(self.get_param("self"), node.id, local_sid)
        )
        return local_sid


    @visitor.when(type_checked.CoolStaticDispatchNode)
    def visit(self, node: type_checked.CoolStaticDispatchNode) -> str:
        return_local = self.register_local()

        sid = self.visit(node.expr)
        # Translate all call arguments to cil
        args = [cil.ArgNode(sid)]
        for arg_expr in node.args:
            arg_sid = self.visit(arg_expr)
            args.append(cil.ArgNode(arg_sid))

        self.instructions.extend(args)
        self.instructions.append(
            cil.StaticCallNode(f"{node.static_type}_{node.id}", return_local)
        )
        return return_local

    @visitor.when(type_checked.CoolDispatchNode)
    def visit(self, node: type_checked.CoolDispatchNode) -> str:
        return_local = self.register_local()

        sid = self.visit(node.expr)
        # Translate all call arguments to cil
        args = [cil.ArgNode(sid)]
        for arg_expr in node.args:
            arg_sid = self.visit(arg_expr)
            args.append(cil.ArgNode(arg_sid))

        typeof_local = self.register_local()
        self.instructions.append(cil.TypeOfNode(sid, typeof_local))

        self.instructions.extend(args)
        self.instructions.append(
            cil.DynamicCallNode(typeof_local, node.id, return_local)
        )
        return return_local

    @visitor.when(type_checked.CoolIfThenElseNode)
    def visit(self, node: type_checked.CoolIfThenElseNode) -> str:
        return_local = self.register_local()

        then_label = self.get_label('then')
        else_label = self.get_label('else')
        continue_label = self.get_label('continue')

        # IF condition GOTO then_label
        cond_ret = self.visit(node.cond)
        self.instructions.append(cil.GotoIfNode(cond_ret, then_label))

        # GOTO else_label
        self.instructions.append(cil.GotoNode(else_label))

        # Label then_label
        self.instructions.append(cil.LabelNode(then_label))
        then_ret = self.visit(node.then_expr)
        self.instructions.append(cil.AssignNode(return_local, then_ret))
        self.instructions.append(cil.GotoNode(continue_label))

        # Label else_label
        self.instructions.append(cil.LabelNode(else_label))
        else_ret = self.visit(node.else_expr)
        self.instructions.append(cil.AssignNode(return_local, else_ret))

        # Label continue_label
        self.instructions.append(cil.LabelNode(continue_label))
        return return_local

    @visitor.when(type_checked.CoolWhileNode)
    def visit(self, node: type_checked.CoolWhileNode) -> str:
        while_label = self.get_label('while_label')
        loop_label = self.get_label('loop_label')
        pool_label = self.get_label('pool_label')

        # Label while
        self.instructions.append(cil.LabelNode(while_label))

        # IF condition GOTO loop
        while_ret = self.visit(node.cond)
        self.instructions.append(cil.GotoIfNode(while_ret, loop_label))

        # GOTO pool
        self.instructions.append(cil.GotoNode(pool_label))

        # Label loop
        self.instructions.append(cil.LabelNode(loop_label))
        self.visit(node.body)

        # GOTO while
        self.instructions.append(cil.GotoNode(while_label))

        # Label pool
        self.instructions.append(cil.LabelNode(pool_label))

        return "void"

    @visitor.when(type_checked.CoolBlockNode)
    def visit(self, node: type_checked.CoolBlockNode) -> str:
        for expr in node.expr_list:
            sid = self.visit(expr)
        return sid

    @visitor.when(type_checked.CoolLetInNode)
    def visit(self, node: type_checked.CoolLetInNode) -> str:
        for decl in node.decl_list:
            self.visit(decl)
        return self.visit(node.expr)

    @visitor.when(type_checked.CoolLetDeclNode)
    def visit(self, node: type_checked.CoolLetDeclNode) -> str:
        try:
            lhs_local = self.named_locals[node.id]
        except KeyError:
            lhs_local = self.register_local(node.id)
        rhs_local = self.visit(node.expr)
        self.instructions.append(cil.AssignNode(lhs_local, rhs_local))
        return lhs_local

    @visitor.when(type_checked.CoolCaseNode)
    def visit(self, node: type_checked.CoolCaseNode) -> str:
        raise NotImplementedError("CaseOf is not implemented")

    @visitor.when(type_checked.CoolCaseBranchNode)
    def visit(self, node: type_checked.CoolCaseBranchNode) -> str:
        return self.visit(node.expr)

    @visitor.when(type_checked.CoolNewNode)
    def visit(self, node: type_checked.CoolNewNode) -> str:
        return self.register_new(node.type.name)

    @visitor.when(type_checked.CoolParenthNode)
    def visit(self, node: type_checked.CoolParenthNode) -> str:
        return self.visit(node.expr)

    @visitor.when(type_checked.CoolTildeNode)
    def visit(self, node: type_checked.CoolTildeNode) -> str:
        ret_local = self.register_local()
        sid = self.visit(node.expr)
        self.instructions.append(cil.MinusNode(ret_local, 1, sid))
        return ret_local

    @visitor.when(type_checked.CoolNotNode)
    def visit(self, node: type_checked.CoolNotNode) -> str:
        ret_local = self.register_local()
        sid = self.visit(node.expr)
        self.instructions.extend([
            cil.MinusNode(ret_local, 1, sid),
        ])
        return self.register_new("Bool", ret_local)

    @visitor.when(type_checked.CoolIsVoidNode)
    def visit(self, node: type_checked.CoolIsVoidNode) -> str:
        expr = node.expr
        ret_local = self.register_local()
        self.instructions.append(cil.TypeOfNode(expr, ret_local))
        return self.register_new("Bool", ret_local)

    @visitor.when(type_checked.CoolLeqNode)
    def visit(self, node: type_checked.CoolLeqNode) -> str:
        left = self.visit(node.left_expr)
        if not is_value(left):
            left_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(left, VALUE_ATTR, left_value))
            left = left_value

        right = self.visit(node.right_expr)
        if not is_value(right):
            right_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(right, VALUE_ATTR, right_value))
            right = right_value

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, right, left))
        self.instructions.append(cil.PlusNode(cond_local, cond_local, 1))
        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolEqNode)
    def visit(self, node: type_checked.CoolEqNode) -> str:
        left = self.visit(node.left_expr)
        if not is_value(left):
            left_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(left, VALUE_ATTR, left_value))
            left = left_value

        right = self.visit(node.right_expr)
        if not is_value(right):
            right_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(right, VALUE_ATTR, right_value))
            right = right_value

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, left, right))
        self.instructions.append(cil.MinusNode(cond_local, 1, cond_local))

        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolLeNode)
    def visit(self, node: type_checked.CoolLeNode) -> str:
        left = self.visit(node.left_expr)
        if not is_value(left):
            left_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(left, VALUE_ATTR, left_value))
            left = left_value

        right = self.visit(node.right_expr)
        if not is_value(right):
            right_value = self.register_local()
            self.instructions.append(cil.GetAttrNode(right, VALUE_ATTR, right_value))
            right = right_value

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, right, left))
        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolPlusNode)
    def visit(self, node: type_checked.CoolPlusNode) -> str:
        left = self.visit(node.left_expr)
        right = self.visit(node.right_expr)
        ret_local = self.register_local()
        self.instructions.append(cil.PlusNode(ret_local, left, right))
        return ret_local

    @visitor.when(type_checked.CoolMinusNode)
    def visit(self, node: type_checked.CoolMinusNode) -> str:
        left = self.visit(node.left_expr)
        right = self.visit(node.right_expr)
        ret_local = self.register_local()
        self.instructions.append(cil.MinusNode(ret_local, left, right))
        return ret_local

    @visitor.when(type_checked.CoolMultNode)
    def visit(self, node: type_checked.CoolMultNode) -> str:
        left = self.visit(node.left_expr)
        right = self.visit(node.right_expr)
        ret_local = self.register_local()
        self.instructions.append(cil.StarNode(ret_local, left, right))
        return ret_local

    @visitor.when(type_checked.CoolDivNode)
    def visit(self, node: type_checked.CoolDivNode) -> str:
        left = self.visit(node.left_expr)
        right = self.visit(node.right_expr)
        ret_local = self.register_local()
        self.instructions.append(cil.DivNode(ret_local, left, right))
        return ret_local

    @visitor.when(type_checked.CoolIntNode)
    def visit(self, node: type_checked.CoolIntNode) -> str:
        return node.value

    @visitor.when(type_checked.CoolBoolNode)
    def visit(self, node: type_checked.CoolBoolNode) -> str:
        return node.value

    @visitor.when(type_checked.CoolStringNode)
    def visit(self, node: type_checked.CoolStringNode) -> str:
        data_id = self.register_data("string", repr(node.value))
        return_sid = self.register_local()
        self.instructions.append(cil.LoadNode(return_sid, data_id))
        return return_sid

    @visitor.when(type_checked.CoolVarNode)
    def visit(self, node: type_checked.CoolVarNode) -> str:
        try:
            return self.named_locals[node.value]
        except KeyError:
            pass

        param_sid = self.get_param(node.value)
        if param_sid in self.params:
            return param_sid

        local_sid = self.register_local(node.value)
        self.instructions.append(
            cil.GetAttrNode(self.get_param("self"), node.value, local_sid)
        )
        return local_sid

# vim: foldmethod=indent foldnestmax=2 foldlevel=1
