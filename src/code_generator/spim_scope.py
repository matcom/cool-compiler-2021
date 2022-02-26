import cmp.visitor as visitor
from .ast_CIL import *

WSIZE = 4

class MIPSScope:
    def __init__(self):
        self.types = {}
        self.functions = {}

    def __str__(self):
        r = ''
        for t, ti in self.types.items():
            r += f'{t}\n'
            r += f'{ti}\n\n'
        for f, cf in self.functions.items():
            r += f'{f}\n'
            r += f'{cf}\n\n'
        return r
            
            

class TypeInfo:
    def __init__(self, typex: CILTypeNode):
        # This is obvious 
        self.id = typex.id

        # Memory to allocate for an instance of the type
        self.size = (len(typex.attributes) + 1) * WSIZE 

        # Use this offset to calculate the attribute address, given the address of the instance will be attr_addr = inst_addr + WORD_SIZE * offset
        self.attrs_offset = {attr.id : i for i, attr in enumerate(typex.attributes)} 

        # Associates every method of the type to the label to call
        self.methods_offset = { m.id : i for i, m in enumerate(typex.methods) }
        
    def get_attr_addr(self, attr, register):
        offset = self.attrs_offset[attr]
        return f'{(offset + 1) * WSIZE}({register})'
    
    def get_method_addr(self, method, register):
        offset = self.methods_offset[method]
        return f'{(offset + 2) * WSIZE}({register})'
    
    def __str__(self):
        r = '--------------------Type----------------\n'
        r += f'Attrs : {self.attrs_offset}\n'
        r += f'Methods : {self.methods_offset}\n'
        r += '-------------------------------------------'
        return r

class ProcCallFrame:
    def __init__(self, nargs, nvars):
        self.nargs = nargs
        self.size = WSIZE * nvars
        self.args = {} # Associates each argument with the offset to be accessed in the stack
        self.vars = {} # Associates each parameter with the offset to be accessed in the stack
        self.arg_queue = []

    def push_arg(self, arg):
        self.arg_queue.append(arg)

    def clear_args(self):
        self.arg_queue = []


    def add_argument(self, idx):
        self.args[idx] = self.nargs - len(self.args)

    def add_variable(self, idx):
        self.vars[idx] = len(self.vars)

    def arg_addr(self, id):
        offset = self.args[id]
        return f'{(2 + offset) * WSIZE}($fp)'
    
    def var_addr(self, id):
        offset = self.vars[id]
        return f'-{offset * WSIZE}($fp)'

    def get_addr(self, id):
        try:
            return self.arg_addr(id)
        except KeyError:
            return self.var_addr(id)

    def __str__(self):
        r = '-------------- Frame -----------------\n'
        r += f'Size: {self.size}\n'
        r += f'Args: {self.args}\n'
        r += f'Vars: {self.vars}\n'
        r += '-----------------------------------------\n'
        return r

class MIPSScopeBuilder:
    def __init__(self):
        self.scope = MIPSScope()

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(CILProgramNode)
    def visit(self, node: CILProgramNode):
        for t in node.types:
            self.visit(t)

        for f in node.functions:
            self.visit(f)

        return self.scope

    @visitor.when(CILTypeNode)
    def visit(self, node: CILTypeNode):
        info = TypeInfo(node)
        self.scope.types[node.id] = info

    @visitor.when(CILFuncNode)
    def visit(self, node: CILFuncNode):
        frame = ProcCallFrame(len(node.params), len(node.locals))
        for p in node.params:
            frame.add_argument(p.id)
        for l in node.locals:
            frame.add_variable(l.id)
        self.scope.functions[node.id] = frame


        

