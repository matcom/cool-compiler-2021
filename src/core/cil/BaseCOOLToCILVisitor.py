from ..cil import CILAst as cil
from ..tools.Semantic import VariableInfo


class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.types_map = {}
        self.current_type = None
        self.current_method = None
        self.current_function = None

        self.context = context
        self.vself = VariableInfo('self', None)
        self.value_types = ['String', 'Int', 'Bool']

        self.var_names = {}

        self.breakline_data = self.register_data('\n', 0, 0)
        self.emptystring_data = self.register_data('', 0, 0)

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

    def register_param(self, vinfo, line, column):
        name = f'local_param_{self.current_function.name}_{vinfo.name}_{len(self.params)}'
        param_node = cil.ParamNode(name, line, column)
        self.params.append(param_node)
        self.var_names[vinfo.name] = name
        return name

    def register_local(self, vinfo, line, column):
        name = vinfo.name
        vinfo.name = f'local_{self.current_function.name}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name, line, column)
        self.localvars.append(local_node)
        self.var_names[name] = vinfo.name
        return vinfo.name

    def register_attribute(self, name, type, line, column):
        name =  f'attr_{type}_{name}'
        return cil.AttributeNode(name, line, column)


    def define_internal_local(self, line, column):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo, line, column)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def register_function(self, function_name, line, column):
        function_node = cil.FunctionNode(function_name, [], [], [], line, column)
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name, line, column):
        type_node = cil.TypeNode(name, line, column)
        self.types_map[name] = type_node
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value, line, column):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value, line, column)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label, line, column):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return cil.LabelNode(lname, line, column)

    def init_name(self, name):
        return f'init_at_{name}'

    def init_attr_name(self, name):
        return f'init_attr_at_{name}'

    def register_runtime_error(self, condition, msg, line, column):
        error_node = self.register_label('error_label', line, column)
        continue_node = self.register_label('continue_label', line, column)
        self.register_instruction(cil.GotoIfNode(condition, error_node.label, line, column))
        self.register_instruction(cil.GotoNode(continue_node.label, line, column))
        self.register_instruction(error_node)
        data_node = self.register_data(msg, line, column)
        self.register_instruction(cil.ErrorNode(data_node, line, column))
        self.register_instruction(continue_node)

    def register_builtin(self):
        # Object
        line, column = 0, 0
        type_node = self.register_type('Object', line, column)

        self.current_function = self.register_function(self.init_name('Object'), line, column)
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.AllocateNode('Object', instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('abort', 'Object'), line, column)
        self_param = self.register_param(self.vself, line, column)
        vname = self.define_internal_local(line, column)
        abort_data = self.register_data('Abort called from class ', line, column)
        self.register_instruction(cil.LoadNode(vname, abort_data, line, column))
        self.register_instruction(cil.PrintStringNode(vname, line, column))
        self.register_instruction(cil.TypeOfNode(vname, self_param, line, column))
        self.register_instruction(cil.PrintStringNode(vname, line, column))
        self.register_instruction(cil.LoadNode(vname, self.breakline_data, line, column))
        self.register_instruction(cil.PrintStringNode(vname, line, column))
        self.register_instruction(cil.ExitNode())

        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'), line, column)
        self_param = self.register_param(self.vself, line, column)
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.TypeOfNode(result, self_param, line, column))
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('copy', 'Object'), line, column)
        self_param = self.register_param(self.vself, line, column)
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.CopyNode(result, self_param, line, column))
        self.register_instruction(cil.ReturnNode(result, line, column))

        type_node.methods = {name: self.to_function_name(name, 'Object') for name in ['abort', 'type_name', 'copy']}
        type_node.methods['init'] = self.init_name('Object')
        obj_methods = ['abort', 'type_name', 'copy']

        # IO
        type_node = self.register_type('IO', line, column)

        self.current_function = self.register_function(self.init_name('IO'), line, column)
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.AllocateNode('IO', instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'), line, column)
        self_param = self.register_param(self.vself, line, column)
        x = self.register_param(VariableInfo('x', None), line, column)
        vname = self.define_internal_local(line, column)
        self.register_instruction(cil.GetAttribNode(vname, x, 'value', 'String', line, column))
        self.register_instruction(cil.PrintStringNode(vname, line, column))
        self.register_instruction(cil.ReturnNode(self_param, line, column))

        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'), line, column)
        self_param = self.register_param(self.vself, line, column)
        x = self.register_param(VariableInfo('x', None), line, column)
        vname = self.define_internal_local(line, column)
        self.register_instruction(cil.GetAttribNode(vname, x, 'value', 'Int', line, column))
        self.register_instruction(cil.PrintIntNode(vname, line, column))
        self.register_instruction(cil.ReturnNode(self_param, line, column))

        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'), line, column)
        self_param = self.register_param(self.vself, line, column)
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.ReadStringNode(result, line, column))
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'), line, column)
        self_param = self.register_param(self.vself, line, column)
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.ReadIntNode(result, line, column))
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'IO') for name in
                              ['out_string', 'out_int', 'in_string', 'in_int']})
        type_node.methods['init'] = self.init_name('IO')

        # String
        type_node = self.register_type('String', line, column)
        type_node.attributes = {name:self.register_attribute(name, 'String', 0, 0) for name in ['value', 'length']}

        self.current_function = self.register_function(self.init_name('String'), line, column)
        val = self.register_param(VariableInfo('val', None), line, column)
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.AllocateNode('String', instance, line, column))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'String', line, column))
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.LengthNode(result, val, line, column))
        attr = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), attr, line, column))
        self.register_instruction(cil.SetAttribNode(instance, 'length', attr, 'String', line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('length', 'String'), line, column)
        self_param = self.register_param(self.vself, line, column)
        result = self.define_internal_local(line, column)
        self.register_instruction(cil.GetAttribNode(result, self_param, 'length', 'String', line, column))
        self.register_instruction(cil.ReturnNode(result, line, column))

        self.current_function = self.register_function(self.to_function_name('concat', 'String'), line, column)
        self_param = self.register_param(self.vself, line, column)
        s = self.register_param(VariableInfo('s', None), line, column)
        str_1 = self.define_internal_local(line, column)
        str_2 = self.define_internal_local(line, column)
        length_1 = self.define_internal_local(line, column)
        length_2 = self.define_internal_local(line, column)
        self.register_instruction(cil.GetAttribNode(str_1, self_param, 'value', 'String', line, column))
        self.register_instruction(cil.GetAttribNode(str_2, s, 'value', 'String', line, column))
        self.register_instruction(cil.GetAttribNode(length_1, self_param, 'length', 'String', line, column))
        self.register_instruction(cil.GetAttribNode(length_2, s, 'length', 'String', line, column))
        self.register_instruction(cil.GetAttribNode(length_1, length_1, 'value', 'Int', line, column))
        self.register_instruction(cil.GetAttribNode(length_2, length_2, 'value', 'Int', line, column))
        self.register_instruction(cil.PlusNode(length_1, length_1, length_2, line, column))

        result = self.define_internal_local(line, column)
        self.register_instruction(cil.ConcatNode(result, str_1, str_2, length_1, line, column))
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        self.current_function = self.register_function(self.to_function_name('substr', 'String'), line, column)
        self_param = self.register_param(self.vself, line, column)
        i = self.register_param(VariableInfo('i', None), line, column)
        l = self.register_param(VariableInfo('l', None), line, column)
        result = self.define_internal_local(line, column)
        index_value = self.define_internal_local(line, column)
        length_value = self.define_internal_local(line, column)
        length_attr = self.define_internal_local(line, column)
        length_substr = self.define_internal_local(line, column)
        less_value = self.define_internal_local(line, column)
        str_value = self.define_internal_local(line, column)
        self.register_instruction(cil.GetAttribNode(str_value, self_param, 'value', 'String', line, column))
        self.register_instruction(cil.GetAttribNode(index_value, i, 'value', 'Int', line, column))
        self.register_instruction(cil.GetAttribNode(length_value, l, 'value', 'Int', line, column))
        # Check Out of range error
        self.register_instruction(cil.GetAttribNode(length_attr, self_param, 'length', 'String', line, column))
        self.register_instruction(cil.PlusNode(length_substr, length_value, index_value, line, column))
        self.register_instruction(cil.LessNode(less_value, length_attr, length_substr, line, column))
        self.register_runtime_error(less_value, 'Substring out of range', line, column)
        self.register_instruction(cil.SubstringNode(result, str_value, index_value, length_value, line, column))
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.ArgNode(result, line, column))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance, line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'String') for name in ['length', 'concat', 'substr']})
        type_node.methods['init'] = self.init_name('String')

        # Int
        type_node = self.register_type('Int', line, column)
        type_node.attributes = {name:self.register_attribute(name, 'Int', 0, 0) for name in ['value']}

        self.current_function = self.register_function(self.init_name('Int'), line, column)
        val = self.register_param(VariableInfo('val', None), line, column)
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.AllocateNode('Int', instance, line, column))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'Int', line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        type_node.methods = {method:self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.init_name('Int')

        # Bool
        type_node = self.register_type('Bool', line, column)
        type_node.attributes = {name:self.register_attribute(name, 'Bool', 0, 0) for name in ['value']}

        self.current_function = self.register_function(self.init_name('Bool'), line, column)
        val = self.register_param(VariableInfo('val', None), line, column)
        instance = self.define_internal_local(line, column)
        self.register_instruction(cil.AllocateNode('Bool', instance, line, column))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'Bool', line, column))
        self.register_instruction(cil.ReturnNode(instance, line, column))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.init_name('Bool')


