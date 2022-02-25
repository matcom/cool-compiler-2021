from gen_code import cil_ast as astCIL
from gen_code import ast as astmip
import re

def get_types():
    return TYPE

def get_type(name):
    try:
        return TYPE[name]
    except KeyError:
        return None

def free_stack(bytes):
    return [astmip.AdduInstruction('$sp', '$sp', bytes)]

def peek_stack(src, pos):
    return [astmip.LwInstruction(src, pos)]

def allocate_stack(bytes):
    return [astmip.SubuInstruction('$sp', '$sp', bytes)]

def push_stack(src, pos):
    return peek_stack('$t0', src)+[astmip.SwInstruction('$t0', pos)]

def save_address(key, value):    
    if type(value) is int:
        if value:
            ADDR[key] = f'{value}($sp)'
        else:
            ADDR[key] = f'($sp)'
    ADDR[key] = value

def reserva_tipos(types):
    total=0
    for i, node in enumerate(types):
        node.size_mips = (len(node.attributes) + 5) * 4
        node.code_mips = i
        total +=(len(node.methods) + 1) * 4
        node.attr_index_mips = {}
        for i, a in enumerate(node.attributes):
            node.attr_index_mips[a] = i + 1
        TYPE[node.type] = node
    return total

def programMIPS(program: astCIL.ProgramNode):
    global datos, __VT__

    q = program.types.copy()
    node = q.pop(0)
    if node.type != 'SELF_TYPE':
        raise Exception("unexpected first type")

    while len(q):
        node = q.pop(0)
        for method, type_impl in node.methods.items():
            if type_impl == node.type:
                __VT__[(node.type, method)] = f'{type_impl}_{method}'
            else:
                try:
                    __VT__[(node.type, method)] = __VT__[(type_impl, method)]
                except KeyError:
                    q.append(node)

    total=reserva_tipos(program.types)

    vt_space_code = reserve_virtual_tables_space(program, total)
    datos = [astmip.MIPSDataItem(d.id, astmip.AsciizInst(f'"{d.val}"'))
                for d in program.data]
    datos.append(astmip.MIPSDataItem('new_line', astmip.AsciizInst(f'"\\n"')))
    datos.extend(vt_space_code)
    data_section = astmip.MIPSDataSection(datos)
    functions = [function_to_mips_visitor(f)
                 for f in program.built_in_code + program.code]
    text_section = astmip.MIPSTextSection(functions)
    return astmip.MIPSProgram(data_section, text_section)

def main_instructions():
    instructions=[]
    types=get_types()
    for node in types.keys():
        __OFFSET_COUNT__=0
        for m in types[node].methods:
            instructions.append(astmip.LaInstruction('$t0', __VT__[(node, m)]))
            instructions.append(astmip.UswInstruction('$t0', f'vt_{node}+{get_function_offset(m)*4}'))
    return instructions

def reserve_virtual_tables_space(program: astCIL.ProgramNode, total):
    code = [astmip.MIPSDataItem(f'vt_{node.type}', astmip.SpaceInst(total))
            for node in program.types[1:]]     
    return code

def function_to_mips_visitor(function):
    global CURRENT_FUNCTION
    func = astmip.MIPSFunction(function.name, function.params, function.locals)

    CURRENT_FUNCTION = func
    if func.name=='main':
        for i in main_instructions():
            CURRENT_FUNCTION.append_instruction(i)
    for cil_inst in function.body:
        for mips_inst in instructionMIPS(cil_inst):
            CURRENT_FUNCTION.append_instruction(mips_inst)
    return func

def get_function_offset(function):
    global __OFFSET_COUNT__
    try:
        return __OFFSET__[function]
    except KeyError:
        __OFFSET__[function]=__OFFSET_COUNT__
        __OFFSET_COUNT__+=1
        return __OFFSET__[function]
        
def instructionMIPS(inst):
    try:
        return __visitors__[type(inst)](inst)
    except KeyError:
        print(f'There is no visitor for {type(inst)}')
    return []

def returnMIPS(ret: astCIL.ReturnNode):
    code = [astmip.Comment(str(ret))]
    if isinstance(ret.ret_value, int):
        code.append(astmip.LiInstruction('$v0', ret.ret_value))
    else:
        offset = CURRENT_FUNCTION.offset[str(ret.ret_value)]
        code.append(astmip.LwInstruction('$v0', f'{offset}($fp)'))
    code.extend(CURRENT_FUNCTION.end_instructions)
    return code

def readMIPS(read: astCIL.ReadNode):
    offset = CURRENT_FUNCTION.offset[str(read.result)]
    return [astmip.LiInstruction('$a0', BUFF),astmip.LiInstruction('$v0', 9),
        astmip.SyscallInstruction(),astmip.MoveInstruction('$a0', '$v0'),
        astmip.MoveInstruction('$t3', '$v0'),astmip.LiInstruction('$a1', BUFF),
        astmip.LiInstruction('$v0', 8),astmip.SyscallInstruction(),
        astmip.MIPSLabel('remove_nl_loop'),astmip.LbInstruction('$t0', '($a0)'),
        astmip.BeqzInstruction('$t0', 'end_loop'),astmip.LaInstruction('$t1', 'new_line'),
        astmip.LbInstruction('$t2', '($t1)'),astmip.BeqInstruction('$t0', '$t2', 'end_loop'),
        astmip.AdduInstruction('$a0', '$a0', 1),astmip.BInstruction('remove_nl_loop'),
        astmip.MIPSLabel('end_loop'),astmip.SbInstruction('$zero', '($a0)'),
        astmip.SwInstruction('$t3', f'{offset}($fp)')] 

def readIntMIPS(read: astCIL.ReadIntNode):
    addr = CURRENT_FUNCTION.offset[str(read.result)]
    code = [astmip.Comment(str(read)),astmip.LiInstruction('$v0', 5),
        astmip.SyscallInstruction(),astmip.SwInstruction('$v0', f'{addr}($fp)')]
    return code

def loadMIPS(load: astCIL.LoadNode):
    offset = CURRENT_FUNCTION.offset[str(load.result)]
    return [astmip.Comment(str(load)),astmip.LaInstruction('$t0', load.addr),
        astmip.SwInstruction('$t0', f'{offset}($fp)')]

def typeOfMIPS(typeof: astCIL.TypeOfNode):
    addrs = CURRENT_FUNCTION.offset[str(typeof.var)]
    t_addr = CURRENT_FUNCTION.offset[str(typeof.result)]
    return [astmip.Comment(str(typeof)),astmip.LwInstruction('$t0', f'{addrs}($fp)'),
        astmip.LwInstruction('$t1', '($t0)'),astmip.SwInstruction('$t1', f'{t_addr}($fp)') ]

def goToMIPS(goto: astCIL.GotoNode):
    return [astmip.Comment(str(goto)),astmip.BInstruction(goto.label)]

def lblMIPS(label: astCIL.LabelNode):
    return [astmip.Comment(str(label)),astmip.MIPSLabel(label.label_name)]

def starMIPS(star: astCIL.MultNode):
    code = [astmip.Comment(str(star))]
    if isinstance(star.left, int):
        code.append(astmip.LiInstruction('$t0', star.left))
    else:
        addrs = CURRENT_FUNCTION.offset[str(star.left)]
        code.append(astmip.LwInstruction('$t0', f'{addrs}($fp)'))
    if isinstance(star.right, int):
        code.append(astmip.LiInstruction('$t1', star.right))
    else:
        y_addr = CURRENT_FUNCTION.offset[str(star.right)]
        code.append(astmip.LwInstruction('$t1', f'{y_addr}($fp)'))
    z_addr = CURRENT_FUNCTION.offset[str(star.result)]
    return code + [astmip.MulInstruction('$t0', '$t0', '$t1'), astmip.SwInstruction('$t0', f'{z_addr}($fp)')]

def divMIPS(div: astCIL.DivNode):
    code = [astmip.Comment(str(div))]
    if isinstance(div.left, int):
        code.append(astmip.LiInstruction('$t0', div.left))
    else:
        addrs = CURRENT_FUNCTION.offset[str(div.left)]
        code.append(astmip.LwInstruction('$t0', f'{addrs}($fp)'))
    if isinstance(div.right, int):
        code.append(astmip.LiInstruction('$t1', div.right))
    else:
        y_addr = CURRENT_FUNCTION.offset[str(div.right)]
        code.append(astmip.LwInstruction('$t1', f'{y_addr}($fp)'))
    z_addr = CURRENT_FUNCTION.offset[str(div.result)]
    return code + [astmip.DivInstruction('$t0', '$t0', '$t1'), astmip.SwInstruction('$t0', f'{z_addr}($fp)')]

def minusMIPS(minus: astCIL.MinusNode):
    code = [astmip.Comment(str(minus))]
    if isinstance(minus.left, int):
        code.append(astmip.LiInstruction('$t0', minus.left))
    else:
        addrs = CURRENT_FUNCTION.offset[str(minus.left)]
        code.append(astmip.LwInstruction('$t0', f'{addrs}($fp)'))
    if isinstance(minus.right, int):
        code.append(astmip.LiInstruction('$t1', minus.right))
    else:
        y_addr = CURRENT_FUNCTION.offset[str(minus.right)]
        code.append(astmip.LwInstruction('$t1', f'{y_addr}($fp)'))
    z_addr = CURRENT_FUNCTION.offset[str(minus.result)]
    return code + [astmip.SubInstruction('$t0', '$t0', '$t1'), astmip.SwInstruction('$t0', f'{z_addr}($fp)')]

def plusMIPS(plus: astCIL.PlusNode):
    code = [astmip.Comment(str(plus))]
    if isinstance(plus.left, int):
        code.append(astmip.LiInstruction('$t0', plus.left))
    else:
        addrs = CURRENT_FUNCTION.offset[str(plus.left)]
        code.append(astmip.LwInstruction('$t0', f'{addrs}($fp)'))
    if isinstance(plus.right, int):
        code.append(astmip.LiInstruction('$t1', plus.right))
    else:
        y_addr = CURRENT_FUNCTION.offset[str(plus.right)]
        code.append(astmip.LwInstruction('$t1', f'{y_addr}($fp)'))
    z_addr = CURRENT_FUNCTION.offset[str(plus.result)]
    return code + [astmip.AddInstruction('$t0', '$t0', '$t1'), astmip.SwInstruction('$t0', f'{z_addr}($fp)')]

def notMIPS(notn: astCIL.NotNode):
    instructions = [astmip.Comment(str(notn))]
    if isinstance(notn.value, int):
        instructions.append(astmip.LiInstruction('$t0', notn.value))
    else:
        y_offset = CURRENT_FUNCTION.offset[str(notn.value)]
        instructions.append(astmip.LwInstruction('$t0', f'{y_offset}($fp)'))
    x_offset = CURRENT_FUNCTION.offset[str(notn.result)]
    return instructions + [astmip.NegInstruction('$t0', '$t0'),astmip.SwInstruction('$t0', f'{x_offset}($fp)')]

def lessMIPS(less: astCIL.LessNode):
    instructions = [astmip.Comment(str(less))]
    if isinstance(less.left, int):
        instructions.append(astmip.LiInstruction('$t0', less.left))
    else:
        y_offset = CURRENT_FUNCTION.offset[str(less.left)]
        instructions.append(astmip.LwInstruction('$t0', f'{y_offset}($fp)'))
    if isinstance(less.right, int):
        instructions.append(astmip.LiInstruction('$t1', less.right))
    else:
        z_offset = CURRENT_FUNCTION.offset[str(less.right)]
        instructions.append(astmip.LwInstruction('$t1', f'{z_offset}($fp)'))
    x_offset = CURRENT_FUNCTION.offset[str(less.result)]
    return instructions + [astmip.SltInstruction('$t0', '$t0', '$t1'),astmip.SwInstruction('$t0', f'{x_offset}($fp)')]

def notEqMIPS(eq:astCIL.EqualNode):
    instructions = [astmip.Comment(str(eq))]
    if isinstance(eq.left, int):
        instructions.append(astmip.LiInstruction('$t0', eq.left))
    else:
        y_offset = CURRENT_FUNCTION.offset[str(eq.left)]
        instructions.append(astmip.LwInstruction('$t0', f'{y_offset}($fp)'))

    if isinstance(eq.right, int):
        instructions.append(astmip.LiInstruction('$t1', eq.right))
    else:
        z_offset = CURRENT_FUNCTION.offset[str(eq.right)]
        instructions.append(astmip.LwInstruction('$t1', f'{z_offset}($fp)'))
    x_offset = CURRENT_FUNCTION.offset[str(eq.result)]
    return instructions + [astmip.SneInstruction('$t0', '$t0', '$t1'),astmip.SwInstruction('$t0', f'{x_offset}($fp)')]
    
def notEqInstMIPS(noteq:astCIL.NotEqualNode):
    y_offset = CURRENT_FUNCTION.offset[str(noteq.left)]
    z_offset = CURRENT_FUNCTION.offset[str(noteq.right)]
    x_offset = CURRENT_FUNCTION.offset[str(noteq.result)]
    return [astmip.Comment(str(noteq)),astmip.LwInstruction('$t0', f'{y_offset}($fp)'),
        astmip.LwInstruction('$t1', '($t0)'),astmip.LwInstruction('$t0', f'{z_offset}($fp)'),
        astmip.LwInstruction('$t2', '($t0)'),astmip.SneInstruction('$t0', '$t1', '$t2'),
        astmip.SwInstruction('$t0', f'{x_offset}($fp)')]

def copyMIPS(copy: astCIL.CopyNode):
    addrs = CURRENT_FUNCTION.offset[str(copy.val)]
    y_addr = CURRENT_FUNCTION.offset[str(copy.result)]
    return [astmip.Comment(str(copy)), astmip.LwInstruction('$a0', f'{addrs+8}($fp)'),
            astmip.LiInstruction('$v0', 9), astmip.SyscallInstruction(),
            astmip.SwInstruction('$v0', f'{y_addr}($fp)'),astmip.AdduInstruction('$t1', '$fp', addrs),
            astmip.AdduInstruction('$t2', '$fp', y_addr),astmip.MIPSLabel('copy_loop'),
            astmip.LwInstruction('$t0', '($t1)'),astmip.SwInstruction('$t0', '($t2)'),
            astmip.AdduInstruction('$t1', '$t1', 4),astmip.AdduInstruction('$t2', '$t2', 4),
            astmip.SubuInstruction('$a0', '$a0', 4),astmip.BeqzInstruction('$a0', 'end_copy_loop'),
            astmip.BInstruction('copy_loop'),astmip.MIPSLabel('end_copy_loop')]

def eqStringMIPS(eq:astCIL.EqualNode):
    global __EQUAL__
    y_offset = CURRENT_FUNCTION.offset[str(eq.left)]
    z_offset = CURRENT_FUNCTION.offset[str(eq.right)]
    x_offset = CURRENT_FUNCTION.offset[str(eq.result)]
    __EQUAL__+=1
    return [astmip.Comment(str(eq)),astmip.LwInstruction('$t0', f'{y_offset}($fp)'),
        astmip.LwInstruction('$t1', f'{z_offset}($fp)'),astmip.LiInstruction('$v0', 1),
        astmip.SwInstruction('$v0', f'{x_offset}($fp)'),astmip.MIPSLabel(f'equal_loop_{__EQUAL__}'),
        astmip.LbInstruction('$t2', '($t0)'),astmip.LbInstruction('$t3', '($t1)'),
        astmip.SeqInstruction('$t4', '$t2', '$t3'),astmip.BeqzInstruction('$t4', f'not_equal_{__EQUAL__}'),
        astmip.BeqzInstruction('$t2', f'end_loop_{__EQUAL__}'),astmip.AdduInstruction('$t0','$t0', 1),
        astmip.AdduInstruction('$t1', '$t1', 1),astmip.BInstruction(f'equal_loop_{__EQUAL__}'),
        astmip.BInstruction(f'end_loop_{__EQUAL__}'),astmip.MIPSLabel(f'not_equal_{__EQUAL__}'),
        astmip.LiInstruction('$v0', 0),astmip.SwInstruction('$v0', f'{x_offset}($fp)'),
        astmip.MIPSLabel(f'end_loop_{__EQUAL__}')]

def equalMIPS(eq:astCIL.EqualNode):
    instructions = [astmip.Comment(str(eq))]
    if isinstance(eq.left, int):
        instructions.append(astmip.LiInstruction('$t0', eq.left))
    else:
        y_offset = CURRENT_FUNCTION.offset[str(eq.left)]
        instructions.append(astmip.LwInstruction('$t0', f'{y_offset}($fp)'))
    if isinstance(eq.right, int):
        instructions.append(astmip.LiInstruction('$t1', eq.right))
    else:
        z_offset = CURRENT_FUNCTION.offset[str(eq.right)]
        instructions.append(astmip.LwInstruction('$t1', f'{z_offset}($fp)'))
    x_offset = CURRENT_FUNCTION.offset[str(eq.result)]
    return instructions + [astmip.SeqInstruction('$t0', '$t0', '$t1'),astmip.SwInstruction('$t0', f'{x_offset}($fp)')]

def lessEqMIPS(lesseq: astCIL.LessEqualNode):
    instructions = [astmip.Comment(str(lesseq))]
    if isinstance(lesseq.left, int):
        instructions.append(astmip.LiInstruction('$t0', lesseq.left))
    else:
        y_offset = CURRENT_FUNCTION.offset[str(lesseq.left)]
        instructions.append(astmip.LwInstruction('$t0', f'{y_offset}($fp)'))

    if isinstance(lesseq.right, int):
        instructions.append(astmip.LiInstruction('$t1', lesseq.right))
    else:
        z_offset = CURRENT_FUNCTION.offset[str(lesseq.right)]
        instructions.append(astmip.LwInstruction('$t1', f'{z_offset}($fp)'))
    x_offset = CURRENT_FUNCTION.offset[str(lesseq.result)]
    return instructions + [astmip.SleInstruction('$t0', '$t0', '$t1'),astmip.SwInstruction('$t0', f'{x_offset}($fp)')]

def setAttrMIPS(setattr: astCIL.SetAttrNode):
    code = [astmip.Comment(str(setattr))]
    if isinstance(setattr.val, int):
        code.append(astmip.LiInstruction('$t0', setattr.val))
    else:
        addrs = CURRENT_FUNCTION.offset[str(setattr.val)]
        code.append(astmip.LwInstruction('$t0', f'{addrs}($fp)'))
    y_addr = CURRENT_FUNCTION.offset[str(setattr.obj)]
    _attr = setattr.attr_index * 4
    return code + [astmip.LwInstruction('$t1', f'{y_addr}($fp)'),astmip.SwInstruction('$t0', f'{_attr}($t1)')]

def getAttrMIPS(getattr: astCIL.GetAttrNode):
    addrs = CURRENT_FUNCTION.offset[str(getattr.result)]
    y_addr = CURRENT_FUNCTION.offset[str(getattr.obj)]
    _attr = getattr.attr_index * 4
    return [astmip.Comment(str(getattr)),astmip.LwInstruction('$t0', f'{y_addr}($fp)'),
        astmip.LwInstruction('$t1', f'{_attr}($t0)'),astmip.SwInstruction('$t1', f'{addrs}($fp)')]

def typeAddressMIPS(get_type:astCIL.GetTypeAddrNode):
    addrs = CURRENT_FUNCTION.offset[str(get_type.var)]
    t_addr = CURRENT_FUNCTION.offset[str(get_type.result)]
    return [astmip.Comment(str(get_type)),astmip.LwInstruction('$t1', f'{addrs}($fp)'),
        astmip.LwInstruction('$t0', f'8($t1)'),astmip.SwInstruction('$t0', f'{t_addr}($fp)')]
    
def typeOrderMIPS(get_order:astCIL.GetTypeOrderNode):
    addrs = CURRENT_FUNCTION.offset[str(get_order.var)]
    t_addr = CURRENT_FUNCTION.offset[str(get_order.result)]
    return [astmip.Comment(str(get_order)),astmip.LwInstruction('$t1', f'{addrs}($fp)'),
        astmip.LwInstruction('$t0', f'12($t1)'),astmip.SwInstruction('$t0', f'{t_addr}($fp)')]
  
def typeOrderMMIPS(get_order:astCIL.GetTypeMinOrderNode):
    addrs = CURRENT_FUNCTION.offset[str(get_order.var)]
    t_addr = CURRENT_FUNCTION.offset[str(get_order.result)]
    return [astmip.Comment(str(get_order)),astmip.LwInstruction('$t1', f'{addrs}($fp)'),
        astmip.LwInstruction('$t0', f'16($t1)'),astmip.SwInstruction('$t0', f'{t_addr}($fp)')]

def assgMIPS(assign: astCIL.AssignNode):
    code = [astmip.Comment(str(assign))]
    addrs = CURRENT_FUNCTION.offset[str(assign.result)]
    if isinstance(assign.val, int):
        code.append(astmip.LiInstruction('$t0', assign.val))
    else:
        y_addr = CURRENT_FUNCTION.offset[str(assign.val)]
        code.append(astmip.LwInstruction('$t0', f'{y_addr}($fp)'))
    return code+[astmip.SwInstruction('$t0', f'{addrs}($fp)')]

def vcallMIPS(vcall: astCIL.VCAllNode):
    instructions = []
    instructions.append(astmip.Comment(str(vcall)))
    try:
        CURRENT_FUNCTION.used_regs.remove('v0')
    except KeyError:
        pass
    try:
        CURRENT_FUNCTION.used_regs.remove('sp')
    except KeyError:
        pass
    _space = len(CURRENT_FUNCTION.used_regs) * 4
    instructions.append(astmip.SubuInstruction('$sp', '$sp', _space))
    for i, reg in enumerate(CURRENT_FUNCTION.used_regs):
        instructions.append(astmip.SwInstruction(f'${reg}', f'{i*4}($sp)'))

    instructions.extend(CURRENT_FUNCTION.args_code)
    CURRENT_FUNCTION.args_code.clear()    
    try:
        type_local=CURRENT_FUNCTION.offset[str(vcall.type)]
        instructions.append(astmip.LwInstruction('$t0', f'{type_local}($fp)'))
        instructions.append(astmip.UlwInstruction('$t1', f'{__OFFSET__[vcall.method]*4}($t0)'))
        instructions.append(astmip.JalrInstruction('$t1'))
    except KeyError:
        instructions.append(astmip.JalInstruction(__VT__[(str(vcall.type), str(vcall.method))]))
    instructions.append(astmip.AdduInstruction(
        '$sp', '$sp', CURRENT_FUNCTION.args_count * 4))
    CURRENT_FUNCTION.args_count = 0
    for i, reg in enumerate(CURRENT_FUNCTION.used_regs):
        instructions.append(astmip.LwInstruction(f'${reg}', f'{i*4}($sp)'))
    instructions.append(astmip.AdduInstruction('$sp', '$sp', _space))
    try:
        ret_offset = CURRENT_FUNCTION.offset[str(vcall.result)]
        instructions.append(astmip.SwInstruction('$v0', f'{ret_offset}($fp)'))
    except KeyError:
        pass
    return instructions

def goToCondMIPS(goto: astCIL.ConditionalGotoNode):
    instructions = [astmip.Comment(str(goto))]
    if isinstance(goto.predicate, int):
        instructions.append(astmip.LiInstruction('$t0', goto.predicate))
    else:
        expression = CURRENT_FUNCTION.offset[str(goto.predicate)]
        instructions.append(astmip.LwInstruction(
            '$t0', f'{expression}($fp)'))
    return instructions + [astmip.BnezInstruction('$t0', goto.label)]

def mips_print(p: astCIL.PrintNode):
    offset = CURRENT_FUNCTION.offset[str(p.str)]
    code = [astmip.Comment(str(p)),astmip.LwInstruction('$a0', f'{offset}($fp)')]
    if p.str == 'int':
        code.append(astmip.LiInstruction('$v0', 1)) 
    elif p.str == 'str':
        code.append(astmip.LiInstruction('$v0', 4))
    code.append(astmip.SyscallInstruction()) 
    return code

def exitMIPS(abort: astCIL.AbortNode):
    instructions = [astmip.Comment(str(abort)),astmip.LaInstruction('$a0', 'data_abort'),
        astmip.LiInstruction('$v0', 4), astmip.SyscallInstruction()]
    if abort.type_name:
        datos.append(astmip.MIPSDataItem(f'abort_{abort.type_name}', astmip.AsciizInst(f'"{abort.type_name}"')))
        instructions.append(astmip.LaInstruction('$a0', f'abort_{abort.type_name}'))
    else:
        instructions.append(astmip.LwInstruction('$a0', f'($fp)'))
    return instructions + [astmip.LiInstruction('$v0', 4),astmip.SyscallInstruction(),
        astmip.LaInstruction('$a0', 'new_line'),astmip.LiInstruction('$v0', 4),
        astmip.SyscallInstruction(),astmip.LiInstruction('$v0', 10),
        astmip.SyscallInstruction()]

def parametMIPS(arg: astCIL.ArgNode):
    code = [astmip.Comment(str(arg))]
    if isinstance(arg.val, int):
        code.append(astmip.LiInstruction('$t0', arg.val))
    else:
        addr = CURRENT_FUNCTION.offset[str(arg.val)]
        code.append(astmip.LwInstruction('$t0', f'{addr}($fp)'))
    CURRENT_FUNCTION.args_code.extend(
        code + [astmip.SubuInstruction('$sp', '$sp', 4), astmip.SwInstruction('$t0', '($sp)')])
    CURRENT_FUNCTION.args_count += 1
    return []

def allocateMIPS(allocate: astCIL.AllocateNode):
    address = CURRENT_FUNCTION.offset[str(allocate.result)]
    if allocate.type=='String':
        size= BUFF
        code=[astmip.Comment(str(allocate)), astmip.LiInstruction('$a0', size),
            astmip.LiInstruction('$v0', 9),  astmip.SyscallInstruction(),
            astmip.SwInstruction('$v0', f'{address}($fp)')]        
    else:
        size = get_type(allocate.type).size_mips + 16
        code = [astmip.Comment(str(allocate)),astmip.LiInstruction('$a0', size),
            astmip.LiInstruction('$v0', 9),astmip.SyscallInstruction(),
            astmip.SwInstruction('$v0', f'{address}($fp)'),astmip.LaInstruction('$t0', f'vt_{allocate.type}'),
            astmip.SwInstruction('$t0', f'8($v0)')]
    return code

def lengthMIPS(length: astCIL.LengthNode):
    val = CURRENT_FUNCTION.offset[str(length.str)]
    result_val = CURRENT_FUNCTION.offset[str(length.result)]
    code = [astmip.Comment(str(length)),astmip.LwInstruction('$t2', f'{val}($fp)'),
        astmip.LiInstruction('$t1', 0),astmip.MIPSLabel('length_loop'),
        astmip.LbInstruction('$t0', '($t2)'),astmip.BeqzInstruction('$t0', 'end_length_loop'),
        astmip.AdduInstruction('$t2', '$t2', 1),astmip.AdduInstruction('$t1', '$t1', 1),
        astmip.BInstruction('length_loop'),astmip.MIPSLabel('end_length_loop'),
        astmip.SwInstruction('$t1', f'{result_val}($fp)')]
    return code

def concatString(concat: astCIL.ConcatNode):
    final = CURRENT_FUNCTION.offset[str(concat.result)]
    a_offset = CURRENT_FUNCTION.offset[str(concat.str_a)]
    b_offset = CURRENT_FUNCTION.offset[str(concat.str_b)]
    return [astmip.Comment(str(concat)),astmip.LwInstruction('$t2', f'{a_offset}($fp)'),
        astmip.LiInstruction('$t1', 0),astmip.MIPSLabel('concat_a_length_loop'),
        astmip.LbInstruction('$t0', '($t2)'),astmip.BeqzInstruction('$t0', 'concat_a_end_length_loop'),
        astmip.AdduInstruction('$t2', '$t2', 1),astmip.AdduInstruction('$t1', '$t1', 1),
        astmip.BInstruction('concat_a_length_loop'),astmip.MIPSLabel('concat_a_end_length_loop'),        
        astmip.LwInstruction('$t2', f'{b_offset}($fp)'),astmip.MIPSLabel('concat_b_length_loop'),
        astmip.LbInstruction('$t0', '($t2)'),astmip.BeqzInstruction('$t0', 'concat_b_end_length_loop'),
        astmip.AdduInstruction('$t2', '$t2', 1),astmip.AdduInstruction('$t1', '$t1', 1),
        astmip.BInstruction('concat_b_length_loop'),astmip.MIPSLabel('concat_b_end_length_loop'),        
        astmip.AdduInstruction('$a0', '$t1', 1),astmip.LiInstruction('$v0', 9),
        astmip.SyscallInstruction(),astmip.MoveInstruction('$t0', '$v0'),        
        astmip.LwInstruction('$t1', f'{a_offset}($fp)'),astmip.LwInstruction('$t2', f'{b_offset}($fp)'),
        astmip.MIPSLabel('concat_loop_a'),astmip.LbInstruction('$a0', '($t1)'),
        astmip.BeqzInstruction('$a0', 'concat_loop_b'),astmip.SbInstruction('$a0', '($t0)'),
        astmip.AdduInstruction('$t0', '$t0', 1),astmip.AdduInstruction('$t1', '$t1', 1),
        astmip.BInstruction('concat_loop_a'),astmip.MIPSLabel('concat_loop_b'),
        astmip.LbInstruction('$a0', '($t2)'),astmip.BeqzInstruction('$a0', 'end_concat'),
        astmip.SbInstruction('$a0', '($t0)'),astmip.AdduInstruction('$t0', '$t0', 1),
        astmip.AdduInstruction('$t2', '$t2', 1),astmip.BInstruction('concat_loop_b'),
        astmip.MIPSLabel('end_concat'),astmip.SbInstruction('$zero', '($t0)'),
        astmip.SwInstruction('$v0', f'{final}($fp)')] 

def subStringMIPS(ss: astCIL.SubStringNode):
    final=CURRENT_FUNCTION.offset[str(ss.result)]
    _string = CURRENT_FUNCTION.offset[str(ss.str)]
    index = CURRENT_FUNCTION.offset[str(ss.i)]
    _lenght = CURRENT_FUNCTION.offset[str(ss.len)]
    return [astmip.Comment(str(ss)),astmip.LwInstruction('$t0', f'{_string}($fp)'),        
        astmip.LwInstruction('$a0', f'{_lenght}($fp)'),astmip.AdduInstruction('$a0', '$a0', 1),
        astmip.LiInstruction('$v0', 9),astmip.SyscallInstruction(),
        astmip.MoveInstruction('$t1', '$v0'),astmip.LwInstruction('$t4', f'{index}($fp)'),
        astmip.LwInstruction('$t2', f'{_lenght}($fp)'),astmip.AdduInstruction('$t0', '$t0', '$t4'),
        astmip.MIPSLabel('substring_loop'),astmip.BeqzInstruction('$t2', 'end_substring_loop'),
        astmip.LbInstruction('$t3', '($t0)'),astmip.SbInstruction('$t3', '($t1)'),
        astmip.SubuInstruction('$t2', '$t2', 1),astmip.AdduInstruction('$t0', '$t0', 1),
        astmip.AdduInstruction('$t1', '$t1', 1),astmip.BInstruction('substring_loop'),
        astmip.MIPSLabel('end_substring_loop'),astmip.SbInstruction('$zero', '($t1)'),
        astmip.SwInstruction('$v0', f'{final}($fp)')]

register_pattern = re.compile(r'\$v[0-1]|\$a[0-3]|\$t[0-9]|\$s[0-7]')

def is_register(addr: str):
    return register_pattern.match(addr) != None

BUFF = 1024
datos = []
CURRENT_FUNCTION = None
__VT__ = {}
__OFFSET_COUNT__= 0
__OFFSET__={}
__EQUAL__=0
TYPE = {}
ADDR = {}
__visitors__ = {
    astCIL.GetAttrNode: getAttrMIPS, astCIL.SetAttrNode: setAttrMIPS,    
    astCIL.TypeOfNode: typeOfMIPS, astCIL.AssignNode: assgMIPS,
    astCIL.PrintNode: mips_print, astCIL.ReturnNode: returnMIPS,    
    astCIL.GotoNode: goToMIPS, astCIL.ConditionalGotoNode: goToCondMIPS,
    astCIL.NotNode: notMIPS, astCIL.LessNode: lessMIPS,
    astCIL.EqualNode: equalMIPS, astCIL.LessEqualNode: lessEqMIPS,
    astCIL.NotEqualNode:notEqMIPS, astCIL.NotEqInstanceNode:notEqInstMIPS, 
    astCIL.ArgNode: parametMIPS, astCIL.AllocateNode: allocateMIPS,
    astCIL.CopyNode: copyMIPS, astCIL.LabelNode: lblMIPS,
    astCIL.MultNode: starMIPS, astCIL.DivNode: divMIPS,    
    astCIL.MinusNode: minusMIPS,astCIL.PlusNode: plusMIPS,    
    astCIL.SubStringNode: subStringMIPS, astCIL.LengthNode: lengthMIPS,
    astCIL.GetTypeOrderNode:typeOrderMIPS, astCIL.GetTypeAddrNode: typeAddressMIPS, 
    astCIL.ConcatNode: concatString, astCIL.ReadNode: readMIPS,
    astCIL.ReadIntNode: readIntMIPS, astCIL.EqStringNode:eqStringMIPS,
    astCIL.LoadNode: loadMIPS, astCIL.VCAllNode: vcallMIPS,    
    astCIL.AbortNode: exitMIPS, astCIL.GetTypeMinOrderNode:typeOrderMMIPS     
}
