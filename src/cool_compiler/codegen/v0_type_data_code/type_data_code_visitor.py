from cool_compiler.types.type import Type
from ...cmp import visitor
from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from . import type_data_code_ast as ASTR
from .type_data_code_ast import result, super_value, instance_to

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
        pass

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
        self.program.functions[self.currentFunc.name] = self.currentFunc

        self.currentFunc.param_push('self')
        for name, t_params in node.params:
            self.currentFunc.param_push(name)
        
        expr_list = self.visit(node.expr, result)
        self.currentFunc.local_push(result)
        cond = expr_list[-1].try_set_value(result)

        expr_list.append(ASTR.Return(result if cond else 'self'))

    @visitor.when(AST.CastingDispatch)
    def visit(self, node: AST.CastingDispatch):
        instance_expr_list = self.visit(node.expr)
        instance_name = self.currentFunc.local_push(f'instance_to_{node.type.name}_{node.id}')
        instance_expr_list[-1].set_value(instance_name)

        arg_list = [instance_name]
        for i, param in enumerate(node.params):
            param_expr_list = self.visit(param)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.type.name}_{node.id}')
            param_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
            instance_expr_list += param_expr_list
        
        for arg in arg_list:
            instance_expr_list.append(ASTR.Arg(arg))
        
        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, node.id))
        return instance_expr_list