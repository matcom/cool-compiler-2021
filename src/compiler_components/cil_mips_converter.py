def register_param(self, vinfo):
    vinfo.cilName = vinfo.name  # f'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
    param_node = cil.ParamNode(vinfo.cilName)
    self.params.append(param_node)
    return vinfo.cilName


def register_local(self, vinfo):
    vinfo.cilName = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
    local_node = cil.LocalNode(vinfo.cilName)
    self.localvars.append(local_node)
    return vinfo.cilName


def register_label(self):
    name = f'label_{self.current_function.name[9:]}_{len(self.labels)}'
    self.labels.append(name)
    return name


def define_internal_local(self):
    vinfo = VariableInfo('internal', None)
    return self.register_local(vinfo)


def register_instruction(self, instruction):
    self.instructions.append(instruction)
    return instruction


def to_function_name(self, method_name, type_name):
    return f'function_{method_name}_at_{type_name}'


def to_attribute_name(self, attr_name, attr_type):
    return f'attribute_{attr_name}'


def register_function(self, function_name):
    function_node = cil.FunctionNode(function_name, [], [], [], [])
    self.dotcode.append(function_node)
    return function_node


def register_type(self, name):
    type_node = cil.TypeNode(name)
    self.dottypes.append(type_node)
    return type_node


def register_data(self, value):
    for dataNode in self.dotdata:
        if dataNode.value == value:
            return dataNode

    vname = f'data_{len(self.dotdata)}'
    data_node = cil.DataNode(vname, value)
    self.dotdata.append(data_node)
    return data_node


def get_attr(self, function_name, attribute):
    for dottype in self.dottypes:
        if dottype.name == function_name:
            break

    # for attrib in dottype.attributes:
    #     if self.to_attribute_name(attribute, None) == attrib:
    #         break

    return dottype.attributes.index(self.to_attribute_name(attribute, None))


def get_method(self, type_name, method_name):
    for typeContext in self.context.types:
        if typeContext == type_name:
            break

    methods = list(self.context.types[typeContext].all_methods())

    for m in methods:
        if m[0].name == method_name:
            break

    return methods.index(m)


def sort_types(self, types):
    q = queue.deque()
    lst = []
    for tp1 in types:
        if not any([x for x in types if x != tp1 and tp1.conforms_to(x)]):
            q.append(tp1)

    while len(q) != 0:
        tp = q.popleft()
        if tp in types:
            lst.append(tp)
        for s in tp.sons:
            q.append(s)
    lst = list(reversed(lst))
    return lst


def get_preordenTypes(self, typex):
    ret_lis = []

    for son in typex.sons:
        ret_lis.extend(self.get_preordenTypes(son))

    ret_lis.append(typex)
    return ret_lis


def box(self, typeName, value):
    obj_internal = self.define_internal_local()
    self.register_instruction(cil.AllocateNode(typeName, obj_internal))
    self.register_instruction(cil.SetAttribNode(obj_internal, 0, value))
    self.register_instruction(cil.LoadNode(obj_internal, f'{typeName}_name'))
    self.register_instruction(cil.LoadIntNode(obj_internal, f'{typeName}_size', 4))
    self.register_instruction(cil.LoadNode(obj_internal, f'__virtual_table__{typeName}', 8))
    return obj_internal