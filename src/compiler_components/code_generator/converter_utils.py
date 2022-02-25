from .cil_nodes import *
import queue


def define_internal_local(converter):
    var_info = VariableInfo('internal', None)
    return register_local(converter, var_info)


def get_preorder_types(converter, typex):
    ret_lis = []

    for son in typex.sons:
        ret_lis.extend(get_preorder_types(converter, son))

    ret_lis.append(typex)
    return ret_lis


def get_attr(converter, function_name, attribute):
    for dottype in converter.dottypes:
        if dottype.name == function_name:
            break

    return dottype.attributes.index(to_attribute_name(attribute))


def get_method(converter, type_name, method_name):
    for typeContext in converter.context.types:
        if typeContext == type_name:
            break

    methods = list(converter.context.types[typeContext].all_methods())

    for m in methods:
        if m[0].name == method_name:
            break

    return methods.index(m)


def box(converter, typeName, value):
    obj_internal = define_internal_local(converter)
    register_instruction(converter, CilAllocateNode(typeName, obj_internal))
    register_instruction(converter, CilSetAttribNode(obj_internal, 0, value))
    register_instruction(converter, CilLoadNode(obj_internal, f'{typeName}_name'))
    register_instruction(converter, CilLoadIntNode(obj_internal, f'{typeName}_size', 4))
    register_instruction(converter, CilLoadNode(obj_internal, f'__virtual_table__{typeName}', 8))
    return obj_internal


def to_function_name(method_name, type_name):
    return f'function_{method_name}_at_{type_name}'


def to_attribute_name(attr_name):
    return f'attribute_{attr_name}'


def register_param(converter, var_info):
    var_info.cilName = var_info.name
    param_node = CilParamNode(var_info.cilName)
    converter.params.append(param_node)
    return var_info.cilName


def register_local(converter, var_info):
    var_info.cilName = f'local_{converter.current_function.name[9:]}_{var_info.name}_{len(converter.localvars)}'
    local_node = CilLocalNode(var_info.cilName)
    converter.localvars.append(local_node)
    return var_info.cilName


def register_label(converter):
    name = f'label_{converter.current_function.name[9:]}_{len(converter.labels)}'
    converter.labels.append(name)
    return name


def register_instruction(converter, instruction):
    converter.instructions.append(instruction)
    return instruction


def register_function(converter, function_name):
    function_node = CilFunctionNode(function_name, [], [], [], [])
    converter.dotcode.append(function_node)
    return function_node


def register_type(converter, name):
    type_node = CilTypeNode(name)
    converter.dottypes.append(type_node)
    return type_node


def register_data(converter, value):
    for dataNode in converter.dotdata:
        if dataNode.value == value:
            return dataNode

    vname = f'data_{len(converter.dotdata)}'
    data_node = CilDataNode(vname, value)
    converter.dotdata.append(data_node)
    return data_node


def sort_types(types):
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


def basic_types(converter):
    for basicType in ['Int', 'String', 'Bool']:
        cil_type = register_type(converter, basicType)
        cil_type.attributes.append(to_attribute_name('value'))

        for method, typeMethod in converter.context.get_type(basicType).all_methods():
            cil_type.methods.append((method.name, to_function_name(method.name, typeMethod.name)))

    for basicType in ['Object', 'IO']:
        cil_type = register_type(converter, basicType)
        for method, typeMethod in converter.context.get_type(basicType).all_methods():
            cil_type.methods.append((method.name, to_function_name(method.name, typeMethod.name)))


class VariableInfo:
    def __init__(self, name, typex):
        self.name = name
        self.type = typex
