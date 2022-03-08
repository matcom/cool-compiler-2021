from utils.semantic import Scope, VariableInfo
import utils.visitor as visitor
import ast_cool_hierarchy as COOL_AST
import ast_cil_hierarchy as CIL_AST


class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = {}
        self.dotdata = {}
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.label_count = 0
        self.context.set_type_tags()
        self.context.set_type_max_tags()

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def get_label(self):
        self.label_count += 1
        return f'label_{self.label_count}'

    def register_param(self, vinfo):
        param_node = CIL_AST.ParamDec(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def is_defined_param(self, name):
        for p in self.params:
            if p.name == name:
                return True
        return False

    def register_local(self, var_name):
        local_node = CIL_AST.LocalDec(var_name)
        self.localvars.append(local_node)
        return var_name

    def define_internal_local(self, scope, name="internal", cool_var_name=None, class_type=None):
        if class_type != None:
            cilname = f'{class_type}.{name}'
            scope.define_cil_local(cool_var_name, cilname, None)
            self.register_local(cilname)
        else:
            cilname = f'{name}_{len(self.localvars)}'
            scope.define_cil_local(cool_var_name, cilname, None)
            self.register_local(cilname)
        return cilname

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f'{type_name}.{method_name}'

    def register_function(self, function_name):
        function_node = CIL_AST.Function(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = CIL_AST.Type(name)
        self.dottypes[name] = type_node
        return type_node

    def is_in_data(self, name):
        return name in self.dotdata.keys

    def register_data(self, value):
        vname = f's_{len(self.dotdata)}'
        self.dotdata[vname] = value
        return vname

    def register_builtin_types(self, scope):
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = [f'{attr.name}' for attr in builtin_type.attributes]
            cil_type.methods = {f'{m}': f'{c}.{m}' for c, m in builtin_type.get_all_methods()}
            if t in ['Int', 'String', 'Bool']:
                cil_type.attributes.append('value')

        # ----------------Object---------------------
        # init
        self.current_function = self.register_function('Object_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.Return(None))

        # abort
        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="msg")
        key_msg = ''
        for s in self.dotdata.keys():
            if self.dotdata[s] == 'Abort called from class ':
                key_msg = s
        self.register_instruction(CIL_AST.LoadStr(key_msg, msg))
        self.register_instruction(CIL_AST.PrintString(msg))
        type_name = self.define_internal_local(scope=scope, name="type_name")
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        self.register_instruction(CIL_AST.PrintString(type_name))
        eol_local = self.define_internal_local(scope=scope, name="eol")
        for s in self.dotdata.keys():
            if self.dotdata[s] == '\n':
                eol = s
        self.register_instruction(CIL_AST.LoadStr(eol, eol_local))
        self.register_instruction(CIL_AST.PrintString(eol_local))
        self.register_instruction(CIL_AST.Halt())

        # type_name
        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local(scope=scope, name="type_name")
        self.register_instruction(CIL_AST.TypeOf('self', type_name))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(type_name), CIL_AST.Arg(instance)], "String"))
        self.register_instruction(CIL_AST.Return(instance))

        # copy
        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(VariableInfo('self', None))
        copy = self.define_internal_local(scope=scope, name="copy")
        self.register_instruction(CIL_AST.Copy('self', copy))
        self.register_instruction(CIL_AST.Return(copy))

        # ----------------IO---------------------
        # init
        self.current_function = self.register_function('IO_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(CIL_AST.Return(None))

        # out_string
        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(CIL_AST.GetAttr(v, 'x', 'value', 'String'))
        self.register_instruction(CIL_AST.PrintString(v))
        self.register_instruction(CIL_AST.Return('self'))

        # out_int
        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(CIL_AST.GetAttr(v, 'x', 'value', 'Int'))
        self.register_instruction(CIL_AST.PrintInteger(v))
        self.register_instruction(CIL_AST.Return('self'))

        # in_string
        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="read_str")
        self.register_instruction(CIL_AST.ReadString(msg))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(msg), CIL_AST.Arg(instance)], "String"))
        self.register_instruction(CIL_AST.Return(instance))

        # in_int
        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local(scope=scope, name="read_int")
        self.register_instruction(CIL_AST.ReadInteger(number))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(number), CIL_AST.Arg(instance)], "Int"))
        self.register_instruction(CIL_AST.Return(instance))

        # ----------------String---------------------
        # init
        self.current_function = self.register_function('String_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'String'))
        self.register_instruction(CIL_AST.Return(None))

        # length
        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        length_result = self.define_internal_local(scope=scope, name="length")
        self.register_instruction(CIL_AST.Length('self', length_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(length_result), CIL_AST.Arg(instance)], "Int"))
        self.register_instruction(CIL_AST.Return(instance))

        # concat
        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(CIL_AST.GetAttr(str1, 'self', 'value', 'String'))
        len1 = self.define_internal_local(scope=scope, name="len1")
        self.register_instruction(CIL_AST.Call(len1, 'String.length', [CIL_AST.Arg('self')], 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(CIL_AST.GetAttr(str2, 's', 'value', 'String'))
        len2 = self.define_internal_local(scope=scope, name="len2")
        self.register_instruction(CIL_AST.Call(len2, 'String.length', [CIL_AST.Arg('s')], 'String'))

        local_len1 = self.define_internal_local(scope=scope, name="local_len1")
        self.register_instruction(CIL_AST.GetAttr(local_len1, len1, 'value', 'Int'))
        local_len2 = self.define_internal_local(scope=scope, name="local_len2")
        self.register_instruction(CIL_AST.GetAttr(local_len2, len2, 'value', 'Int'))

        concat_result = self.define_internal_local(scope=scope, name="concat")
        self.register_instruction(CIL_AST.Concat(str1, local_len1, str2, local_len2, concat_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(concat_result), CIL_AST.Arg(instance)], "String"))
        self.register_instruction(CIL_AST.Return(instance))

        # substr
        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        i_value = self.define_internal_local(scope=scope, name="i_value")
        self.register_instruction(CIL_AST.GetAttr(i_value, 'i', 'value', 'Int'))
        l_value = self.define_internal_local(scope=scope, name="l_value")
        self.register_instruction(CIL_AST.GetAttr(l_value, 'l', 'value', 'Int'))
        subs_result = self.define_internal_local(scope=scope, name="subs_result")
        self.register_instruction(CIL_AST.SubStr(i_value, l_value, 'self', subs_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(subs_result), CIL_AST.Arg(instance)], "String"))
        self.register_instruction(CIL_AST.Return(instance))

        # ----------------Bool---------------------
        # init
        self.current_function = self.register_function('Bool_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'Bool'))
        self.register_instruction(CIL_AST.Return(None))

        # ----------------Int---------------------
        # init
        self.current_function = self.register_function('Int_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(CIL_AST.SetAttr('self', 'value', 'v', 'Int'))
        self.register_instruction(CIL_AST.Return(None))

    def build_string_equals_function(self, scope):
        self.current_function = self.register_function('String_equals')
        self.register_param(VariableInfo('str1', None))
        self.register_param(VariableInfo('str2', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(CIL_AST.GetAttr(str1, 'str1', 'value', 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(CIL_AST.GetAttr(str2, 'str2', 'value', 'String'))

        result = self.define_internal_local(scope=scope, name="comparison_result")
        self.register_instruction(CIL_AST.StringEquals(str1, str2, result))
        self.register_instruction(CIL_AST.Return(result))


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(COOL_AST.ProgramNode)
    def visit(self, node: COOL_AST.ProgramNode, scope=None):
        scope = Scope()
        self.current_function = self.register_function('main')
        instance = self.define_internal_local(scope=scope, name="instance")
        result = self.define_internal_local(scope=scope, name="result")
        self.register_instruction(CIL_AST.Allocate('Main', self.context.get_type('Main').tag, instance))
        self.register_instruction(CIL_AST.Call(result, 'Main_init', [CIL_AST.Arg(instance)], "Main"))
        self.register_instruction(
            CIL_AST.Call(result, self.to_function_name('main', 'Main'), [CIL_AST.Arg(instance)], "Main"))
        self.register_instruction(CIL_AST.Return(None))
        self.current_function = None

        self.register_data('Abort called from class ')
        self.register_data('\n')
        self.dotdata['empty_str'] = ''

        # Add built-in types in .TYPES section
        self.register_builtin_types(scope)

        # Add string equals function
        self.build_string_equals_function(scope)

        for klass in node.declarations:
            self.visit(klass, scope.create_child())

        return CIL_AST.Program(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(COOL_AST.ClassDeclarationNode)
    def visit(self, node: COOL_AST.ClassDeclarationNode, scope):
        self.current_type = self.context.get_type(node.id)

        # Handle all the .TYPE section
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = [f'{attr.name}' for c, attr in self.current_type.get_all_attributes()]
        cil_type.methods = {f'{m}': f'{c}.{m}' for c, m in self.current_type.get_all_methods()}

        scope.define_cil_local("self", self.current_type.name, self.current_type)

        func_declarations = [f for f in node.features if isinstance(f, COOL_AST.FuncDeclarationNode)]
        attr_declarations = [a for a in node.features if isinstance(a, COOL_AST.AttrDeclarationNode)]
        for attr in attr_declarations:
            scope.define_cil_local(attr.id, attr.id, node.id)

        # -------------------------Init---------------------------------
        self.current_function = self.register_function(f'{node.id}_init')
        self.register_param(VariableInfo('self', None))

        # Init parents recursively
        result = self.define_internal_local(scope=scope, name="result")
        self.register_instruction(CIL_AST.Call(result, f'{node.parent}_init', [CIL_AST.Arg('self')], node.parent))
        self.register_instruction(CIL_AST.Return(None))

        for attr in attr_declarations:
            self.visit(attr, scope)
        # ---------------------------------------------------------------
        self.current_function = None

        for feature in func_declarations:
            self.visit(feature, scope.create_child())

        self.current_type = None

    @visitor.when(COOL_AST.FuncDeclarationNode)
    def visit(self, node: COOL_AST.FuncDeclarationNode, scope):
        self.current_method = self.current_type.get_method(node.id)[0]
        self.dottypes[self.current_type.name].methods[node.id] = f'{self.current_type.name}.{node.id}'
        cil_method_name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.register_function(cil_method_name)

        self.register_param(VariableInfo('self', self.current_type))
        for p_name, p_type in node.params:
            self.register_param(VariableInfo(p_name, p_type))

        value = self.visit(node.body, scope)

        self.register_instruction(CIL_AST.Return(value))
        self.current_method = None

    @visitor.when(COOL_AST.AttrDeclarationNode)
    def visit(self, node: COOL_AST.AttrDeclarationNode, scope):
        instance = None

        if node.val is not None:
            expr = self.visit(node.val, scope)
            self.register_instruction(CIL_AST.SetAttr('self', node.id, expr, self.current_type.name))
            return

        if node.type in ['Int', 'Bool']:
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type, self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadInt(0, value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(
                CIL_AST.Call(result_init, f'{node.type}_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)], node.type))
        elif node.type == 'String':
            instance = self.define_internal_local(scope=scope, name="instance")
            self.register_instruction(CIL_AST.Allocate(node.type, self.context.get_type(node.type).tag, instance))
            value = self.define_internal_local(scope=scope, name="value")
            self.register_instruction(CIL_AST.LoadStr('empty_str', value))
            result_init = self.define_internal_local(scope=scope, name="result_init")
            self.register_instruction(
                CIL_AST.Call(result_init, f'{node.type}_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)], node.type))

        self.register_instruction(CIL_AST.SetAttr('self', node.id, instance, self.current_type.name))


    @visitor.when(COOL_AST.AssignNode)
    def visit(self, node: COOL_AST.AssignNode, scope):
        expr_local = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name="result")
        cil_node_name = scope.find_cil_local(node.id)

        if self.is_defined_param(node.id):
            self.register_instruction(CIL_AST.Assign(node.id, expr_local))
        elif self.current_type.has_attr(node.id):
            cil_type_name = 'self'
            self.register_instruction(CIL_AST.SetAttr(cil_type_name, node.id, expr_local, self.current_type.name))
        else:
            self.register_instruction(CIL_AST.Assign(cil_node_name, expr_local))
        return expr_local

    @visitor.when(COOL_AST.BlockNode)
    def visit(self, node: COOL_AST.BlockNode, scope):
        result_local = None
        for e in node.expr_list:
            result_local = self.visit(e, scope)
        return result_local

    @visitor.when(COOL_AST.ConditionalNode)
    def visit(self, node: COOL_AST.ConditionalNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        cond_value = self.visit(node.if_expr, scope)

        if_then_label = self.get_label()
        self.register_instruction(CIL_AST.IfGoto(cond_value, if_then_label))

        else_value = self.visit(node.else_expr, scope)
        self.register_instruction(CIL_AST.Assign(result_local, else_value))

        end_if_label = self.get_label()
        self.register_instruction(CIL_AST.Goto(end_if_label))

        self.register_instruction(CIL_AST.Label(if_then_label))
        then_value = self.visit(node.then_expr, scope)
        self.register_instruction(CIL_AST.Assign(result_local, then_value))
        self.register_instruction(CIL_AST.Label(end_if_label))

        return result_local

    @visitor.when(COOL_AST.LoopNode)
    def visit(self, node: COOL_AST.LoopNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")

        loop_init_label = self.get_label()
        loop_body_label = self.get_label()
        loop_end_label = self.get_label()
        self.register_instruction(CIL_AST.Label(loop_init_label))
        pred_value = self.visit(node.condition, scope)
        self.register_instruction(CIL_AST.IfGoto(pred_value, loop_body_label))
        self.register_instruction(CIL_AST.Goto(loop_end_label))

        self.register_instruction(CIL_AST.Label(loop_body_label))
        body_value = self.visit(node.body, scope)
        self.register_instruction(CIL_AST.Goto(loop_init_label))
        self.register_instruction(CIL_AST.Label(loop_end_label))

        self.register_instruction(CIL_AST.LoadVoid(result_local))
        return result_local

    @visitor.when(COOL_AST.CallNode)
    def visit(self, node: COOL_AST.CallNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        expr_value = self.visit(node.obj, scope)

        call_args = []
        for arg in reversed(node.args):
            param_local = self.visit(arg, scope)
            call_args.append(CIL_AST.Arg(param_local))
        call_args.append(CIL_AST.Arg(expr_value))

        if node.ancestor_type is None:
            o_type = self.current_type if node.obj.computed_type.name == 'SELF_TYPE' else node.obj.computed_type
            dynamic_type = o_type.name
            self.register_instruction(CIL_AST.VCall(result_local, node.id, call_args, dynamic_type, expr_value))
        else:
            static_instance = self.define_internal_local(scope=scope, name='static_instance')
            self.register_instruction(
                CIL_AST.Allocate(node.ancestor_type, self.context.get_type(node.ancestor_type).tag, static_instance))

            self.register_instruction(
                CIL_AST.VCall(result_local, node.id, call_args, node.ancestor_type, static_instance))

        return result_local

    @visitor.when(COOL_AST.LetNode)
    def visit(self, node: COOL_AST.LetNode, scope):
        let_scope = scope.create_child()
        for var_name, var_type, var_expr in node.var_list:
            if var_expr is not None:
                var_expr_value = self.visit(var_expr, let_scope)
            else:
                instance = None
                if var_type in ['Int', 'Bool']:
                    instance = self.define_internal_local(scope=let_scope, name="instance")
                    self.register_instruction(
                        CIL_AST.Allocate(var_type, self.context.get_type(var_type).tag, instance))
                    value = self.define_internal_local(scope=let_scope, name="value")
                    self.register_instruction(CIL_AST.LoadInt(0, value))
                    result_init = self.define_internal_local(scope=let_scope, name="result_init")
                    self.register_instruction(
                        CIL_AST.Call(result_init, f'{var_type}_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)],
                                     var_type))
                elif var_type == 'String':
                    instance = self.define_internal_local(scope=let_scope, name="instance")
                    self.register_instruction(
                        CIL_AST.Allocate(var_type, self.context.get_type(var_type).tag, instance))
                    value = self.define_internal_local(scope=let_scope, name="value")
                    self.register_instruction(CIL_AST.LoadStr('empty_str', value))
                    result_init = self.define_internal_local(scope=let_scope, name="result_init")
                    self.register_instruction(
                        CIL_AST.Call(result_init, f'{var_type}_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)],
                                     var_type))
                var_expr_value = instance
            let_var = self.define_internal_local(scope=let_scope, name=var_name, cool_var_name=var_name)
            self.register_instruction(CIL_AST.Assign(let_var, var_expr_value))

        body_value = self.visit(node.body, let_scope)
        result_local = self.define_internal_local(scope=scope, name="let_result")
        self.register_instruction(CIL_AST.Assign(result_local, body_value))
        return result_local

    @visitor.when(COOL_AST.CaseNode)
    def visit(self, node: COOL_AST.CaseNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        case_expr = self.visit(node.expr, scope)

        exit_label = self.get_label()
        label = self.get_label()

        self.register_instruction(CIL_AST.Case(case_expr, label))

        tag_lst = []
        action_dict = {}
        for action in node.branch_list:
            tag = self.context.get_type(action.type).tag
            tag_lst.append(tag)
            action_dict[tag] = action
        tag_lst.sort()

        for t in reversed(tag_lst):
            action: COOL_AST.BranchNode = action_dict[t]
            self.register_instruction(CIL_AST.Label(label))
            label = self.get_label()

            action_type = self.context.get_type(action.type)
            self.register_instruction(CIL_AST.Action(case_expr, action_type.tag, action_type.max_tag, label))

            action_scope = scope.create_child()
            action_id = self.define_internal_local(scope=action_scope, name=action.id, cool_var_name=action.id)
            self.register_instruction(CIL_AST.Assign(action_id, case_expr))
            expr_result = self.visit(action.action, action_scope)

            self.register_instruction(CIL_AST.Assign(result_local, expr_result))
            self.register_instruction(CIL_AST.Goto(exit_label))

        self.register_instruction(CIL_AST.Label(label))
        self.register_instruction(CIL_AST.Goto('case_no_match_error'))
        self.register_instruction(CIL_AST.Label(exit_label))
        return result_local

    @visitor.when(COOL_AST.InstantiateNode)
    def visit(self, node: COOL_AST.InstantiateNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        result_init = self.define_internal_local(scope=scope, name="init")

        if node.lex == "SELF_TYPE":
            self.register_instruction(CIL_AST.Allocate(self.current_type.name, self.current_type.tag, result_local))
            self.register_instruction(
                CIL_AST.Call(result_init, f'{self.current_type.name}_init', [result_local], self.current_type.name))
        else:
            self.register_instruction(CIL_AST.Allocate(node.lex, self.context.get_type(node.lex).tag, result_local))
            self.register_instruction(
                CIL_AST.Call(result_init, f'{node.lex}_init', [CIL_AST.Arg(result_local)], self.current_type.name))

        return result_local

    @visitor.when(COOL_AST.IsVoidNode)
    def visit(self, node: COOL_AST.IsVoidNode, scope):
        expre_value = self.visit(node.expr, scope)
        result_local = self.define_internal_local(scope=scope, name="isvoid_result")
        self.register_instruction(CIL_AST.IsVoid(result_local, expre_value))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Bool', self.context.get_type('Bool').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(result_local), CIL_AST.Arg(instance)], "Bool"))
        return instance

    @visitor.when(COOL_AST.ArithBinaryNode)
    def visit(self, node: COOL_AST.ArithBinaryNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        l_type = self.current_type if node.left.computed_type.name == 'SELF_TYPE' else node.left.computed_type
        r_type = self.current_type if node.right.computed_type.name == 'SELF_TYPE' else node.right.computed_type

        self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", l_type.name))
        self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", r_type.name))

        if isinstance(node, COOL_AST.PlusNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "+"))
        elif isinstance(node, COOL_AST.MinusNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "-"))
        elif isinstance(node, COOL_AST.StarNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "*"))
        elif isinstance(node, COOL_AST.DivNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "/"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))
        return result_local

    @visitor.when(COOL_AST.IntCompNode)
    def visit(self, node: COOL_AST.IntCompNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        expr_local = self.define_internal_local(scope=scope)

        expr_value = self.visit(node.expr, scope)

        e_type = self.current_type if node.expr.computed_type.name == 'SELF_TYPE' else node.expr.computed_type
        self.register_instruction(CIL_AST.GetAttr(expr_local, expr_value, "value", e_type.name))
        self.register_instruction(CIL_AST.UnaryOperator(op_local, expr_local, "~"))

        # Allocate Int result
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Int"))

        return result_local

    @visitor.when(COOL_AST.NotNode)
    def visit(self, node: COOL_AST.NotNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        expr_local = self.define_internal_local(scope=scope)

        expr_value = self.visit(node.expr, scope)

        e_type = self.current_type if node.expr.computed_type.name == 'SELF_TYPE' else node.expr.computed_type
        self.register_instruction(CIL_AST.GetAttr(expr_local, expr_value, "value", e_type.name))
        self.register_instruction(CIL_AST.UnaryOperator(op_local, expr_local, "not"))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))

        return result_local

    @visitor.when(COOL_AST.BooleanBinaryNode)
    def visit(self, node: COOL_AST.BooleanBinaryNode, scope):
        result_local = self.define_internal_local(scope=scope, name="result")
        op_local = self.define_internal_local(scope=scope, name="op")
        left_local = self.define_internal_local(scope=scope, name="left")
        right_local = self.define_internal_local(scope=scope, name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        l_type = self.current_type if node.left.computed_type.name == 'SELF_TYPE' else node.left.computed_type
        r_type = self.current_type if node.right.computed_type.name == 'SELF_TYPE' else node.right.computed_type

        if isinstance(node, COOL_AST.LessNode) or isinstance(node, COOL_AST.LessEqualNode):
            self.register_instruction(CIL_AST.GetAttr(left_local, left_value, "value", l_type.name))
            self.register_instruction(CIL_AST.GetAttr(right_local, right_value, "value", r_type.name))

        if isinstance(node, COOL_AST.LessNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "<"))
        elif isinstance(node, COOL_AST.LessEqualNode):
            self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "<="))
        elif isinstance(node, COOL_AST.EqualNode):
            if l_type.name == 'String':
                self.register_instruction(
                    CIL_AST.Call(op_local, 'String_equals', [CIL_AST.Arg(right_value), CIL_AST.Arg(left_value)],
                                 'String'))
            elif l_type.name in ['Int', 'Bool']:
                self.register_instruction(
                    CIL_AST.GetAttr(left_local, left_value, "value", l_type.name))
                self.register_instruction(
                    CIL_AST.GetAttr(right_local, right_value, "value", r_type.name))
                self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "="))
            else:
                self.register_instruction(CIL_AST.Assign(left_local, left_value))
                self.register_instruction(CIL_AST.Assign(right_local, right_value))
                self.register_instruction(CIL_AST.BinaryOperator(op_local, left_local, right_local, "="))

        # Allocate Bool result
        self.register_instruction(CIL_AST.Allocate('Bool', self.context.get_type('Bool').tag, result_local))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(op_local), CIL_AST.Arg(result_local)], "Bool"))
        return result_local

    @visitor.when(COOL_AST.VariableNode)
    def visit(self, node: COOL_AST.VariableNode, scope):
        if self.is_defined_param(node.lex):
            return node.lex
        elif self.current_type.has_attr(node.lex):
            result_local = self.define_internal_local(scope=scope, name=node.lex, class_type=self.current_type.name)
            self.register_instruction(CIL_AST.GetAttr(result_local, 'self', node.lex, self.current_type.name))
            return result_local
        else:
            return scope.find_cil_local(node.lex)

    @visitor.when(COOL_AST.ConstantNumNode)
    def visit(self, node: COOL_AST.ConstantNumNode, scope):
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Int', self.context.get_type('Int').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(CIL_AST.LoadInt(node.lex, value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Int_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)], "Int"))
        return instance

    @visitor.when(COOL_AST.StringNode)
    def visit(self, node: COOL_AST.StringNode, scope):
        str_name = ""
        for s in self.dotdata.keys():
            if self.dotdata[s] == node.lex:
                str_name = s
                break
        if str_name == "":
            str_name = self.register_data(node.lex)

        result_local = self.define_internal_local(scope=scope)
        self.register_instruction(CIL_AST.LoadStr(str_name, result_local))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'String_init', [CIL_AST.Arg(result_local), CIL_AST.Arg(instance)], "String"))
        return instance

    @visitor.when(COOL_AST.BoolNode)
    def visit(self, node: COOL_AST.BoolNode, scope):
        boolean = 0
        if str(node.lex) == "True":
            boolean = 1
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(CIL_AST.Allocate('Bool', self.context.get_type('Bool').tag, instance))
        value = self.define_internal_local(scope=scope, name="value")
        self.register_instruction(CIL_AST.LoadInt(boolean, value))
        result_init = self.define_internal_local(scope=scope, name="result_init")
        self.register_instruction(
            CIL_AST.Call(result_init, 'Bool_init', [CIL_AST.Arg(value), CIL_AST.Arg(instance)], "Bool"))
        return instance
