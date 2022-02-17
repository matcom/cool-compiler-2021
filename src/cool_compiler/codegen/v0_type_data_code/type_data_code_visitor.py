from cool_compiler.types.type import Type
from ...cmp import visitor
from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from . import type_data_code_ast as ASTR
from .type_data_code_ast import result, super_value

def parent_list(node: AST.CoolClass):
    parent_list = []
    parent = node.type
    while True:
        if parent is None: break
        parent_list.append(parent)
        parent = parent.parent

    parent_list.reverse()
    return parent_list

class CILGenerate: 
    def __init__(self, errors) -> None:
        self.errors = errors

    @visitor.on('node')
    def visit(node):
        return [ASTR.Sum(super_value, 'a', 'b')]

    @visitor.when(AST.Program)
    def visit(self, node: AST.Program):
        self.program = ASTR.Program()
        for cls in node.class_list:
            self.visit(cls)

        return self.program
    
    @visitor.when(AST.CoolClass)
    def visit(self, node: AST.CoolClass):
        self.currentType = ASTR.Type(node.type.name)
        self.currentClass = node.type
        self.program.add_type(self.currentType)

        for parent in parent_list(node):
            for attr in parent.attributes:
                self.currentType.attr_push(attr.name)
            for func in parent.methods:
                self.currentType.method_push(func.name, f'{parent.name}@{func.name}')

        for feat in node.feature_list:
            self.visit(feat)
    
    @visitor.when(AST.FuncDef)
    def visit(self, node: AST.FuncDef):
        self.currentFunc = ASTR.Function(f'{self.currentType.name}@{node.name}')
        self.program.add_func(self.currentFunc)

        self.currentFunc.param.append('self')
        for name, t_params in node.params:
            self.currentFunc.param_push(name, True)
        
        expr_list = self.visit(node.expr)
        self.currentFunc.local_push(result)
        cond = expr_list[-1].try_set_value(result)

        expr_list.append(ASTR.Return(result if cond else 'self'))

        self.currentFunc.expr = expr_list

    @visitor.when(AST.CastingDispatch)
    def visit(self, node: AST.CastingDispatch):
        instance_expr_list = self.visit(node.expr)
        instance_name = self.currentFunc.local_push(f'instance_{node.type.name}_to_{node.id}')
        instance_expr_list[-1].set_value(instance_name)

        arg_list = [instance_name]
        for i, param in enumerate(node.params):
            instance_expr_list += self.visit(param)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}')
            instance_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            instance_expr_list.append(ASTR.Arg(arg))
        
        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, node.id))
        return instance_expr_list
    
    @visitor.when(AST.Dispatch)
    def visit(self, node: AST.Dispatch):
        instance_expr_list = self.visit(node.expr)
        instance_name = self.currentFunc.local_push(f'instance_to_call_{node.id}')
        instance_expr_list[-1].set_value(instance_name)

        arg_list = [instance_name]

        for i, param in enumerate(node.params):
            instance_expr_list += self.visit(param)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}')
            instance_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            instance_expr_list.append(ASTR.Arg(arg))
        
        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, node.id))
        return instance_expr_list
    
    @visitor.when(AST.StaticDispatch)
    def visit(self, node: AST.StaticDispatch):
        arg_list = ['self']
        param_expr_list = []
        for i, param in enumerate(node.params):
            param_expr_list += self.visit(param)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}')
            param_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            param_expr_list.append(ASTR.Arg(arg))
        
        param_expr_list.append(ASTR.VCall(super_value, self.currentClass.name, node.id))
        return param_expr_list
    
    @visitor.when(AST.Str)
    def visit(self, node: AST.Str):
        name = self.program.add_data('string', node.item.name)
        return [ASTR.Load(super_value, name)]