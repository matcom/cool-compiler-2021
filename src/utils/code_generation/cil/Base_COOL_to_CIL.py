from utils.code_generation.cil.AST_CIL import cil_ast as nodes
from cmp.semantic import VariableInfo


class BaseCOOLToCIL:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.current_type = None
        self.current_method = None
        self.current_function = None

        self.context = context
        self.vself = VariableInfo('self', None)

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def ids(self):
        return self.current_function.ids

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_param(self, vinfo):
        param_node = nodes.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_local(self, vinfo, id=False):
        if len(self.current_function.id) >= 8 and self.current_function.id[:8] == 'function':
            name = f'local_{self.current_function.id[9:]}_{vinfo.name}_{len(self.localvars)}'
        else:
            name = f'local_{self.current_function.id[5:]}_{vinfo.name}_{len(self.localvars)}'

        new_vinfo = VariableInfo(name, None)
        local_node = nodes.LocalNode(new_vinfo.name)

        if id:
            self.ids[vinfo.name] = new_vinfo.name

        self.localvars.append(local_node)
        return new_vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def init_name(self, type_name, attr=False):
        if attr:
            return f'init_attr_at_{type_name}'
        return f'init_at_{type_name}'

    def register_function(self, function_name):
        function_node = nodes.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = nodes.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = nodes.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return nodes.LabelNode(lname)

    def register_runtime_error(self, condition, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(
            nodes.IfGotoNode(condition, error_node.label))
        self.register_instruction(nodes.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(nodes.ErrorNode(data_node))
        self.register_instruction(continue_node)

    def register_built_in(self):
        self.__register_Object()
        self.__register_IO()
        self.__register_String()
        self.__register_Int()
        self.__register_Bool()

    # convirtiendo tipos y funciones integrados en COOL en CIL

    def __register_Object(self):
        type_node = self.register_type('Object')

        self.current_function = self.register_function(
            self.init_name('Object'))
        instance = self.define_internal_local()
        self.register_instruction(nodes.AllocateNode('Object', instance))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('abort', 'Object'))
        self.register_param(self.vself)
        vname = self.define_internal_local()
        data_node = [dn for dn in self.dotdata if dn.value ==
                     'Aborting... in class '][0]
        self.register_instruction(nodes.LoadNode(vname, data_node))
        self.register_instruction(nodes.PrintStrNode(vname))
        self.register_instruction(nodes.TypeNameNode(vname, self.vself.name))
        self.register_instruction(nodes.PrintStrNode(vname))
        data_node = self.register_data('\n')
        self.register_instruction(nodes.LoadNode(vname, data_node))
        self.register_instruction(nodes.PrintStrNode(vname))
        self.register_instruction(nodes.AbortNode())

        self.current_function = self.register_function(
            self.to_function_name('type_name', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(nodes.TypeNameNode(result, self.vself.name))
        instance = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(nodes.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('copy', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(nodes.CopyNode(result, self.vself.name))
        self.register_instruction(nodes.ReturnNode(result))

        type_node.methods = [(name, self.to_function_name(name, 'Object'))
                             for name in ['abort', 'type_name', 'copy']]
        type_node.methods += [('init', self.init_name('Object'))]

    def __register_IO(self):
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.init_name('IO'))
        instance = self.define_internal_local()
        self.register_instruction(nodes.AllocateNode('IO', instance))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('out_string', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(
            nodes.GetAttrNode(vname, 'x', 'value', 'String'))
        self.register_instruction(nodes.PrintStrNode(vname))
        self.register_instruction(nodes.ReturnNode(self.vself.name))

        self.current_function = self.register_function(
            self.to_function_name('out_int', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(
            nodes.GetAttrNode(vname, 'x', 'value', 'Int'))
        self.register_instruction(nodes.PrintIntNode(vname))
        self.register_instruction(nodes.ReturnNode(self.vself.name))

        self.current_function = self.register_function(
            self.to_function_name('in_string', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(nodes.ReadStrNode(result))
        instance = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(nodes.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('in_int', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(nodes.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(nodes.StaticCallNode(
            self.init_name('Int'), instance))
        self.register_instruction(nodes.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in ['type_name', 'abort', 'copy']]
        type_node.methods += [(name, self.to_function_name(name, 'IO'))
                              for name in ['out_string', 'out_int', 'in_string', 'in_int']]
        type_node.methods += [('init', self.init_name('IO'))]

    def __register_Int(self):
        type_node = self.register_type('Int')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Int'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(nodes.AllocateNode('Int', instance))
        self.register_instruction(nodes.SetAttrNode(
            instance, 'value', 'val', 'Int'))
        self.register_instruction(nodes.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in ['type_name', 'abort', 'copy']]
        type_node.methods += [('init', self.init_name('Int'))]

    def __register_String(self):
        type_node = self.register_type('String')
        type_node.attributes = ['value', 'length']

        self.current_function = self.register_function(
            self.init_name('String'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(nodes.AllocateNode('String', instance))
        self.register_instruction(nodes.SetAttrNode(
            instance, 'value', 'val', 'String'))
        result = self.define_internal_local()
        self.register_instruction(nodes.LengthNode(result, 'val'))
        attr = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(
            nodes.StaticCallNode(self.init_name('Int'), attr))
        self.register_instruction(nodes.SetAttrNode(
            instance, 'length', attr, 'String'))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('length', 'String'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(nodes.GetAttrNode(
            result, self.vself.name, 'length', 'String'))
        self.register_instruction(nodes.ReturnNode(result))

        self.current_function = self.register_function(
            self.to_function_name('concat', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('s', None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        length_1 = self.define_internal_local()
        length_2 = self.define_internal_local()
        self.register_instruction(nodes.GetAttrNode(
            str_1, self.vself.name, 'value', 'String'))
        self.register_instruction(
            nodes.GetAttrNode(str_2, 's', 'value', 'String'))
        self.register_instruction(nodes.GetAttrNode(
            length_1, self.vself.name, 'length', 'String'))
        self.register_instruction(nodes.GetAttrNode(
            length_2, 's', 'length', 'String'))
        self.register_instruction(nodes.GetAttrNode(
            length_1, length_1, 'value', 'Int'))
        self.register_instruction(nodes.GetAttrNode(
            length_2, length_2, 'value', 'Int'))
        self.register_instruction(nodes.PlusNode(length_1, length_1, length_2))

        result = self.define_internal_local()
        self.register_instruction(
            nodes.ConcatNode(result, str_1, str_2, length_1))
        instance = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(nodes.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(nodes.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('substr', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(nodes.GetAttrNode(
            str_value, self.vself.name, 'value', 'String'))
        self.register_instruction(nodes.GetAttrNode(
            index_value, 'i', 'value', 'Int'))
        self.register_instruction(nodes.GetAttrNode(
            length_value, 'l', 'value', 'Int'))

        self.register_instruction(nodes.GetAttrNode(
            length_attr, self.vself.name, 'length', 'String'))
        self.register_instruction(nodes.PlusNode(
            length_substr, length_value, index_value))
        self.register_instruction(nodes.LessThanNode(
            less_value, length_attr, length_substr))
        self.register_runtime_error(less_value, 'Substring out of range')
        self.register_instruction(nodes.SubstringNode(
            result, str_value, index_value, length_value))
        instance = self.define_internal_local()
        self.register_instruction(nodes.ArgNode(result))
        self.register_instruction(nodes.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(nodes.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in ['type_name', 'abort', 'copy']]
        type_node.methods += [(name, self.to_function_name(name, 'String'))
                              for name in ['length', 'concat', 'substr']]
        type_node.methods += [('init', self.init_name('String'))]

    def __register_Bool(self):
        type_node = self.register_type('Bool')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Bool'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(nodes.AllocateNode('Bool', instance))
        self.register_instruction(nodes.SetAttrNode(
            instance, 'value', 'val', 'Bool'))
        self.register_instruction(nodes.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in ['type_name', 'abort', 'copy']]
        type_node.methods += [('init', self.init_name('Bool'))]
