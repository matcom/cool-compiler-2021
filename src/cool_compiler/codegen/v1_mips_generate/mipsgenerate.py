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
            if func in self.native_fun: 
                self.new_program.func[func]  = self.native_fun[func]()
            else:
                self.visit(self.cil_func[func])
        
        return self.new_program

    @visitor.when(AST.Function)
    def visit(self, node: AST.Function):
        new_func = ASTR.Func(node.name if not node.name == 'new_ctr_Main' else 'main')
        self.stack = []
        self.final_len_stack = len(node.param) + len(node.local) + 2
        self.local_push = 0
        
        for param in [AST.Param('Return $ra')] + node.param:
            new_func.cmd += self.visit(param)

        for _local in node.local + [AST.Local('$ra')]:
            new_func.cmd += self.visit(_local)

        new_func.cmd += (
            [ASTR.SW('$ra', "0($sp)")] + 
            [ASTR.Comment(f"Agrega $ra a la pila para salvar el punto de retorno de la funcion {node.name}")])

        for expr in node.expr:
            new_func.cmd += self.visit(expr)

        self.new_program.func[new_func.name] = new_func

    #stack_pointer = 0
    #bsp = self.base_stack_pointer
    def stack_index(self, name):
        return (len(self.stack) - self.stack.index(name) - 1) * 4

    @visitor.when(AST.Param)
    def visit(self, node: AST.Param):
        self.stack.append(node.x)
        return [ASTR.Header_Comment(f'Parametro {node.x} en stackpoiner + {(self.final_len_stack - len(self.stack)) * 4}')]  
   

    @visitor.when(AST.Local)
    def visit(self, node: AST.Local):
        self.stack.append(node.x)
        return [
            ASTR.AddI('$sp', '$sp', -4), 
            ASTR.Comment(
            f'Push local var {node.x} stackpointer {(self.final_len_stack - len(self.stack)) * 4}')
        ]

    @visitor.when(AST.ALLOCATE)
    def visit(self, node: AST.ALLOCATE):
        memory_dir = node.x
        _type = node.y

        stack_plus = self.stack_index(memory_dir) 
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
        
        stack_plus = self.stack_index(memory_dir)
        self.local_push += 1
        self.stack.append(memory_dir)

        return [
            ASTR.LW('$t0', f'{stack_plus}($sp)'),
            ASTR.Comment(f'Saca de la pila {node.x}'),
            ASTR.AddI('$sp', '$sp', -4),
            ASTR.SW('$t0', '0($sp)'),
            ASTR.Comment(f'Mete para la pila {node.x}'),
        ]        

    @visitor.when(AST.VCall)
    def visit(self, node: AST.VCall):
        memory_dest = node.x
        _type = node.y
        func = node.z

        self.func_list.append(func)
        self.stack = self.stack[0: len(self.stack) - self.local_push]
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.JAL(func),
            ASTR.Comment(f'Call a la function {func}'),
            ASTR.SW('$s0', f'{stack_plus}($sp)' ),
            ASTR.Comment(f'Save el resultado de la funcion que esta en $s0 pa la pila'),
        ]

    @visitor.when(AST.Return)
    def visit(self, node: AST.Return):
        if node.x == 0: 
            return [ASTR.LI('$v0', 10), ASTR.SysCall()]
        
        memory_dest = node.x
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.LW('$s0', f'{stack_plus}($sp)'),
            ASTR.Comment("Envia el resultado de la funcion en $s0"),
            ASTR.LW('$ra', f'{(len(self.stack) - 1)* 4}($sp)'),
            ASTR.Comment("Lee el $ra mas profundo de la pila para retornar a la funcion anterior"),
            ASTR.AddI('$sp', '$sp', len(self.stack) * 4),
            ASTR.Comment("Limpia la pila"),
            ASTR.JR('$ra')
        ]

    @visitor.when(AST.Load)
    def visit(self, node: AST.Load):
        memory_dest = node.x
        data_label = node.y
        
        self.new_program.data[data_label] = ASTR.Data('word', data_label, self.cil_data[data_label].value)
        stack_plus = self.stack_index(memory_dest)

        return [
            ASTR.LA('$t0', data_label),
            ASTR.SW('$t0', f'{stack_plus}($sp)')
        ]
    
    @visitor.when(AST.Comment)
    def visit(self, node: AST.Comment):
        return [ASTR.Comment(node.x)]