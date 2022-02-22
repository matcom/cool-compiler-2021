from cool_compiler.types.type import Type
from ...cmp import visitor
from ..v0_type_data_code import type_data_code_ast as AST
from . import mipsgenerate_ast as ASTR
from ..v0_type_data_code.type_data_code_ast import result, super_value

class MipsGenerate: 
    def __init__(self, errors) -> None:
        self.func_list = ['new_ctr_Main']
        self.native_fun = {
            "IO_out_string": ASTR.Out_String
        }

    @visitor.on('node')
    def visit(node):
        pass

    @visitor.when(AST.Program)
    def visit(self, node: AST.Program):
        self.cil_data = node.data
        self.cil_type = node.types
        self.cil_func = node.functions

        self.new_program = ASTR.Program()

        for func in self.func_list:
            self.visit(self.cil_func[func])
        
        return self.new_program

    @visitor.when(AST.Function)
    def visit(self, node: AST.Function):
        if node.name in self.native_fun: 
            self.new_program[node.name]  = self.native_fun[node.name]()

        new_func = ASTR.Func(node.name if not node.name == 'new_ctr_Main' else 'main')
        self.stack_dir = {}
        self.stack_pointer = 0
        self.local_stack_pointer = 0

        for _local in node.local:
            new_func.cmd += self.visit(_local)

        new_func.cmd += self.visit(AST.Local('$ra')) + [AST.SW('$ra', "4($sp)")]

        for param in node.param:
            new_func.cmd += self.visit(param)

        for expr in node.expr:
            new_func.cmd += self.visit(expr)

        self.new_program.func[node.name] = new_func

    @visitor.when(AST.Param)
    def visit(self, node: AST.Param):
        self.stack_pointer += 4
        self.local_stack_pointer += 4
        self.stack_dir[node.x] = self.stack_pointer

    @visitor.when(AST.Local)
    def visit(self, node: AST.Local):
        self.stack_pointer += 4
        self.local_stack_pointer += 4
        self.stack_dir[node.x] = 0
        for key in self.stack_dir.keys():
            self.stack_dir[key] += 4

        return [ASTR.AddI('$sp', '$sp', -4)]

    @visitor.when(AST.ALLOCATE)
    def visit(self, node: AST.ALLOCATE):
        memory_dir = node.x
        _type = node.y

        stack_plus = self.stack_dir[memory_dir] 
        _len = len(self.cil_type[_type].attributes)

        return [
            ASTR.LI('$a0', _len),
            ASTR.LI('$v0', 9),
            ASTR.SysCall(),
            ASTR.SW('$v0', f'{stack_plus}($sp)')
        ]

    @visitor.when(AST.Arg)
    def visit(self, node: AST.Arg):
        memory_dir = node.x

        stack_plus = self.stack_dir[memory_dir] + (self.stack_pointer + self.local_stack_pointer)
        self.local_stack_pointer += 4

        return [
            ASTR.LW('$t0', f'{stack_plus}($sp)'),
            ASTR.SW('$t0', '0($sp)'),
            ASTR.AddI('$sp', '$sp', -4)
        ]        

    @visitor.when(AST.Call)
    def visit(self, node: AST.Call):
        memory_dest = node.x
        _type = node.y
        func = node.z

        self.func_list.append(func)
        stack_plus = self.stack_dir[memory_dest] + (self.stack_pointer + self.local_stack_pointer)
        self.local_stack_pointer = self.stack_pointer
    
        return [
            ASTR.JAL(func),
            ASTR.SW('$s0', f'{stack_plus}($sp)' )
        ]

    @visitor.when(AST.Return)
    def visit(self, node: AST.Return):
        if node.x == 0: 
            return [ASTR.LI('$v0', 10), ASTR.SysCall()]
        
        memory_dest = node.x
        stack_plus = self.stack_dir[memory_dest]

        return [
            ASTR.LW('$s0', f'{stack_plus}($sp)'),
            ASTR.LW('$ra', f'4($sp)'),
            ASTR.AddI('$sp', '$sp', stack_plus),
            ASTR.JR('$ra')
        ]

    @visitor.when(AST.Load)
    def visit(self, node: AST.Load):
        memory_dest = node.x
        data_label = node.y
        
        stack_plus = self.stack_dir[memory_dest]

        return [
            ASTR.LW('$t0', data_label),
            ASTR.SW('$t0', f'{stack_plus}($sp)')
        ]