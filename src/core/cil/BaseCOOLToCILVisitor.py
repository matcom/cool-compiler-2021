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

        self.breakline_data = self.register_data('\n')
        self.emptystring_data = self.register_data('')

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
        name = vinfo.name
        vinfo.name = f'local_param_{self.current_function.name}_{name}_{len(self.params)}'
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        self.var_names[name] = vinfo.name
        return vinfo.name

    def register_local(self, vinfo):
        name = vinfo.name
        vinfo.name = f'local_{self.current_function.name}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        self.var_names[name] = vinfo.name
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.types_map[name] = type_node
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return cil.LabelNode(lname)

    def init_name(self, name):
        return f'init_at_{name}'

    def init_attr_name(self, name):
        return f'init_attr_at_{name}'

    def register_runtime_error(self, condition, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.GotoIfNode(condition, error_node.label))
        self.register_instruction(cil.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(cil.ErrorNode(data_node))
        self.register_instruction(continue_node)

    def register_builtin(self):
        # Object
        type_node = self.register_type('Object')

        self.current_function = self.register_function(self.init_name('Object'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Object', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self.register_param(self.vself)
        vname = self.define_internal_local()
        abort_data = self.register_data('Abort called from class ')
        self.register_instruction(cil.LoadNode(vname, abort_data))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.TypeOfNode(vname, self.vself.name))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.LoadNode(vname, self.breakline_data))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.ExitNode())

        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(result, self.vself.name))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        type_node.methods = {name: self.to_function_name(name, 'Object') for name in ['abort', 'type_name', 'copy']}
        type_node.methods['init'] = self.init_name('Object')
        obj_methods = ['abort', 'type_name', 'copy']

        # IO
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.init_name('IO'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('IO', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self.register_param(self.vself)
        x = self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, x, 'value', 'String'))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self.register_param(self.vself)
        x = self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, x, 'value', 'Int'))
        self.register_instruction(cil.PrintIntNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadStringNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'IO') for name in
                              ['out_string', 'out_int', 'in_string', 'in_int']})
        type_node.methods['init'] = self.init_name('IO')

        # String
        type_node = self.register_type('String')
        type_node.attributes = ['value', 'length']

        self.current_function = self.register_function(self.init_name('String'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('String', instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'String'))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, val))
        attr = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('Int'), attr))
        self.register_instruction(cil.SetAttribNode(instance, 'length', attr, 'String'))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(result, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self.register_param(self.vself)
        s = self.register_param(VariableInfo('s', None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        length_1 = self.define_internal_local()
        length_2 = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_1, self.vself.name, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(str_2, s, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(length_1, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(length_2, s, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(length_1, length_1, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(length_2, length_2, 'value', 'Int'))
        self.register_instruction(cil.PlusNode(length_1, length_1, length_2))

        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, str_1, str_2, length_1))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self.register_param(self.vself)
        i = self.register_param(VariableInfo('i', None))
        l = self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_value, self.vself.name, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(index_value, i, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(length_value, l, 'value', 'Int'))
        # Check Out of range error
        self.register_instruction(cil.GetAttribNode(length_attr, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.PlusNode(length_substr, length_value, index_value))
        self.register_instruction(cil.LessNode(less_value, length_attr, length_substr))
        self.register_runtime_error(less_value, 'Substring out of range')
        self.register_instruction(cil.SubstringNode(result, str_value, index_value, length_value))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'String') for name in ['length', 'concat', 'substr']})
        type_node.methods['init'] = self.init_name('String')

        # Int
        type_node = self.register_type('Int')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Int'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Int', instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'Int'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method:self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.init_name('Int')

        # Bool
        type_node = self.register_type('Bool')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Bool'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Bool', instance))
        self.register_instruction(cil.SetAttribNode(instance, 'value', val, 'Bool'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.init_name('Bool')


