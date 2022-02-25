from . import cil_ast as AST
from .cil_ast import *
import parser.ast as C_AST
import semantic.types as CT

datos = {}
g_locals = {}
g_data_locals = {}
g_typeof = {}
g_attr = {}
g_type = None


class CIL_block:
    def __init__(self, body, value):
        self.body = body
        self.value = value


def add_str_data(data: str):
    try:
        return datos[data]
    except KeyError:
        count = len(datos) + 1
        datos[data] = f'data_{count}'
        return datos[data]


def add_local(id=None):
    global g_locals
    id = f'local_{len(g_locals)}' if not id else id
    local = AST.LocalNode(id)
    g_locals[id] = local
    return local


labels_count = 0


def add_label():
    global labels_count
    labels_count += 1
    return f'label_{labels_count}'


def ast_to_cil(ast):
    if type(ast) == C_AST.ProgramNode:
        return program_cil_visitor(ast)
    raise Exception(f'AST root must be program')


def add_data_local(string_addr):
    try:
        return g_data_locals[string_addr], False
    except KeyError:
        local_data = add_local()
        g_data_locals[string_addr] = local_data
        return local_data, True


def get_typeof(obj):
    try:
        return g_typeof[obj], False
    except KeyError:
        type_local = add_local()
        g_typeof[obj] = type_local
        return type_local, True


def program_cil_visitor(program):
    code = []
    types = []
    built_in_code = []
    for t in CT.TypesByName:
        _type = AST.TypeNode(t)
        value = CT.TypesByName[t]
        g_attr[t] = []
        for attr in value.atributos():
            _type.attributes.append(attr.id)
            g_attr[t].append(attr.id)
        for method in value.metodos_heredados():
            _type.methods[method.id] = method.owner
        for method in value.my_method():
            _type.methods[method] = t
        if t not in ('SELF_TYPE', 'Object', 'IO', 'String', 'Bool', 'Int'):
            _type.methods['__init__'] = t
        types.append(_type)

    init_main = new_cil_visitor(C_AST.NewNode(None, None, 'Main'), 'self')
    body = init_main.body
    main_result = add_local('main_result')
    body.append(AST.ArgNode(init_main.value))
    body.append(AST.VCAllNode('Main', 'main', main_result))
    body.append(AST.ReturnNode(main_result))
    main_function = AST.FuncNode('main', [], [g_locals[k] for k in g_locals.keys()], body)
    built_in_code.append(main_function)

    for c in program.classes:
        code.append(init_instance(c.type, c.parent_type))
        for f in c.feature_nodes:
            if type(f) == C_AST.FuncDeclarationNode:
                fun = func_cil_visitor(c.type, f)
                code.append(fun)

    built_in_code += builder()
    data = [AST.DataNode(datos[data_value], data_value)
            for data_value in datos.keys()]

    data.append(AST.DataNode('data_abort', 'Abort called from class '))
    cil_program = AST.ProgramNode(types, data, code, built_in_code)
    return cil_program


def builder():
    return [int_cil_out(), 
            str_cil_out(),
            str_cil_in(),
            int_cil_in(),
            typeN_object_cil(),
            copy_cil(),
            length_cil(), 
            concat_cil(), 
            substring_cil(), 
            abort_cil(), 
            abort_str_cil(), 
            abort_int_cil(), 
            abort_bool_cil(), 
            typeN_bool_cil(), 
            typeN_int_cil(), 
            typeN_string_cil()]


def str_cil_out():
    return AST.FuncNode('IO_out_string', [AST.ParamNode('self'),  AST.ParamNode('str')], [], [AST.PrintNode('str'),  AST.ReturnNode('self')])


def int_cil_out():
    return AST.FuncNode('IO_out_int', [AST.ParamNode('self'),  AST.ParamNode('int')], [], [AST.PrintNode('int'),  AST.ReturnNode('self')])


def str_cil_in():
    return AST.FuncNode('IO_in_string', [AST.ParamNode('self')], [AST.LocalNode('read_result')], [AST.ReadNode(AST.LocalNode('read_result')),   AST.ReturnNode(AST.LocalNode('read_result'))])


def int_cil_in():
    return AST.FuncNode('IO_in_int', [AST.ParamNode('self')], [AST.LocalNode('int')], [AST.ReadIntNode(AST.LocalNode('int')),   AST.ReturnNode(AST.LocalNode('int'))])


def typeN_string_cil():
    str_addr = add_str_data('String')
    t, need_load = add_data_local(str_addr)
    body = [AST.LoadNode(str_addr, t)] if need_load else []
    return AST.FuncNode('String_type_name', [AST.ParamNode('self')], [t], body+[AST.ReturnNode(t)])


def typeN_int_cil():
    str_addr = add_str_data('Int')
    t, need_load = add_data_local(str_addr)
    body = [AST.LoadNode(str_addr, t)] if need_load else []
    return AST.FuncNode('Int_type_name', [AST.ParamNode('self')], [t], body+[AST.ReturnNode(t)])


def typeN_bool_cil():
    str_addr = add_str_data('Bool')
    t, need_load = add_data_local(str_addr)
    body = [AST.LoadNode(str_addr, t)] if need_load else []
    return AST.FuncNode('Bool_type_name', [AST.ParamNode('self')], [t], body+[AST.ReturnNode(t)])


def typeN_object_cil():
    t = AST.LocalNode('type')
    return AST.FuncNode('Object_type_name', [AST.ParamNode('self')], [t], [AST.TypeOfNode(t, 'self'),   AST.ReturnNode(t)])


def copy_cil():
    copy = AST.LocalNode('copy')
    return AST.FuncNode('Object_copy', [AST.ParamNode('self')], [copy], [AST.CopyNode('self', copy),   AST.ReturnNode(copy)])


def length_cil():
    result = AST.LocalNode('len_result')
    return AST.FuncNode('String_length', [AST.ParamNode('self')], [result], [AST.LengthNode('self', result),   AST.ReturnNode(result)])


def concat_cil():
    result = AST.LocalNode('concat_result')
    return AST.FuncNode('String_concat', [AST.ParamNode('self'),   AST.ParamNode('key')], [result], [AST.ConcatNode('self', 'key', result),   AST.ReturnNode(result)])


def substring_cil():
    result = AST.LocalNode('substring_result')
    return AST.FuncNode('String_substr', [AST.ParamNode('self'),   AST.ParamNode('i'),   AST.ParamNode('l')], [result], [AST.SubStringNode('self', 'i', 'l', result),   AST.ReturnNode(result)])


def abort_cil():
    return AST.FuncNode('Object_abort', [AST.ParamNode('self')], [], [AST.AbortNode()])


def abort_str_cil():
    return AST.FuncNode('String_abort', [AST.ParamNode('self')], [], [AST.AbortNode('String')])


def abort_bool_cil():
    return AST.FuncNode('Bool_abort', [AST.ParamNode('self')], [], [AST.AbortNode('Bool')])


def abort_int_cil():
    return AST.FuncNode('Int_abort', [AST.ParamNode('self')], [], [AST.AbortNode('Int')])


def func_cil_visitor(type_name, func):
    global g_locals, g_data_locals, g_typeof, labels_count, g_type
    name = f'{type_name}_{func.id}'
    params = [AST.ParamNode('self')]
    params += [AST.ParamNode(id) for (id, _) in func.params]
    g_locals = {}
    g_data_locals = {}
    g_typeof = {}
    g_type = type_name
    body = []
    instruction = expr_cil_visitor(func.expressions)
    body += instruction.body
    body.append(AST.ReturnNode(instruction.value))

    l_keys = (g_locals.copy()).keys()
    for k in l_keys:
        for p in func.params:
            if k == p[0]:
                g_locals.pop(k)

    return AST.FuncNode(name, params, [g_locals[k] for k in g_locals.keys()], body)


def expr_cil_visitor(expression):
    try:
        return __visitor__[type(expression)](expression)
    except:
        raise Exception(f'There is no visitor for {type(expression)}')


def order_cases(case_list):
    result = []
    while len(case_list):
        c_list = case_list[0]
        for branch in case_list[1:]:
            c_list = branch if CT.TypesByName[branch.type].order < CT.TypesByName[c_list.type].order else c_list
        result.append(c_list)
        case_list.remove(c_list)
    return result


def case_cil_visitor(case):
    body = []
    expr_cil = expr_cil_visitor(case.expr)
    body += expr_cil.body
    t = add_local()
    body.append(AST.GetTypeOrderNode(t, expr_cil.value))
    t_min = add_local()
    body.append(AST.GetTypeMinOrderNode(t_min, expr_cil.value))
    labels = [add_label() for _ in range(len(case.case_list))]
    value = add_local()
    l = order_cases(case.case_list)
    for i, branch in enumerate(l):
        order = CT.TypesByName[branch.type].order
        min_order = CT.TypesByName[branch.type].min_order

        first_comp_result = add_local()
        body.append(AST.LessNode(order, t, first_comp_result))
        body.append(AST.ConditionalGotoNode(first_comp_result, labels[i]))

        second_comp_result = add_local()
        body.append(AST.LessNode(t_min, min_order, second_comp_result))
        body.append(AST.ConditionalGotoNode(second_comp_result, labels[i]))

        val = add_local(branch.id)
        body.append(AST.AssignNode(val, expr_cil.value))
        branch_cil = expr_cil_visitor(
            branch.expr)
        body += branch_cil.body
        body.append(AST.AssignNode(value, branch_cil.value))
        body.append(AST.GotoNode(labels[len(l)-1]))
        body.append(AST.LabelNode(labels[i]))
    return CIL_block(body, value)


def assign_cil_visitor(assign):
    expr = expr_cil_visitor(assign.expr)
    if assign.id in g_attr[g_type]:
        index = g_attr[g_type].index(assign.id)
        body = expr.body + \
            [AST.SetAttrNode('self', assign.id, expr.value, index + 5)]
        return CIL_block(body, expr.value)
    else:
        val = add_local(assign.id)
        body = expr.body + [AST.AssignNode(val, expr.value)]
        return CIL_block(body, val)


def arith_cil_visitor(arith):
    left = expr_cil_visitor(arith.lvalue)
    right = expr_cil_visitor(arith.rvalue)
    result = add_local()
    body = left.body + right.body
    if type(arith) == C_AST.PlusNode:
        body.append(AST.PlusNode(left.value, right.value, result))
    elif type(arith) == C_AST.MinusNode:
        body.append(AST.MinusNode(left.value, right.value, result))
    elif type(arith) == C_AST.MultNode:
        body.append(AST.MultNode(left.value, right.value, result))
    elif type(arith) == C_AST.DivNode:
        body.append(AST.DivNode(left.value, right.value, result))

    return CIL_block(body, result)


def if_cil_visitor(_if):
    predicate = expr_cil_visitor(_if.if_expr)

    then = expr_cil_visitor(_if.then_expr)

    else_expression = expr_cil_visitor(
        _if.else_expr)

    label_1 = add_label()
    label_2 = add_label()
    value = add_local()

    body = predicate.body + [AST.ConditionalGotoNode(predicate.value, label_1)] + else_expression.body + [
        AST.AssignNode(value, else_expression.value),  AST.GotoNode(label_2),  AST.LabelNode(label_1)] + then.body + [
        AST.AssignNode(value, then.value),  AST.LabelNode(label_2)]

    return CIL_block(body, value)


def loop_cil_visitor(loop):
    predicate = expr_cil_visitor(loop.cond)

    loop_block = expr_cil_visitor(loop.body)

    value = add_local()

    predicate_label = add_label()
    loop_label = add_label()
    end_label = add_label()

    body = [AST.LabelNode(predicate_label)] + predicate.body + [AST.ConditionalGotoNode(predicate.value, loop_label),  AST.GotoNode(end_label),
                                                                   AST.LabelNode(loop_label)] + loop_block.body + [AST.GotoNode(predicate_label),  AST.LabelNode(end_label),  AST.AssignNode(value, 0)]

    return CIL_block(body, value)


def equal_cil_visitor(equal):
    left = expr_cil_visitor(equal.lvalue)
    right = expr_cil_visitor(equal.rvalue)
    
    tname_l = equal.lvalue.returned_type.name
    tname_r = equal.rvalue.returned_type.name

    result = add_local()
    value = add_local()

    comparison = AST.EqStringNode(left.value, right.value, result) if tname_l == 'String' and tname_r == 'String' else AST.EqualNode(left.value, right.value, result)

    body = left.body + right.body + [comparison, AST.AssignNode(value, result)]

    return CIL_block(body, value)


def less_cil_visitor(lessthan):
    left = expr_cil_visitor(lessthan.lvalue)
    right = expr_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = left.body + right.body + [AST.LessNode(left.value, right.value, value)]
    return CIL_block(body, value)


def lessequal_cil_visitor(lessthan):
    left = expr_cil_visitor(lessthan.lvalue)
    right = expr_cil_visitor(lessthan.rvalue)

    value = add_local()
    body = left.body + right.body + [AST.LessEqualNode(left.value, right.value, value)]
    return CIL_block(body, value)


def int_cil_visitor(integer):
    return CIL_block([], integer.value)


def bool_cil_visitor(b: C_AST.BoolNode):
    return CIL_block([], 1) if b.value else CIL_block([], 0)


def id_cil_visitor(id):
    try:
        val = g_locals[id.id]
        return CIL_block([], val)
    except:
        if id.id in g_attr[g_type]:
            result = add_local()
            index = g_attr[g_type].index(id.id)
            return CIL_block([AST.GetAttrNode('self', id.id, result, index + 5)], result)
        return CIL_block([], id.id)


def init_instance(t, parent=None):
    global g_type, g_locals, g_data_locals, g_typeof

    g_locals = {}
    g_data_locals = {}
    g_typeof = {}
    g_type = t
    body = []

    if parent and parent not in ('Object', 'IO', 'Int', 'Bool', 'String'):
        parent_init = add_local()
        body.append(AST.ArgNode('self'))
        body.append(AST.VCAllNode(parent, '__init__', parent_init))

    all_attr = CT.TypesByName[t].atributos()
    init_attr = CT.TypesByName[t].my_attribute()
    for index, attr in enumerate(init_attr, len(all_attr)-len(init_attr)+5):
        if attr.expression:
            attr_cil = expr_cil_visitor(attr.expression)
            body += attr_cil.body
            body.append(AST.SetAttrNode('self', attr.id, attr_cil.value, index))
        elif attr.attrType.name == 'String':
            val = add_local()
            body.append(AST.AllocateNode('String', val))
            body.append(AST.SetAttrNode('self', attr.id, val, index))
        elif attr.attrType.name not in ('Bool', 'Int'):
            init = new_cil_visitor(None, default_type=attr.attrType.name)
            body.extend(init.body)
            body.append(AST.SetAttrNode('self', attr.id, init.value, index))
        else:
            body.append(AST.SetAttrNode('self', attr.id, 0, index))

    body.append(AST.ReturnNode('self'))

    return AST.FuncNode(f'{t}___init__', [AST.ParamNode('self')], [g_locals[k] for k in g_locals.keys()], body)


def new_cil_visitor(new_node, val_id=None, default_type=None):
    value = add_local(val_id) if val_id else add_local()
    t = default_type if default_type else new_node.type
    body = [AST.TypeOfNode(t, 'self')] if t == 'SELF_TYPE' else []
    body.append(AST.AllocateNode(t, value))
    t_data = add_str_data(t)
    t_local = add_local()
    size_local = add_local()
    order_local = add_local()
    min_order_local = add_local()
    init_attr = CT.TypesByName[t].atributos()
    body.append(AST.LoadNode(t_data, t_local))
    body.append(AST.SetAttrNode(value, '@type', t_local))
    body.append(AST.AssignNode(size_local, (len(init_attr)+5)*4))
    body.append(AST.SetAttrNode(value, '@size', size_local, 1))
    body.append(AST.AssignNode(order_local, CT.TypesByName[t].order))
    body.append(AST.SetAttrNode(value, '@order', order_local, 3))
    body.append(AST.AssignNode(min_order_local, CT.TypesByName[t].min_order))
    body.append(AST.SetAttrNode(value, '@min_order', min_order_local, 4))

    if t not in ('IO', 'Object', 'Int', 'String', 'Bool'):
        body.append(AST.ArgNode(value))
        allocate_res = add_local()
        body.append(AST.VCAllNode(t, '__init__', allocate_res))
        return CIL_block(body, allocate_res)
    else:
        return CIL_block(body, value)


def isVoid_cil_visitor(isvoid):
    expr_cil = expr_cil_visitor(isvoid.val)
    body = expr_cil.body
    return CIL_block(body, 1) if not expr_cil.value else CIL_block(body, 0)


def string_cil_visitor(str):
    str_addr = add_str_data(str.value)
    str_id, _ = add_data_local(str_addr)
    body = [AST.LoadNode(str_addr, str_id)]
    return CIL_block(body, str_id)


def let_cil_visitor(let):
    body = []
    for attr in let.let_attrs:
        val = add_local(attr.id)
        if attr.expr:
            attr_cil = expr_cil_visitor(attr.expr)
            body += attr_cil.body
            body.append(AST.AssignNode(val, attr_cil.value))
        elif attr.type == 'String':
            body.append(AST.AllocateNode('String', val))
        elif attr.type not in ('Bool', 'Int'):
            init = new_cil_visitor(None, default_type=attr.type)
            body.extend(init.body)
            body.append(AST.AssignNode(val, init.value))
        else:
            body.append(AST.AssignNode(val, 0))
    expr_cil = expr_cil_visitor(let.expr)
    body += expr_cil.body
    return CIL_block(body, expr_cil.value)


def not_cil_visitor(not_node):
    expr_cil = expr_cil_visitor(
        not_node.val)
    value = add_local()
    end_label = add_label()
    body = expr_cil.body + [AST.AssignNode(value, 0),  AST.ConditionalGotoNode(expr_cil.value, end_label),
                            AST.AssignNode(value, 1),  AST.LabelNode(end_label)]
    return CIL_block(body, value)


def intComp_cil_visitor(not_node):
    expr_cil = expr_cil_visitor(not_node.val)
    value = add_local()
    body = expr_cil.body + [AST.NotNode(expr_cil.value, value)]
    return CIL_block(body, value)


def block_cil_visitor(block):
    body = []
    value = None
    for expr in block.expressions:
        expr_cil = expr_cil_visitor(expr)
        body += expr_cil.body
        value = expr_cil.value
    return CIL_block(body, value)


def func_call_cil_visitor(call):
    body = []
    t = add_local()
    returned = None
    if call.object:
        obj_cil = expr_cil_visitor(
            call.object)
        body += obj_cil.body
        obj = obj_cil.value
        returned = call.object.returned_type
        if returned and returned.name in ("String", "Int", "Bool"):
            call.type = returned.name
        else:
            body.append(AST.GetTypeAddrNode(t, obj))
    else:
        obj = 'self'
        body.append(AST.GetTypeAddrNode(t, obj))
    arg_values = []
    for arg in call.args:
        arg_cil = expr_cil_visitor(arg)
        body += arg_cil.body
        arg_values.append(arg_cil.value)
    body.append(AST.ArgNode(obj))
    for arg in arg_values:
        body.append(AST.ArgNode(arg))
    result = add_local()
    if not call.type:
        body.append(AST.VCAllNode(t, call.id, result))
    else:
        body.append(AST.VCAllNode(call.type, call.id, result))
    return CIL_block(body, result)


def optimization_locals(program: ProgramNode):
    for function in program.code:
        intervals = {}
        uFunctions = []
        for local in function.locals:
            start = 0
            for index, instruction in enumerate(function.body):
                if local in instruction.locals:
                    start = index
                    break
                else:
                    uFunctions.append(local)
                    continue
            end = start
            for index, instruction in enumerate(function.body[start:]):
                if local in instruction.locals:
                    end = start + index
            intervals[local] = (start, end)
        _checked = []
        for key in intervals.keys():
            start, end = intervals[key]
            _checked.append((start, end, key))
        final_locals = []
        if len(_checked) != 0:
            final_locals.append(_checked[0])
        for l in _checked[1:]:
            start, end, key = l
            for index in range(len(final_locals)):
                start1, end1, y = final_locals[index]
                if end1 < start:
                    uFunctions.append(key)
                    key.id = y.id
                    final_locals[index] = (start1, end, y)
                    break
                elif end < start1:
                    uFunctions.append(key)
                    key.id = y.id
                    final_locals[index] = (start, end1, y)
                    break
            else:
                final_locals.append(l)
        for uFunc in uFunctions:
            function.locals.remove(uFunc)

def remove_unused_locals(program: ProgramNode):
    for function in program.code:
        used_locals=[]
        for instruction in function.body:
            for local in instruction.locals:
                if local not in used_locals:
                    try:
                        if instruction.result.id != local.id:
                            used_locals.append(local)
                    except:
                            used_locals.append(local)
        body=(function.body).copy()
        for instruction in function.body:
            for local in instruction.locals:
                try:
                    if instruction.result.id==local.id and local not in used_locals and not isinstance(instruction, VCAllNode):
                        body.remove(instruction)
                except:
                    pass
        function.body=body
        function.locals=used_locals

__visitor__ = {
    C_AST.AssignNode: assign_cil_visitor,
    C_AST.BlockNode: block_cil_visitor,
    C_AST.BoolNode: bool_cil_visitor,
    C_AST.IfNode: if_cil_visitor,
    C_AST.WhileNode: loop_cil_visitor,
    C_AST.EqualNode: equal_cil_visitor,
    C_AST.NotNode: not_cil_visitor,
    C_AST.LetNode: let_cil_visitor,
    C_AST.NewNode: new_cil_visitor,
    C_AST.IntNode: int_cil_visitor,
    C_AST.StringNode: string_cil_visitor,
    C_AST.PlusNode: arith_cil_visitor,
    C_AST.MinusNode: arith_cil_visitor,
    C_AST.MultNode: arith_cil_visitor,
    C_AST.DivNode: arith_cil_visitor,
    C_AST.VarNode: id_cil_visitor,
    C_AST.FuncCallNode: func_call_cil_visitor,
    C_AST.IsVoidNode: isVoid_cil_visitor,
    C_AST.IntCompNode: intComp_cil_visitor,
    C_AST.LessThanNode: less_cil_visitor,
    C_AST.LessEqualNode: lessequal_cil_visitor,
    C_AST.CaseNode: case_cil_visitor,
}



