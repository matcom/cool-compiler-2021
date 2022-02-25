from collections import defaultdict
from typing import List, Optional, Tuple

import coolpyler.ast.cil.base as cil
import coolpyler.ast.cool.type_checked as type_checked
import coolpyler.utils.visitor as visitor


class CoolToCilVisitor(object):
    def __init__(self):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.type = None
        self.params = None
        self.locals = None
        self.instructions = None

        self.attrs = None
        self.methods = None

        self.label = defaultdict(lambda: 0)

    def reset_state(self):
        self.params, self.locals, self.instructions = [], [], []

    def get_attr_id(self, type: str, name: str):
        attr_id, _ = self.attrs[type][name]
        return attr_id

    def get_method_id(self, type: str, name: str):
        method_id, _ = self.methods[type][name]
        return method_id

    def get_func_id(self, type: str, name: str):
        return f"{type}_{name}"

    def get_label(self, name: str):
        label = f"label_{name}_{self.label[name]}"
        self.label[name] += 1
        return label

    def get_param(self, name: str):
        return f"param_{name}"

    def get_local(self, name: Optional[str] = None):
        return f"local_{len(self.locals) if name is None else name}"

    def register_param(self, name: str):
        param = self.get_param(name)
        self.params.append(cil.ParamNode(param))
        return param

    def register_local(self, name: Optional[str] = None):
        local = self.get_local(name)
        self.locals.append(cil.LocalNode(local))
        return local

    def register_data(self, name: str, value: str):
        data_id = f"data_{len(self.dotdata)}_{name}"
        self.dotdata.append(cil.DataNode(data_id, value))
        return_sid = self.register_local()
        self.instructions.append(cil.LoadNode(return_sid, data_id))
        return return_sid

    def register_num(self, name: Optional[str], value: int):
        return_sid = self.register_local(name)
        self.instructions.append(cil.LoadNode(return_sid, value))
        return return_sid

    def register_new(self, type: str, *args, dest: Optional[str] = None):
        if dest is None:
            dest = self.register_local()
        for arg in args:
            self.instructions.append(cil.ArgNode(arg))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id(type, "init"), dest)
        )
        return dest

    def register_builtins(self):
        self.type = "Object"

        self.methods[self.type] = {
            m: (i, self.type)
            for i, m in enumerate(["copy", "type_name", "abort"])
        }

        self.reset_state()
        str_param = self.register_param("str")
        self.instructions.append(cil.PrintNode(str_param, True))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Object", "out_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.type = "IO"

        self.methods[self.type] = {
            m: (i, self.type)
            for i, m in enumerate(["out_string", "out_int", "in_string", "in_int"])
        }

        self.reset_state()
        str_param = self.register_param("str")
        self.instructions.append(cil.PrintNode(str_param, True))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.reset_state()
        int_param = self.register_param("int")
        self.instructions.append(cil.PrintNode(int_param, False))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.reset_state()
        str_local = self.register_local("str")
        self.instructions.append(cil.ReadNode(str_local, True))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.reset_state()
        int_local = self.register_local("int")
        self.instructions.append(cil.ReadNode(int_local, False))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.dottypes.append(
            cil.TypeNode(
                self.type,
                [],
                [
                    self.get_func_id(htype, method)
                    for method, (_, htype) in self.methods[self.type].items()
                ],
            )
        )

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(type_checked.CoolProgramNode)
    def visit(self, node: type_checked.CoolProgramNode):
        self.attrs, self.methods = dict(), dict()
        for cclass in node.classes:
            type = cclass.type
            self.attrs[cclass.type.name] = {
                attr.name: (i, htype.name)
                for i, (attr, htype) in enumerate(type.all_attributes())
            }
            self.methods[cclass.type.name] = {
                method.name: (i, htype.name)
                for i, (method, htype) in enumerate(type.all_methods())
            }

        self.reset_state()

        self.register_builtins()

        main_instance = self.register_new("Main")
        self.instructions.append(cil.ArgNode(main_instance))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id("Main", "main"), self.register_local())
        )
        self.instructions.append(cil.ExitNode(0))
        self.dotcode.append(
            cil.FunctionNode("main", self.params, self.locals, self.instructions)
        )

        for cool_class in node.classes:
            dottype = self.visit(cool_class)
            self.dottypes.append(dottype)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(type_checked.CoolClassNode)
    def visit(self, node: type_checked.CoolClassNode):
        self.type = node.type.name
        self.reset_state()
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode(node.type.name, self_local))
        for attr, (i, htype) in self.attrs[node.type.name].items():
            attr_local = self.get_local(attr)
            self.instructions.append(
                cil.StaticCallNode(self.get_func_id(htype, f"{attr}_init"), attr_local,)
            )
            self.instructions.append(cil.SetAttrNode(self_local, i, attr_local))
        self.instructions.append(cil.ReturnNode(self_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(node.type.name, "init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        for feat in node.features:
            function = self.visit(feat)
            self.dotcode.append(function)

        return cil.TypeNode(
            node.type.name,
            list(self.attrs[node.type.name].keys()),
            [
                self.get_func_id(htype, method)
                for method, (_, htype) in self.methods[node.type.name].items()
            ],
        )

    @visitor.when(type_checked.CoolAttrDeclNode)
    def visit(self, node: type_checked.CoolAttrDeclNode) -> cil.FunctionNode:
        self.reset_state()
        sid = self.visit(node.body)
        self.instructions.append(cil.ReturnNode(sid))
        return cil.FunctionNode(
            self.get_func_id(self.type, node.attr_info.name),
            self.params,
            self.locals,
            self.instructions,
        )

    @visitor.when(type_checked.CoolMethodDeclNode)
    def visit(self, node: type_checked.CoolMethodDeclNode) -> cil.FunctionNode:
        self.reset_state()
        self.register_param("self")
        for param in node.method_info.param_names:
            self.register_param(param)
        sid = self.visit(node.body)
        self.instructions.append(cil.ReturnNode(sid))
        return cil.FunctionNode(
            self.get_func_id(self.type, node.method_info.name),
            self.params,
            self.locals,
            self.instructions,
        )

    @visitor.when(type_checked.CoolAssignNode)
    def visit(self, node: type_checked.CoolAssignNode) -> str:
        rhs_local = self.visit(node.expr)

        local_sid = self.get_local(node.id)
        if any(local_sid == l.name for l in self.locals):
            self.instructions.append(cil.AssignNode(local_sid, rhs_local))
            return local_sid

        local_sid = self.register_local(node.id)

        param_sid = self.get_param(node.id)
        if any(param_sid == p.name for p in self.params):
            self.instructions.append(cil.AssignNode(param_sid, rhs_local))
            return param_sid

        attr_id = self.get_attr_id(node.type.name, node.id)
        self.instructions.append(
            cil.SetAttrNode(self.get_param("self"), attr_id, local_sid)
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
            cil.StaticCallNode(
                self.get_func_id(node.static_type, node.id), return_local
            )
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
        method_id = self.get_method_id(node.expr.type.name, node.id)
        self.instructions.append(
            cil.DynamicCallNode(typeof_local, method_id, return_local)
        )
        return return_local

    @visitor.when(type_checked.CoolIfThenElseNode)
    def visit(self, node: type_checked.CoolIfThenElseNode) -> str:
        return_local = self.register_local()

        then_label = self.get_label("then")
        else_label = self.get_label("else")
        continue_label = self.get_label("continue")

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
        while_label = self.get_label("while_label")
        loop_label = self.get_label("loop_label")
        pool_label = self.get_label("pool_label")

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
        lhs_local = self.get_local(node.id)
        if not any(lhs_local == l.name for l in self.locals):
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
        self.instructions.append(cil.MinusNode(ret_local, self.register_num(1), sid))
        return ret_local

    @visitor.when(type_checked.CoolNotNode)
    def visit(self, node: type_checked.CoolNotNode) -> str:
        ret_local = self.register_local()
        sid = self.visit(node.expr)
        self.instructions.append(cil.MinusNode(ret_local, self.register_num(1), sid))
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
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, right_value, left_value))
        self.instructions.append(
            cil.PlusNode(cond_local, cond_local, self.register_num(1))
        )
        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolEqNode)
    def visit(self, node: type_checked.CoolEqNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, left_value, right_value))
        self.instructions.append(
            cil.MinusNode(cond_local, self.register_num(1), cond_local)
        )

        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolLeNode)
    def visit(self, node: type_checked.CoolLeNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        cond_local = self.register_local()
        self.instructions.append(cil.MinusNode(cond_local, right_value, left_value))
        return self.register_new("Bool", cond_local)

    @visitor.when(type_checked.CoolPlusNode)
    def visit(self, node: type_checked.CoolPlusNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        ret_local = self.register_local()
        self.instructions.append(cil.PlusNode(ret_local, left_value, right_value))
        return ret_local

    @visitor.when(type_checked.CoolMinusNode)
    def visit(self, node: type_checked.CoolMinusNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        ret_local = self.register_local()
        self.instructions.append(cil.MinusNode(ret_local, left_value, right_value))
        return ret_local

    @visitor.when(type_checked.CoolMultNode)
    def visit(self, node: type_checked.CoolMultNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        ret_local = self.register_local()
        self.instructions.append(cil.StarNode(ret_local, left_value, right_value))
        return ret_local

    @visitor.when(type_checked.CoolDivNode)
    def visit(self, node: type_checked.CoolDivNode) -> str:
        left = self.visit(node.left_expr)
        left_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(left, 0, left_value))

        right = self.visit(node.right_expr)
        right_value = self.register_local()
        self.instructions.append(cil.GetAttrNode(right, 0, right_value))

        ret_local = self.register_local()
        self.instructions.append(cil.DivNode(ret_local, left_value, right_value))
        return ret_local

    @visitor.when(type_checked.CoolIntNode)
    def visit(self, node: type_checked.CoolIntNode) -> str:
        literal = self.register_num("", int(node.value))
        return self.register_new("Int", literal)

    @visitor.when(type_checked.CoolBoolNode)
    def visit(self, node: type_checked.CoolBoolNode) -> str:
        literal = self.register_num("", 1 if node.value == "true" else 0)
        return self.register_new("Bool", literal)

    @visitor.when(type_checked.CoolStringNode)
    def visit(self, node: type_checked.CoolStringNode) -> str:
        literal = self.register_data("string", node.value)
        return self.register_new("String", literal)

    @visitor.when(type_checked.CoolVarNode)
    def visit(self, node: type_checked.CoolVarNode) -> str:
        local_sid = self.get_local(node.value)
        if any(local_sid == l.name for l in self.locals):
            return local_sid

        local_sid = self.register_local(node.value)

        param_sid = self.get_param(node.value)
        if any(param_sid == p.name for p in self.params):
            return param_sid

        local_sid = self.register_local(node.value)
        attr_id = self.get_attr_id(node.type.name, node.value)
        self.instructions.append(
            cil.GetAttrNode(self.get_param("self"), attr_id, local_sid)
        )
        return local_sid
