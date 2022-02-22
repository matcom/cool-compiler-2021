import cil_ast as cil
from semantic.semantic import VariableInfo


class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = {}
        self.dotdata = {}
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
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

    def register_param(self, vinfo):
        # 'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_local(self, name):
        #vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(name)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self, scope, name="internal", cool_var=None, class_type=None):
        if class_type != None:
            cil_name = f'{class_type}.{name}'
            scope.define_cil_local(cool_var, cil_name, None)
            self.register_local(cil_name)
        else:
            cil_name = f'{name}_{len(self.localvars)}'
            scope.define_cil_local(cool_var, cil_name, None)
            self.register_local(cil_name)
        return cil_name

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###############################

    def to_function_name(self, method_name, type_name):
        return f'{type_name}.{method_name}'

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes[name] = type_node
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        self.dotdata[vname] = value
        return vname

    def define_built_in(self, scope):
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = [
                f'{attr}' for attr in builtin_type.attributes]
            cil_type.methods = {f'{m}': f'{c}.{m}' for c,
                                m in builtin_type.get_all_methods()}
            if t in ['Int', 'String', 'Bool']:
                cil_type.attributes.append('value')

        # ----------------Object---------------------
        # init
        self.current_function = self.register_function('Object_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(cil.ReturnNode(None))

        # abort
        self.current_function = self.register_function(
            self.to_function_name('abort', 'Object'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="msg")
        key_msg = ''
        for s in self.dotdata.keys():
            if self.dotdata[s] == 'Abort called from class ':
                key_msg = s
        self.register_instruction(cil.LoadStringNode(key_msg, msg))
        self.register_instruction(cil.PrintStringNode(msg))
        type_name = self.define_internal_local(scope=scope, name="type_name")
        self.register_instruction(cil.TypeOfNode('self', type_name))
        self.register_instruction(cil.PrintStringNode(type_name))
        eol_local = self.define_internal_local(scope=scope, name="eol")
        for s in self.dotdata.keys():
            if self.dotdata[s] == '\n':
                eol = s
        self.register_instruction(cil.LoadStringNode(eol, eol_local))
        self.register_instruction(cil.PrintStringNode(eol_local))
        self.register_instruction(cil.HaltNode())

        # type_name
        self.current_function = self.register_function(
            self.to_function_name('type_name', 'Object'))
        self.register_param(VariableInfo('self', None))
        type_name = self.define_internal_local(scope=scope, name="type_name")
        self.register_instruction(cil.TypeOfNode('self', type_name))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'String_init', [
                                  cil.ArgNode(type_name), cil.ArgNode(instance)], "String"))
        self.register_instruction(cil.ReturnNode(instance))

        # copy
        self.current_function = self.register_function(
            self.to_function_name('copy', 'Object'))
        self.register_param(VariableInfo('self', None))
        copy = self.define_internal_local(scope=scope, name="copy")
        self.register_instruction(cil.CopyNode('self', copy))
        self.register_instruction(cil.ReturnNode(copy))

        # ----------------IO---------------------
        # init
        self.current_function = self.register_function('IO_init')
        self.register_param(VariableInfo('self', None))
        self.register_instruction(cil.ReturnNode(None))

        # out_string
        self.current_function = self.register_function(
            self.to_function_name('out_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(cil.GetAttrNode(v, 'x', 'value', 'String'))
        self.register_instruction(cil.PrintStringNode(v))
        self.register_instruction(cil.ReturnNode('self'))

        # out_int
        self.current_function = self.register_function(
            self.to_function_name('out_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('x', None))
        v = self.define_internal_local(scope=scope, name="v")
        self.register_instruction(cil.GetAttrNode(v, 'x', 'value', 'Int'))
        self.register_instruction(cil.PrintIntNode(v))
        self.register_instruction(cil.ReturnNode('self'))

        # in_string
        self.current_function = self.register_function(
            self.to_function_name('in_string', 'IO'))
        self.register_param(VariableInfo('self', None))
        msg = self.define_internal_local(scope=scope, name="read_str")
        self.register_instruction(cil.ReadStringNode(msg))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'String_init', [
                                  cil.ArgNode(msg), cil.ArgNode(instance)], "String"))
        self.register_instruction(cil.ReturnNode(instance))

        # in_int
        self.current_function = self.register_function(
            self.to_function_name('in_int', 'IO'))
        self.register_param(VariableInfo('self', None))
        number = self.define_internal_local(scope=scope, name="read_int")
        self.register_instruction(cil.ReadIntNode(number))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(number), cil.ArgNode(instance)], "Int"))
        self.register_instruction(cil.ReturnNode(instance))

        # ----------------String---------------------
        # init
        self.current_function = self.register_function('String_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(
            cil.SetAttrNode('self', 'value', 'v', 'String'))
        self.register_instruction(cil.ReturnNode(None))

        # length
        self.current_function = self.register_function(
            self.to_function_name('length', 'String'))
        self.register_param(VariableInfo('self', None))
        length_result = self.define_internal_local(scope=scope, name="length")
        self.register_instruction(cil.LengthNode('self', length_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'Int', self.context.get_type('Int').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'Int_init', [
                                  cil.ArgNode(length_result), cil.ArgNode(instance)], "Int"))
        self.register_instruction(cil.ReturnNode(instance))

        # concat
        self.current_function = self.register_function(
            self.to_function_name('concat', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('s', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(cil.GetAttrNode(
            str1, 'self', 'value', 'String'))
        len1 = self.define_internal_local(scope=scope, name="len1")
        self.register_instruction(cil.CallNode(
            len1, 'String.length', [cil.ArgNode('self')], 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(
            cil.GetAttrNode(str2, 's', 'value', 'String'))
        len2 = self.define_internal_local(scope=scope, name="len2")
        self.register_instruction(cil.CallNode(
            len2, 'String.length', [cil.ArgNode('s')], 'String'))

        local_len1 = self.define_internal_local(scope=scope, name="local_len1")
        self.register_instruction(cil.GetAttrNode(
            local_len1, len1, 'value', 'Int'))
        local_len2 = self.define_internal_local(scope=scope, name="local_len2")
        self.register_instruction(cil.GetAttrNode(
            local_len2, len2, 'value', 'Int'))

        concat_result = self.define_internal_local(scope=scope, name="concat")
        self.register_instruction(cil.ConcatNode(
            str1, local_len1, str2, local_len2, concat_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'String_init', [
                                  cil.ArgNode(concat_result), cil.ArgNode(instance)], "String"))
        self.register_instruction(cil.ReturnNode(instance))

        # substr
        self.current_function = self.register_function(
            self.to_function_name('substr', 'String'))
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        i_value = self.define_internal_local(scope=scope, name="i_value")
        self.register_instruction(
            cil.GetAttrNode(i_value, 'i', 'value', 'Int'))
        l_value = self.define_internal_local(scope=scope, name="l_value")
        self.register_instruction(
            cil.GetAttrNode(l_value, 'l', 'value', 'Int'))
        subs_result = self.define_internal_local(
            scope=scope, name="subs_result")
        self.register_instruction(cil.SubstringNode(
            i_value, l_value, 'self', subs_result))
        instance = self.define_internal_local(scope=scope, name="instance")
        self.register_instruction(cil.AllocateNode(
            'String', self.context.get_type('String').tag, instance))
        result_init = self.define_internal_local(
            scope=scope, name="result_init")
        self.register_instruction(cil.CallNode(result_init, 'String_init', [
                                  cil.ArgNode(subs_result), cil.ArgNode(instance)], "String"))
        self.register_instruction(cil.ReturnNode(instance))

        # ----------------Bool---------------------
        # init
        self.current_function = self.register_function('Bool_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(
            cil.SetAttrNode('self', 'value', 'v', 'Bool'))
        self.register_instruction(cil.ReturnNode(None))

        # ----------------Int---------------------
        # init
        self.current_function = self.register_function('Int_init')
        self.register_param(VariableInfo('self', None))
        self.register_param(VariableInfo('v', None))
        self.register_instruction(cil.SetAttrNode('self', 'value', 'v', 'Int'))
        self.register_instruction(cil.ReturnNode(None))

    def build_string_equals_function(self, scope):
        self.current_function = self.register_function('String_equals')
        self.register_param(VariableInfo('str1', None))
        self.register_param(VariableInfo('str2', None))

        str1 = self.define_internal_local(scope=scope, name="str1")
        self.register_instruction(cil.GetAttrNode(
            str1, 'str1', 'value', 'String'))

        str2 = self.define_internal_local(scope=scope, name="str2")
        self.register_instruction(cil.GetAttrNode(
            str2, 'str2', 'value', 'String'))

        result = self.define_internal_local(
            scope=scope, name="comparison_result")
        self.register_instruction(cil.StringEqualsNode(str1, str2, result))
        self.register_instruction(cil.ReturnNode(result))
