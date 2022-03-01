from collections import defaultdict
from functools import cmp_to_key
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

    def register_num(self, value: int, name: Optional[str] = None):
        return_sid = self.register_local(name)
        self.instructions.append(cil.LoadNode(return_sid, value))
        return return_sid

    def register_new(self, type: str, *args, dest: Optional[str] = None):
        if dest is None:
            dest = self.register_local()

        if len(args) == 0:
            if type == "Int" or type == "Bool":
                self.instructions.append(cil.ArgNode(self.register_num(0)))
            elif type == "String":
                self.instructions.append(cil.ArgNode(self.register_data("")))

        for arg in args:
            self.instructions.append(cil.ArgNode(arg))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id(type, "__init"), dest)
        )
        return dest

    def register_object_abort(self):
        self.reset_state()
        self.register_param("self")
        data = self.register_data("abort_msg", '"Program Halted!"')
        instance = self.register_new("String", data)
        self.instructions.append(cil.PrintNode(instance, True))
        self.instructions.append(cil.ExitNode(1))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Object", "abort"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_type_name(self, type: str):
        self.reset_state()
        self.register_param("self")
        type_name = self.register_data(f"type_name_{type}", f'"{type}"')
        ret_local = self.register_new("String", type_name)
        self.instructions.append(cil.ReturnNode(ret_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(type, "type_name"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_copy(self, type: str):
        self.reset_state()
        self_param = self.register_param("self")
        copy_local = self.register_local("copy")
        self.instructions.append(cil.AllocateNode(type, copy_local))
        for attr, _ in self.attrs[type].values():
            attr_copy_local = self.register_local("attr_copy")
            self.instructions.append(cil.GetAttrNode(self_param, attr, attr_copy_local))
            self.instructions.append(cil.SetAttrNode(copy_local, attr, attr_copy_local))

        self.instructions.append(cil.ReturnNode(copy_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(type, "copy"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io_out_string(self):
        self.reset_state()
        str_param = self.register_param("str")
        self_param = self.register_param("self")

        self.instructions.append(cil.PrintNode(str_param, True))
        self.instructions.append(cil.ReturnNode(self_param))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io_out_int(self):
        self.reset_state()
        int_param = self.register_param("int")
        self_param = self.register_param("self")

        self.instructions.append(cil.PrintNode(int_param, False))
        self.instructions.append(cil.ReturnNode(self_param))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "out_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io_in_string(self):
        self.reset_state()
        self.register_param("self")
        str_local = self.register_local("str")
        self.instructions.append(cil.ReadNode(str_local, True))
        self.instructions.append(cil.ReturnNode(str_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_string"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_io_in_int(self):
        self.reset_state()
        self.register_param("self")
        int_local = self.register_local("int")
        self.instructions.append(cil.ReadNode(int_local, False))
        self.instructions.append(cil.ReturnNode(int_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("IO", "in_int"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string_length(self):
        self.reset_state()
        self_param = self.register_param("self")
        length_local = self.register_local("length")
        self.instructions.append(cil.LengthNode(self_param, length_local))
        self.instructions.append(cil.ReturnNode(self.register_new("Int", length_local)))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "length"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string_concat(self):
        self.reset_state()
        self_param = self.register_param("self")
        other_param = self.register_param("other")

        concat_local = self.register_local("concat")
        self_len_local = self.register_local("self_len")
        other_len_local = self.register_local("other_len")
        concat_len_local = self.register_local("concat_len")

        self.instructions.append(cil.LengthNode(self_len_local, self_param))
        self.instructions.append(cil.LengthNode(other_len_local, other_param))
        self.instructions.append(
            cil.PlusNode(concat_len_local, self_len_local, other_len_local)
        )
        self.instructions.append(
            cil.ConcatNode(concat_local, self_param, other_param, concat_len_local)
        )
        self.instructions.append(
            cil.ReturnNode(self.register_new("String", concat_local))
        )
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "concat"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string_substr(self):
        self.reset_state()
        self_param = self.register_param("self")
        i_param = self.register_param("i")
        l_param = self.register_param("l")
        ret_local = self.register_local("substr")
        self.instructions.append(
            cil.SubstringNode(ret_local, self_param, l_param, i_param)
        )
        self.instructions.append(cil.ReturnNode(ret_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "substr"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_object_init(self):
        self.reset_state()
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode("Object", self_local))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Object", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_int_init(self):
        self.reset_state()
        value_param = self.register_param("value")
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode("Int", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Int", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_bool_init(self):
        self.reset_state()
        value_param = self.register_param("value")
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode("Bool", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Bool", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_string_init(self):
        self.reset_state()
        value_param = self.register_param("value")
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode("String", self_local))
        self.instructions.append(cil.SetAttrNode(self_local, 0, value_param))
        self.instructions.append(cil.ReturnNode(self_local))
        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("String", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

    def register_builtins(self):
        self.register_object_abort()

        for type in self.methods:
            self.register_type_name(type)
            self.register_copy(type)

        self.register_io_out_string()
        self.register_io_out_int()
        self.register_io_in_string()
        self.register_io_in_int()

        self.register_string_length()
        self.register_string_concat()
        self.register_string_substr()

        self.register_object_init()
        self.register_int_init()
        self.register_bool_init()
        self.register_string_init()

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(type_checked.CoolProgramNode)
    def visit(self, node: type_checked.CoolProgramNode):
        self.attrs, self.methods = dict(), dict()
        for type in node.types:
            self.attrs[type.name] = {
                attr.name: (i, htype.name)
                for i, (attr, htype) in enumerate(type.all_attributes())
            }
            self.methods[type.name] = {
                method.name: (i, htype.name)
                if method.name != "type_name"
                else (i, type.name)
                for i, (method, htype) in enumerate(type.all_methods())
            }
            self.dottypes.append(
                cil.TypeNode(
                    type.name,
                    list(self.attrs[type.name].keys()),
                    [
                        self.get_func_id(htype, method)
                        for method, (_, htype) in self.methods[type.name].items()
                    ],
                )
            )

        self.reset_state()
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode("Void", self_local))
        self.instructions.append(cil.ReturnNode(self_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id("Void", "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        self.reset_state()
        main_instance = self.register_new("Main")
        self.instructions.append(cil.ArgNode(main_instance))
        self.instructions.append(
            cil.StaticCallNode(self.get_func_id("Main", "main"), self.register_local())
        )
        self.instructions.append(cil.ExitNode(0))
        self.dotcode.append(
            cil.FunctionNode("main", self.params, self.locals, self.instructions)
        )

        self.register_builtins()

        for cool_class in node.classes:
            self.visit(cool_class)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(type_checked.CoolClassNode)
    def visit(self, node: type_checked.CoolClassNode):
        self.type = node.type.name
        self.reset_state()
        self_local = self.register_local("self")
        self.instructions.append(cil.AllocateNode(node.type.name, self_local))
        for attr, (i, htype) in self.attrs[node.type.name].items():
            attr_local = self.register_local(attr)
            self.instructions.append(cil.ArgNode(self_local))
            self.instructions.append(
                cil.StaticCallNode(self.get_func_id(htype, f"{attr}___init"), attr_local,)
            )
            self.instructions.append(cil.SetAttrNode(self_local, i, attr_local))
        self.instructions.append(cil.ReturnNode(self_local))

        self.dotcode.append(
            cil.FunctionNode(
                self.get_func_id(node.type.name, "__init"),
                self.params,
                self.locals,
                self.instructions,
            )
        )

        for feat in node.features:
            function = self.visit(feat)
            self.dotcode.append(function)

    @visitor.when(type_checked.CoolAttrDeclNode)
    def visit(self, node: type_checked.CoolAttrDeclNode) -> cil.FunctionNode:
        self.reset_state()
        self.register_param("self")
        if node.body is not None:
            sid = self.visit(node.body)
        else: # Void
            sid = self.register_new("Void")
        self.instructions.append(cil.ReturnNode(sid))
        return cil.FunctionNode(
            self.get_func_id(self.type, f"{node.attr_info.name}___init"),
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

        attr_id = self.get_attr_id(self.type, node.id)
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
        if node.expr is not None:
            rhs_local = self.visit(node.expr)
            self.instructions.append(cil.AssignNode(lhs_local, rhs_local))
        else:
            self.register_new("Void", dest=lhs_local)

        return lhs_local

    @visitor.when(type_checked.CoolCaseNode)
    def visit(self, node: type_checked.CoolCaseNode) -> str:
        expr_local = self.visit(node.expr)

        def compare_types(t1, t2):
            t12, t21 = t1.conforms_to(t2), t2.conforms_to(t1)
            return 0 if t12 and t21 else 1 if t21 else -1

        sorted_types = sorted(
            node.expr.type.reachable,
            key=cmp_to_key(compare_types),
        )

        sorted_branches = sorted(
            node.case_branches,
            key=cmp_to_key(lambda b1, b2: compare_types(b1.branch_type, b2.branch_type)),
        )

        branch_labels = []
        for t in sorted_types:
            for b in sorted_branches:
                btyp = b.branch_type
                if not t.conforms_to(btyp):
                    continue

                runtime_type_local = self.register_local()
                self.instructions.append(cil.TypeOfNode(expr_local, runtime_type_local))
                branch_type_local = self.register_local()
                self.instructions.append(cil.LoadNode(branch_type_local, btyp.name))
                types_eq_local = self.register_local()
                self.instructions.append(cil.MinusNode(types_eq_local, runtime_type_local, branch_type_local))
                branch_label = self.get_label("case_branch")
                branch_labels.append(branch_label)
                self.instructions.append(cil.GotoIfNode(types_eq_local, branch_label))
                break

        data = self.register_data("case_err", '"Case of did not match any branch!"')
        instance = self.register_new("String", data)
        self.instructions.append(cil.PrintNode(instance, True))
        self.instructions.append(cil.ExitNode(1))

        ret_local = self.register_local()

        end_label = self.get_label("end_case")
        for label, branch in zip(branch_labels, sorted_branches):
            self.instructions.append(cil.LabelNode(label))
            branch_local = self.register_local(branch.id)
            self.instructions.append(cil.AssignNode(branch_local, expr_local))
            branch_ret_local = self.visit(branch.expr)
            self.instructions.append(cil.AssignNode(ret_local, branch_ret_local))
            self.instructions.append(cil.GotoNode(end_label))
        self.instructions.append(cil.LabelNode(end_label))

        return ret_local

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
        expr = self.visit(node.expr)
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
        literal = self.register_num(int(node.value))
        return self.register_new("Int", literal)

    @visitor.when(type_checked.CoolBoolNode)
    def visit(self, node: type_checked.CoolBoolNode) -> str:
        literal = self.register_num(1 if node.value == "true" else 0)
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

        param_sid = self.get_param(node.value)
        if any(param_sid == p.name for p in self.params):
            return param_sid

        local_sid = self.register_local(node.value)
        # print((node.type.name, node.value))
        attr_id = self.get_attr_id(self.type, node.value)
        self.instructions.append(
            cil.GetAttrNode(self.get_param("self"), attr_id, local_sid)
        )
        return local_sid
