from utils.mip_utils import registers as r, operations as o, datatype as dt
import visitors.visitor as visitor
from cil_ast.cil_ast import *

#heeerreeee con heerrrre carrrill

class Function():
    def __init__(self, label, params, localvars):
        self.label = label
        self.localvars = localvars
        self.params = params
        self.instructions = []

    def to_str(self):
        code = f'{self.label}:\n'
        code += '\n'.join(i for i in self.instructions)
        return code
    
    def register_instruction(self, instruction):
        self.instructions.append(instruction)

    def register_instructions(self, instructions):
        self.instructions.extend(instructions)

    def find_location_param(self, name):
        index = self.params.index(name)
        offset = ((len(self.params) - 1) - index) * 4
        return '{}({})'.format(offset, r.fp)

    def find_location_local(self, name):
        index = self.localvars.index(name)
        offset = (len(self.localvars) + 2 - index) * 4
        return '{}({})'.format(-offset, r.fp)

    def find_var_loc(self, name):
        try:
            return self.find_location_param(name)
        except ValueError:
            return self.find_location_local(name)

class MType():
    def __init__(self, name, label, code, index, attrs, methods):
        self.name = name
        self.label = label
        self.index = index
        self.methods = methods
        self.attributes = attrs
        self.code = code

class DataHandler():
    def __init__(self, label, msg):
        self.label = label
        self.string = msg
        self.code = '{}: {} "{}"'.format(self.label, dt.asciiz, self.string)

class CILToMipsVisitor:
    def __init__(self):

        self.type_lab_cnt = 0
        self.data_lab_cnt = 0
        self.code_lab_cnt = 0
        self.stack_args = 0
        self._function_names = {}
        self._labels = {}
        
        self._data_section = {}
        self._types_section = {}
        self._functions_section = {}
        self._current_function : FunctionNode = None
    
    def register_instruction(self, instruction):
        self._current_function.register_instruction(instruction)

    def register_instructions(self, instructions):
        self._current_function.register_instructions( instructions)
    
    def build_type_label(self):
        self.type_lab_cnt += 1
        return f'type_{self.type_lab_cnt}'

    def build_data_label(self):
        self.data_lab_cnt += 1
        return f'data_{self.data_lab_cnt}'

    def build_code_label(self):
        self.code_lab_cnt += 1
        return f'label_{self.code_lab_cnt}'

    def start_function(self, name, function):
        self._functions_section[name] = function
        self._current_function = function
        self._labels = {}

    def end_function(self):
        self._current_function = None

    def register_label(self, label, new_label):
        self._labels[label] = new_label

    def get_label(self, label):
        return self._labels[label]
    
    def push_register(self, reg):
        move_stack = '{} {} {} {}'.format(o.addi, r.sp, r.sp, -4)
        save_location = '{}({})'.format(0, r.sp)
        save_register = '{} {} {}'.format(o.sw, reg, save_location)
        return [move_stack, save_register]

    def pop_register(self, reg):
        load_value = '{} {} {}({})'.format(o.lw, reg, 0, r.sp)
        move_stack = '{} {} {} {}'.format(o.addi, r.sp, r.sp, 4)
        return [load_value, move_stack]

    def initialize_object(self, reg1, reg2):
        instructions = []

        instructions.append('{} {} {} {}'.format(o.sll, reg1, reg1, 2))
        instructions.append('{} {} {}'.format(o.la, reg2, 'prototype_table'))
        instructions.append('{} {} {} {}'.format(o.add, reg2, reg2, reg1))
        instructions.append("{} {} {}({})".format(o.lw, reg2, 0, reg2))
        instructions.append("{} {} {}({})".format(o.lw, r.a0, 4, reg2))
        instructions.append('{} {} {} {}'.format(o.sll, r.a0, r.a0, 2))
        instructions.append('{} {}'.format(o.jal, "allocate"))
        instructions.append("{} {} {}".format(o.move, r.a2, r.a0))
        instructions.append("{} {} {}".format(o.move, r.a0, reg2))
        instructions.append("{} {} {}".format(o.move, r.a1, r.v0))
        instructions.append('{} {}'.format(o.jal, "copy"))
        
        return instructions

    def find_var_loc(self, node):
        if isinstance(node, AttributeNode):
            return '0({})'.format(r.sp)
        if isinstance(node, str):
            return self._current_function.find_var_loc(node)
        return self._current_function.find_var_loc(node.name)

    @visitor.on('node')
    def collector_fnames(self, node):
        pass

    @visitor.when(ProgramNode)
    def collector_fnames(self, node):
        for f in node.dotcode:
            self.collector_fnames(f)

    @visitor.when(FunctionNode)
    def collector_fnames(self, node):
        if node.name == "entry":
            self._function_names[node.name] = 'main'
        else:
            self._function_names[node.name] = node.name

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.collector_fnames(node)
        self._data_section["default_str"] = DataHandler("default_str", "")

        for i in node.dottypes:
            self.visit(i)
        for i in node.dotdata:
            self.visit(i)
        for i in node.dotcode:
            self.visit(i)

        data = f'.data\n' + '\n.word 0\n'.join(d.code for d in self._data_section.values()) + '\n'
        names_table = f"types_table:\n" + "\n".join([f".word {tp.name}" for tp in self._types_section.values()])
        proto_table = f"prototype_table:\n" + "\n".join([f" .word {tp.label}_prototype" for tp in self._types_section.values()])
        types_table = "\n\n\n".join([tp.code for tp in self._types_section.values()])
        code = '\n\n'.join(f.to_str() for f in self._functions_section.values()) + '\n'
        
        mipsCode = f'{data}\n\n{names_table}\n\n{proto_table}\n\n{types_table}\n\n\n.text\n.globl main\n{code}\n\n'
        mipsCode += '\n'+self.define_util_functions()
        
        return mipsCode

    @visitor.when(TypeNode)
    def visit(self, node):
        name_label = self.build_data_label()
        self._data_section[node.name] = DataHandler(name_label, node.name)

        type_label = self.build_type_label()
        methods = [self._function_names[key] for key in node.methods.values()]

        type_attrs = list(node.attributes.keys())
        
        _methods = "\n".join([f".word {m}" for m in methods])
        dispatch_table = f"{type_label}_dispatch:\n{_methods}"
        begin = f"{type_label}_prototype:\n.word {len(self._types_section)}\n.word {len(type_attrs) + 4}\n.word {type_label}_dispatch"
        attr = "\n".join([f'.word 0' for attr in type_attrs])
        end = f".word\t-1"
        proto = f"{begin}\n{attr}\n{end}" if attr != "" else f"{begin}\n{end}"

        code = f'{dispatch_table}\n\n{proto}'
    
        self._types_section[node.name] = MType(name_label, type_label, code, len(self._types_section), type_attrs, methods)

    @visitor.when(DataNode)
    def visit(self, node):
        label = self.build_data_label()
        self._data_section[node.name] = DataHandler(label, node.value)

    @visitor.when(FunctionNode)
    def visit(self, node):
        label = self._function_names[node.name]
        params = [param.name for param in node.params]
        localvars = [local.name for local in node.localvars]
        size_for_locals = len(localvars) * 4

        new_func = Function(label, params, localvars)
        self.start_function(node.name, new_func)

        for instruction in node.instructions:
            if isinstance(instruction, LabelNode):
                mips_label = self.build_code_label()
                self.register_label(instruction.label, mips_label)

        instructions = []
        instructions.extend(self.push_register(r.ra))
        instructions.extend(self.push_register(r.fp))
        instructions.append('{} {} {} {}'.format(o.addi, r.fp, r.sp, 8))
        instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, -size_for_locals))

        for i in node.instructions:
            instructions.extend(self.visit(i))

        instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, size_for_locals))
        instructions.extend(self.pop_register(r.fp))
        instructions.extend(self.pop_register(r.ra))

        if self._current_function.label != 'main':
            instructions.append('{} {}'.format(o.jr, r.ra))
        else:
            instructions.append('{} {} {}'.format(o.li, r.v0, 10))
            instructions.append('{}'.format(o.syscall))

        new_func.register_instructions( instructions)
        self.end_function()

    @visitor.when(AssignNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.source, VoidNode):
            register = r.zero
        elif isinstance(node.source, int):
            register = r.t0
            instructions.append('{} {} {}'.format(o.li, r.t0, int(node.source)))
        else:
            register = r.t0
            instructions.extend(self.visit(node.source))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.source)))
            if isinstance(node.source, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        if isinstance(node.dest, AttributeNode):
            self_var = self._current_function.params[0]
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(self_var)))

            index = self._types_section[node.dest.type].attributes.index(node.dest.name) + 3
            instructions.append('{} {} {} {}'.format(o.addi, r.t1, r.t1, index * 4))
            instructions.append('{} {} 0({})'.format(o.sw, register, r.t1))
        else:
            instructions.append('{} {} {}'.format(o.sw, register, self.find_var_loc(node.dest)))

        return instructions

    @visitor.when(PlusNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.left, int):
            instructions.append('{} {} {}'.format(o.li, r.t0, node.left))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
            if isinstance(node.left, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        if isinstance(node.right, int):
            instructions.append('{} {} {}'.format(o.li, r.t1, node.right))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
            if isinstance(node.right, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {} {}'.format(o.add, r.t0, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(MinusNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.left, int):
            instructions.append('{} {} {}'.format(o.li, r.t0, node.left))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
            if isinstance(node.left, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        if isinstance(node.right, int):
            instructions.append('{} {} {}'.format(o.li, r.t1, node.right))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
            if isinstance(node.right, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {} {}'.format(o.sub, r.t0, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(StarNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.left, int):
            instructions.append('{} {} {}'.format(o.li, r.t0, node.left))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
            if isinstance(node.left, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        if isinstance(node.right, int):
            instructions.append('{} {} {}'.format(o.li, r.t1, node.right))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
            if isinstance(node.right, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {} {}'.format(r.t0, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(DivNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.left, int):
            instructions.append('{} {} {}'.format(o.li, r.t0, node.left))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
            if isinstance(node.left, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        if isinstance(node.right, int):
            instructions.append('{} {} {}'.format(o.li, r.t1, node.right))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
            if isinstance(node.right, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {}'.format(o.div, r.t0, r.t1))
        instructions.append('{} {}'.format(o.mflo, r.t0))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(AllocateNode)
    def visit(self, node):
        instructions = []

        if isinstance(node.type, int):
            _type = node.type
        else:
            _type = self._types_section[node.type].index
        instructions.append('{} {} {}'.format(o.li, r.t0, _type))
        instructions.extend(self.initialize_object(r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(TypeOfNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.obj))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.obj)))
        if isinstance(node.obj, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} 0({})'.format(o.lw, r.t1, r.t0))
        instructions.append('{} {} {} {}'.format(o.sll, r.t1, r.t1, 2))
        instructions.append('{} {} {}'.format(o.la, r.t0, 'types_table'))
        instructions.append('{} {} {} {}'.format(o.add, r.t0, r.t0, r.t1))
        instructions.append('{} {} 0({})'.format(o.lw, r.t1, r.t0))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t1, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(StaticCallNode)
    def visit(self, node):
        instructions = []

        func_name = self._function_names[node.function]
        instructions.append('{} {}'.format(o.jal, func_name))
        if self.stack_args > 0:
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, self.stack_args * 4))
            self.stack_args = 0
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(DynamicCallNode)
    def visit(self, node):
        instructions = []

        _type = self._types_section[node.type]
        method = _type.methods.index(self._function_names[node.method])

        instructions.append('{} {} 0({})'.format(o.lw, r.t0, r.sp))
        instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        self.stack_args -= 1

        instructions.append('{} {} 8({})'.format(o.lw, r.t0, r.t0))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, method * 4, r.t0))
        instructions.append('{} {} {}'.format(o.jalr, r.ra, r.t0))

        if self.stack_args > 0:
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, self.stack_args * 4))
            self.stack_args = 0
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(ArgNode)
    def visit(self, node):
        instructions = []
        
        self.stack_args += 1
        if isinstance(node.name, int):
            instructions.append('{} {} {}'.format(o.li, r.t0, node.name))
        else:
            instructions.extend(self.visit(node.name))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.name)))
            if isinstance(node.name, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.extend(self.push_register(r.t0))
        
        return instructions

    @visitor.when(ReturnNode)
    def visit(self, node):
        instructions = []

        if node.value is None or isinstance(node.value, VoidNode):
            instructions.append('{} {} {}'.format(o.li, r.v0, 0))
        elif isinstance(node.value, int):
            instructions.append('{} {} {}'.format(o.li, r.v0, node.value))
        else:
            instructions.extend(self.visit(node.value))
            instructions.append('{} {} {}'.format(o.lw, r.v0, self.find_var_loc(node.value)))
            if isinstance(node.value, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        
        return instructions

    @visitor.when(LoadNode)
    def visit(self, node):
        instructions = []

        instructions.append('{} {} {}'.format(o.la, r.t0, self._data_section[node.msg.name].label))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(PrintStringNode)
    def visit(self, node):
        instructions = []
        
        instructions.append('{} {} {}'.format(o.li, r.v0, 4))
        instructions.extend(self.visit(node.str_addr))
        instructions.append('{} {} {}'.format(o.lw, r.a0, self.find_var_loc(node.str_addr)))
        if isinstance(node.str_addr, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{}'.format(o.syscall))
        
        return instructions

    @visitor.when(PrintIntNode)
    def visit(self, node):
        instructions = []
        
        instructions.append('{} {} {}'.format(o.li, r.v0, 1))
        instructions.extend(self.visit(node.value))
        instructions.append('{} {} {}'.format(o.lw, r.a0, self.find_var_loc(node.value)))
        if isinstance(node.value, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{}'.format(o.syscall))
        
        return instructions

    @visitor.when(ExitNode)
    def visit(self, node):
        instructions = []
        
        instructions.append('{} {} {}'.format(o.li, r.v0, 10))
        instructions.append('{}'.format(o.syscall))

        return instructions

    @visitor.when(CopyNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.value))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.value)))
        if isinstance(node.value, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} 4({})'.format(o.lw, r.a0, r.t0))
        instructions.append('{} {} {} {}'.format(o.sll, r.a0, r.a0, 2))
        instructions.append('{} {}'.format(o.jal, "allocate"))
        instructions.append('{} {} {}'.format(o.move, r.a2, r.a0))
        instructions.append('{} {} {}'.format(o.move, r.a0, r.t0))
        instructions.append('{} {} {}'.format(o.move, r.a1, r.v0))
        instructions.append('{} {}'.format(o.jal, "copy"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(GetAttribNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.obj))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.obj)))
        if isinstance(node.obj, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * 4
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, offset, r.t0))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t1, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(ErrorNode)
    def visit(self, node):
        instructions = []

        mips_label = self._data_section[node.data.name].label
        instructions.append('{} {} {}'.format(o.li, r.v0, 4))
        instructions.append('{} {} {}'.format(o.la, r.a0, mips_label))
        instructions.append('{}'.format(o.syscall))
        instructions.append('{} {} {}'.format(o.li, r.v0, 10))
        instructions.append('{}'.format(o.syscall))

        return instructions

    @visitor.when(ReadIntNode)
    def visit(self, node):
        instructions = []

        instructions.append('{} {} {}'.format(o.li, r.v0, 5))
        instructions.append('{}'.format(o.syscall))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(ReadStringNode)
    def visit(self, node):
        instructions = []

        instructions.append('{} {}'.format(o.jal, "read_string"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(SetAttribNode)
    def visit(self, node):
        instructions = []

        tp = self._types_section[node.computed_type]
        offset = (tp.attributes.index(node.attr) + 3) * 4

        instructions.extend(self.visit(node.obj))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.obj)))
        if isinstance(node.obj, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        if type(node.value) == int:
            instructions.append('{} {} {}'.format(o.li, r.t1, node.value))
        else:
            instructions.extend(self.visit(node.value))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.value)))
            if isinstance(node.value, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {} {}({})'.format(o.sw, r.t1, offset, r.t0))

        return instructions

    @visitor.when(LessNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.left))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
        if isinstance(node.left, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.extend(self.visit(node.right))
        instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
        if isinstance(node.right, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {} {}'.format(o.slt, r.t1, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t1, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(GotoIfNode)
    def visit(self, node):
        instructions = []

        mips_label = self.get_label(node.label)
        instructions.extend(self.visit(node.condition))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.condition)))
        if isinstance(node.condition, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {} {}'.format(o.bne, r.t0, r.zero, mips_label))
        
        return instructions

    @visitor.when(GotoNode)
    def visit(self, node):
        instructions = []
        
        mips_label = self.get_label(node.label)
        instructions.append('{} {}'.format(o.j, mips_label))
        
        return instructions

    @visitor.when(LabelNode)
    def visit(self, node):
        instructions = []
        
        mips_label = self.get_label(node.label)
        instructions.append('{}:'.format(mips_label))
        
        return instructions

    @visitor.when(SubstringNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.str_value))
        instructions.append('{} {} {}'.format(o.lw, r.a0, self.find_var_loc(node.str_value)))
        if isinstance(node.str_value, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        if type(node.index) == int:
            instructions.append('{} {} {}'.format(o.li, r.a1, node.index))
        else:
            instructions.extend(self.visit(node.index))
            instructions.append('{} {} {}'.format(o.lw, r.a1, self.find_var_loc(node.index)))
            if isinstance(node.index, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        if type(node.index) == int:
            instructions.append('{} {} {}'.format(o.li, r.a2, node.length))
        else:
            instructions.extend(self.visit(node.length))
            instructions.append('{} {} {}'.format(o.lw, r.a2, self.find_var_loc(node.length)))
            if isinstance(node.length, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {}'.format(o.jal, "substr"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(ConcatNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.prefix))
        instructions.append('{} {} {}'.format(o.lw, r.a0, self.find_var_loc(node.prefix)))
        if isinstance(node.prefix, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.extend(self.visit(node.suffix))
        instructions.append('{} {} {}'.format(o.lw, r.a1, self.find_var_loc(node.suffix)))
        if isinstance(node.suffix, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.extend(self.visit(node.length))
        instructions.append('{} {} {}'.format(o.lw, r.a2, self.find_var_loc(node.length)))
        if isinstance(node.length, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {}'.format(o.jal, "concat"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        
        return instructions

    @visitor.when(LengthNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.source))
        instructions.append('{} {} {}'.format(o.lw, r.a0, self.find_var_loc(node.source)))
        if isinstance(node.source, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {}'.format(o.jal, "length"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(EqualNode)
    def visit(self, node):
        instructions = []

        if type(node.left) == VoidNode:
            instructions.append('{} {} {}'.format(o.li, r.t0, 0))
        else:
            instructions.extend(self.visit(node.left))
            instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
            if isinstance(node.left, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        if type(node.right) == VoidNode:
            instructions.append('{} {} {}'.format(o.li, r.t1, 0))
        else:
            instructions.extend(self.visit(node.right))
            instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
            if isinstance(node.right, AttributeNode):
                instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {} {} {}'.format(o.seq, r.t0, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(NameNode)
    def visit(self, node):
        instructions = []

        instructions.append('{} {} {}'.format(o.la, r.t0, 'types_table'))

        tp_number = self._types_section[node.value].index
        instructions.append('{} {} {} {}'.format(o.addi, r.t0, r.t0, tp_number * 4))
        instructions.append('{} {} 0({})'.format(o.lw, r.t0, r.t0))
        
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(EqualStringNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.left))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
        if isinstance(node.left, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {}'.format(o.move, r.a0, r.t0))

        instructions.extend(self.visit(node.right))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.right)))
        if isinstance(node.right, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {}'.format(o.move, r.a1, r.t0))

        instructions.append('{} {}'.format(o.jal, "equal_str"))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.v0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(ComplementNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.value))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.value)))
        if isinstance(node.value, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {} {}'.format(o.not_bw, r.t0, r.t0))
        instructions.append('{} {} {} {}'.format(o.addi, r.t0, r.t0, 1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(LessEqualNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.left))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.left)))
        if isinstance(node.left, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.extend(self.visit(node.right))
        instructions.append('{} {} {}'.format(o.lw, r.t1, self.find_var_loc(node.right)))
        if isinstance(node.right, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        instructions.append('{} {} {} {}'.format(o.sle, r.t0, r.t0, r.t1))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(NotNode)
    def visit(self, node):
        instructions = []

        instructions.extend(self.visit(node.value))
        instructions.append('{} {} {}'.format(o.lw, r.t0, self.find_var_loc(node.value)))
        if isinstance(node.value, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))
        instructions.append('{} {} {}'.format(o.xori, r.t0, r.t0))
        instructions.extend(self.visit(node.dest))
        instructions.append('{} {} {}'.format(o.sw, r.t0, self.find_var_loc(node.dest)))
        if isinstance(node.dest, AttributeNode):
            instructions.append('{} {} {} {}'.format(o.addi, r.sp, r.sp, 4))

        return instructions

    @visitor.when(VarNode)
    def visit(self, node):
        return []

    @visitor.when(ParamNode)
    def visit(self, node):
        return []

    @visitor.when(AttributeNode)
    def visit(self, node):
        instructions = []

        self_var = self._current_function.params[0]
        instructions.append('{} {} {}'.format(o.lw, r.t4, self.find_var_loc(self_var)))

        index = self._types_section[node.type].attributes.index(node.name) + 3
        instructions.append('{} {} {}({})'.format(o.lw, r.t4, index * 4, r.t4))
        instructions.extend(self.push_register(r.t4))

        return instructions
    
    
    def allocate(self):
        instructions = []
        
        instructions.append('{}:'.format('allocate'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -12))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 8, r.sp))
        instructions.append('{} {} {}'.format(o.li, r.t0, 4))
        instructions.append('{} {} {}'.format(o.div, r.a0, r.t0))                                     
        instructions.append('{} {}'.format(o.mfhi, r.t1))
        instructions.append('{} {} {} {}'.format(o.sub, r.t0, r.t0, r.t1))
        instructions.append('{} {} {} {}'.format(o.add, r.a0, r.a0, r.t0))
        instructions.append('{} {} {}'.format(o.li, r.v0, 9))
        instructions.append('{}'.format(o.syscall))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 8, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 12))
        instructions.append('{} {}'.format(o.jr, r.ra))

        return instructions
    
    def copy(self):
        instructions = []
        
        instructions.append('{}:'.format('copy'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -16))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 12, r.sp))
        instructions.append('{}:'.format('while_copy'))
        instructions.append('{} {} {} {}'.format(o.beq, r.a2, r.zero, 'copy_end'))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 0, r.a0))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 0, r.a1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a0, r.a0, 4))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a1, r.a1, 4))
        instructions.append('{} {} {} {}'.format(o.addi, r.a2, r.a2, -4))
        instructions.append('{} {}'.format(o.j, 'while_copy'))
        instructions.append('{}:'.format('copy_end'))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 12, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 16))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def length(self):
        instructions = []
        
        instructions.append('{}:'.format('length'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -8))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 4, r.sp))
        instructions.append('{} {} {}'.format(o.move, r.t0, r.a0))
        instructions.append('{} {} {}'.format(o.move, r.v0, r.zero))
        instructions.append('{}:'.format('while_len'))
        instructions.append('{} {} {}({})'.format(o.lb, r.t1, 0, r.t0))
        instructions.append('{} {} {} {}'.format(o.beq, r.t1, r.zero, 'len_end'))
        instructions.append('{} {} {} {}'.format(o.addi, r.v0, r.v0, 1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t0, r.t0, 1))
        instructions.append('{} {}'.format(o.j, 'while_len'))
        instructions.append('{}:'.format('len_end'))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 4, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 8))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def substring(self):
        instructions = []
        
        instructions.append('{}:'.format('substr'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -32))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t3, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a1, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a2, 24, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.ra, 28, r.sp))
        instructions.append('{} {} {}'.format(o.move, r.t0, r.a0))
        instructions.append('{} {} {} {}'.format(o.add, r.t0, r.t0, r.a1))
        instructions.append('{} {} {}'.format(o.li, r.t1, 4))
        instructions.append('{} {} {}'.format(o.div, r.a2, r.t1))
        instructions.append('{} {}'.format(o.mfhi, r.t2))
        instructions.append('{} {} {} {}'.format(o.bne, r.t2, r.zero, 'substr_allign_size'))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.a2))
        instructions.append('{} {}'.format(o.j, 'substr_new_chunk'))
        instructions.append('{}:'.format('substr_allign_size'))
        instructions.append('{} {} {} {}'.format(o.sub, r.t1, r.t1, r.t2))
        instructions.append('{} {} {} {}'.format(o.add, r.t1, r.t1, r.a2))
        instructions.append('{}:'.format('substr_new_chunk'))
        instructions.append('{} {} {}'.format(o.move, r.a0, r.t1))
        instructions.append('{} {}'.format(o.jal, 'allocate'))
        instructions.append('{} {} {}'.format(o.move, r.t3, r.v0))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.zero))
        instructions.append('{}:'.format('while_substr_copy'))
        instructions.append('{} {} {} {}'.format(o.beq, r.t1, r.a2, 'substr_end'))
        instructions.append('{} {} {}({})'.format(o.lb, r.t2, 0, r.t0))
        instructions.append('{} {} {}({})'.format(o.sb, r.t2, 0, r.t3))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t0, r.t0, 1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t3, r.t3, 1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t1, r.t1, 1))
        instructions.append('{} {}'.format(o.j, 'while_substr_copy'))
        instructions.append('{}:'.format('substr_end'))
        instructions.append('{} {} {}({})'.format(o.sb, r.zero, 0, r.t3))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t3, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a1, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a2, 24, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.ra, 28, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 32))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def concat(self):
        instructions = []
        
        instructions.append('{}:'.format('concat'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -24))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a1, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.ra, 20, r.sp))
        instructions.append('{} {} {}'.format(o.move, r.t0, r.a0))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.a1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a0, r.a2, 1))
        instructions.append('{} {} {}'.format(o.li, r.t2, 4))
        instructions.append('{} {} {}'.format(o.div, r.a0, r.t2))
        instructions.append('{} {}'.format(o.mfhi, r.a0))
        instructions.append('{} {} {} {}'.format(o.bne, r.a0, r.zero, 'concat_allign_size'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a0, r.a2, 1))
        instructions.append('{} {}'.format(o.j, 'concat_size_allignned'))
        instructions.append('{}:'.format('concat_allign_size'))
        instructions.append('{} {} {} {}'.format(o.sub, r.t2, r.t2, r.a0))
        instructions.append('{} {} {} {}'.format(o.add, r.a0, r.a2, r.t2))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a0, r.a0, 1))
        instructions.append('{}:'.format('concat_size_allignned'))
        instructions.append('{} {}'.format(o.jal, 'allocate'))
        instructions.append('{} {} {}'.format(o.move, r.t2, r.v0))
        instructions.append('{} {}'.format(o.j, 'first_while_concat_copy'))
        instructions.append('{}:'.format('first_while_concat_copy'))
        instructions.append('{} {} {}({})'.format(o.lb, r.a0, 0, r.t0))
        instructions.append('{} {} {} {}'.format(o.beq, r.a0, r.zero, 'second_while_concat_copy'))
        instructions.append('{} {} {}({})'.format(o.sb, r.a0, 0, r.t2))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t0, r.t0, 1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t2, r.t2, 1))
        instructions.append('{} {}'.format(o.j, 'first_while_concat_copy'))
        instructions.append('{}:'.format('second_while_concat_copy'))
        instructions.append('{} {} {}({})'.format(o.lb, r.a0, 0, r.t1))
        instructions.append('{} {} {} {}'.format(o.beq, r.a0, r.zero, 'concat_end'))
        instructions.append('{} {} {}({})'.format(o.sb, r.a0, 0, r.t2))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t1, r.t1, 1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t2, r.t2, 1))
        instructions.append('{} {}'.format(o.j, 'second_while_concat_copy'))
        instructions.append('{}:'.format('concat_end'))
        instructions.append('{} {} {}({})'.format(o.sb, r.zero, 0, r.t2))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t2, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a1, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.ra, 20, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 24))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def read_string(self):
        instructions = []
        
        instructions.append('{}:'.format('read_string'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -28))
        instructions.append('{} {} {}({})'.format(o.sw, r.ra, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a1, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a2, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t2, 24, r.sp))
        instructions.append('{} {} {}'.format(o.li, r.t0, 8))
        instructions.append('{} {} {} {}'.format(o.addi, r.a0, r.t0, 4))
        instructions.append('{} {}'.format(o.jal, 'allocate'))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.v0))
        instructions.append('{} {} {}'.format(o.move, r.t2, r.zero))
        instructions.append('{}:'.format('while_read_string'))
        instructions.append('{} {} {} {}'.format(o.addu, r.a0, r.t1, r.t2))
        instructions.append('{} {} {} {}'.format(o.subu, r.a1, r.t0, r.t2))
        instructions.append('{} {} {} {}'.format(o.addu, r.t2, r.t2, r.a1))
        instructions.append('{} {}'.format(o.jal, 'read_string_up_to'))
        instructions.append('{} {} {} {}'.format(o.beq, r.v0, r.zero, 'read_string_not_finished'))
        instructions.append('{} {} {}'.format(o.move, r.v0, r.t1))
        instructions.append('{} {}'.format(o.j, 'end_read_string'))
        instructions.append('{}:'.format('read_string_not_finished'))
        instructions.append('{} {} {} {}'.format(o.sll, r.t0, r.t0, 1))
        instructions.append('{} {} {} {}'.format(o.addi, r.a0, r.t0, 4))
        instructions.append('{} {}'.format(o.jal, 'allocate'))
        instructions.append('{} {} {}'.format(o.move, r.a0, r.t1))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.v0))
        instructions.append('{} {} {}'.format(o.move, r.a1, r.v0))
        instructions.append('{} {} {}'.format(o.move, r.a2, r.t2))
        instructions.append('{} {}'.format(o.jal, 'copy'))
        instructions.append('{} {}'.format(o.j, 'while_read_string'))
        instructions.append('{}:'.format('end_read_string'))
        instructions.append('{} {} {}({})'.format(o.lw, r.ra, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a1, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a2, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t2, 24, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 28))
        instructions.append('{} {}'.format(o.jr, r.ra))
        instructions.append('{}:'.format('read_string_up_to'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -28))
        instructions.append('{} {} {}({})'.format(o.sw, r.ra, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t2, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t3, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t4, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t5, 24, r.sp))
        instructions.append('{} {} {}'.format(o.move, r.t0, r.a0))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.zero))
        instructions.append('{} {} {}'.format(o.li, r.t2, 10))
        instructions.append('{} {} {} {}'.format(o.addu, r.t3, r.t0, r.a1))
        instructions.append('{} {} {} {}'.format(o.addiu, r.a1, r.a1, 1))
        instructions.append('{} {} {}'.format(o.li, r.v0, 8))
        instructions.append('{}'.format(o.syscall))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 0, r.a0))
        instructions.append('{} {} {} {}'.format(o.beq, r.a0, r.zero, 'eol_terminated'))
        instructions.append('{} {} {}'.format(o.li, r.v0, 0))
        instructions.append('{}:'.format('eol_check'))
        instructions.append('{} {} {} {}'.format(o.beq, r.t0, r.t3, 'read_loop_continue'))
        instructions.append('{} {} {}({})'.format(o.lb, r.t1, 0, r.t0))
        instructions.append('{} {} {} {}'.format(o.beq, r.t1, r.t2, 'eol_terminated'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.t0, r.t0, 1))
        instructions.append('{} {}'.format(o.j, 'eol_check'))
        instructions.append('{}:'.format('eol_terminated'))
        instructions.append('{} {} {}({})'.format(o.sb, r.zero, 0, r.t0))
        instructions.append('{} {} {}'.format(o.li, r.v0, 1))
        instructions.append('{}:'.format('read_loop_continue'))
        instructions.append('{} {} {}({})'.format(o.lw, r.ra, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t2, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t3, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t4, 20, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t5, 24, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 28))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def string_equals(self):
        instructions = []
        
        instructions.append('{}:'.format('equal_str'))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, -24))
        instructions.append('{} {} {}({})'.format(o.sw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a0, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.a1, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t2, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.sw, r.t3, 20, r.sp))
        instructions.append('{} {} {}'.format(o.move, r.t0, r.a0))
        instructions.append('{} {} {}'.format(o.move, r.t1, r.a1))
        instructions.append('{}:'.format('while_equal_str'))
        instructions.append('{} {} {}({})'.format(o.lb, r.t2, 0, r.t0))
        instructions.append('{} {} {}({})'.format(o.lb, r.t3, 0, r.t1))
        instructions.append('{} {} {} {}'.format(o.bne, r.t2, r.t3, 'equal_str_different_strings'))
        instructions.append('{} {} {} {}'.format(o.beq, r.t2, r.zero, 'first_end_equal_str'))
        instructions.append('{} {} {} {}'.format(o.beq, r.t3, r.zero, 'second_end_equal_str'))
        instructions.append('{} {} {} {}'.format(o.addi, r.t1, r.t1, 1))
        instructions.append('{} {} {} {}'.format(o.addi, r.t0, r.t0, 1))
        instructions.append('{} {}'.format(o.j, 'while_equal_str'))
        instructions.append('{}:'.format('equal_str_different_strings'))
        instructions.append('{} {} {}'.format(o.move, r.v0, r.zero))
        instructions.append('{} {}'.format(o.j, 'equal_str_end'))
        instructions.append('{}:'.format('first_end_equal_str'))
        instructions.append('{} {} {} {}'.format(o.beq, r.t3, r.zero, 'second_end_equal_str'))
        instructions.append('{} {} {}'.format(o.move, r.v0, r.zero))
        instructions.append('{} {}'.format(o.j, 'equal_str_end'))
        instructions.append('{}:'.format('second_end_equal_str'))
        instructions.append('{} {} {}'.format(o.li, r.v0, 1))
        instructions.append('{}:'.format('equal_str_end'))
        instructions.append('{} {} {}({})'.format(o.lw, r.t0, 0, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t1, 4, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a0, 8, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.a1, 12, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t2, 16, r.sp))
        instructions.append('{} {} {}({})'.format(o.lw, r.t3, 20, r.sp))
        instructions.append('{} {} {} {}'.format(o.addiu, r.sp, r.sp, 24))
        instructions.append('{} {}'.format(o.jr, r.ra))
        
        return instructions
    
    def define_util_functions(self):
        # instructions = [self.allocate(), self.copy(), self.length(), self.substring(), self.concat(), self.read_string(), self.string_equals()]
        instructions = [self.allocate(), self.copy(), self.length(), self.concat(), self.substring(), self.string_equals(), self.read_string()]
        
        code = '\n\n'.join('\n'.join(i for i in j) for j in instructions)
        return code
        
