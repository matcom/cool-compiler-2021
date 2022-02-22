from cool_compiler.cmp.scope import Scope
from cool_compiler.types.cool_type_build_in_manager import CoolTypeBuildInManager
from cool_compiler.types.type import Type
from ...cmp import visitor
from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from . import type_data_code_ast as ASTR
from .type_data_code_ast import result, super_value


CoolInt = CoolTypeBuildInManager().find("Int")
CoolBool = CoolTypeBuildInManager().find("Bool")
CoolStr = CoolTypeBuildInManager().find("String")


def parent_list(node: AST.CoolClass):
    parent_list = []
    parent = node.type
    while True:
        if parent is None: break
        parent_list.append(parent)
        parent = parent.parent

    parent_list.reverse()
    return parent_list

def new_name(name, _dict):
    index = 0
    while True:
        try: 
            _ = _dict[f'{name}@{index}']
            index += 1
        except KeyError:
            _dict[f'{name}@{index}'] = 1
            return f'{name}@{index}'

class CILGenerate: 
    def __init__(self, errors) -> None:
        self.errors = errors
        self.label_list = {}

    @visitor.on('node')
    def visit(node, scope: Scope):
        pass

    @visitor.when(AST.Program)
    def visit(self, node: AST.Program, scope: Scope = None):
        self.program = ASTR.Program()
        scope = Scope()
        for cls in node.class_list:
            self.visit(cls, scope)

        return self.program
    
    @visitor.when(AST.CoolClass)
    def visit(self, node: AST.CoolClass, scope: Scope):
        self.class_scope = scope.create_child(node.type.name)
        self.new_class_scope = scope.create_child(f'new_{node.type.name}')

        self.currentType = ASTR.Type(node.type.name)
        self.currentClass = node.type
        self.new_type_func = ASTR.Function(f'new_ctr_{node.type.name}')
        
        self.program.add_type(self.currentType)

        for parent in parent_list(node):
            for attr in parent.attributes:
                self.currentType.attr_push(attr.name, f'{parent.name}_{attr.name}')
            for func in parent.methods:
                self.currentType.method_push(func.name, f'{parent.name}_{func.name}')
        
        self.new_type_func.force_local('instance', self.new_class_scope)
        self.new_type_func.expr_push(ASTR.ALLOCATE('instance', node.type.name))

        for feat in node.feature_list:
            self.visit(feat, self.class_scope)

        if node.type.name == 'Main':
            self.new_type_func.force_local(result, self.new_class_scope)
            self.new_type_func.expr_push(ASTR.Arg('instance'))
            self.new_type_func.expr_push(ASTR.Call(result, 'Main', 'main_Main'))
            self.new_type_func.expr_push(ASTR.Return(0))
        else:
            self.new_type_func.expr_push(ASTR.Return('instance'))

        self.program.add_func(self.new_type_func)
    
    @visitor.when(AST.AtrDef)
    def visit(self, node: AST.AtrDef, scope: Scope):
        if not node.expr is None:
            save_current_func = self.currentFunc
            self.currentFunc = self.new_type_func
            attr_name = self.new_type_func.local_push(node.name, self.new_class_scope)
            exp_list = self.visit(node.expr, self.new_class_scope)
            exp_list[-1].set_value(attr_name)
            exp_list.append(ASTR.SetAttr('instance', self.currentType.attr[node.name], attr_name))
            self.new_type_func.expr += exp_list
            self.currentFunc = save_current_func


    @visitor.when(AST.FuncDef)
    def visit(self, node: AST.FuncDef, scope: Scope):
        func_scope = scope.create_child(node.name)
        self.currentFunc = ASTR.Function(f'{self.currentType.name}_{node.name}')
        self.program.add_func(self.currentFunc)

        self.currentFunc.force_parma('self', func_scope)
        for name, t_params in node.params:
            self.currentFunc.param_push(name, func_scope)

        expr_list = self.visit(node.expr, func_scope)
        self.currentFunc.force_local(result, func_scope)
        cond = expr_list[-1].try_set_value(result)

        expr_list.append(ASTR.Return(result if cond else 'self'))

        self.currentFunc.expr = expr_list

    @visitor.when(AST.CastingDispatch)
    def visit(self, node: AST.CastingDispatch, scope: Scope):
        instance_expr_list = self.visit(node.expr, scope)
        instance_name = self.currentFunc.local_push(f'instance_{node.type.name}_to_{node.id}', scope)
        instance_expr_list[-1].set_value(instance_name)

        arg_list = [instance_name]
        for i, param in enumerate(node.params):
            instance_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            instance_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            instance_expr_list.append(ASTR.Arg(arg))
        
        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, self.currentType.methods[node.id]))
        return instance_expr_list
    
    @visitor.when(AST.Dispatch)
    def visit(self, node: AST.Dispatch, scope: Scope):
        instance_expr_list = self.visit(node.expr, scope)
        instance_name = self.currentFunc.local_push(f'instance_to_call_{node.id}', scope)
        instance_expr_list[-1].set_value(instance_name)

        arg_list = [instance_name]

        for i, param in enumerate(node.params):
            instance_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            instance_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            instance_expr_list.append(ASTR.Arg(arg))
        
        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, self.currentType.methods[node.id]))
        return instance_expr_list
    
    @visitor.when(AST.StaticDispatch)
    def visit(self, node: AST.StaticDispatch, scope: Scope):
        arg_list = ['self']
        param_expr_list = []
        for i, param in enumerate(node.params):
            param_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            param_expr_list[-1].set_value(param_name)
            arg_list.append(param_name)
        
        for arg in arg_list:
            param_expr_list.append(ASTR.Arg(arg))
        
        param_expr_list.append(ASTR.VCall(super_value, self.currentClass.name, self.currentType.methods[node.id]))
        return param_expr_list
    

    @visitor.when(AST.Assing)
    def visit(self, node: AST.Assing, scope: Scope):
        exp_list = self.visit(node.expr, scope)
        result_local = self.currentFunc.local_push(f'result@assing@{node.id}', scope)
        exp_list[-1].set_value(result_local)
        
        var = scope.find_variable(node.id)
        if not var is None: 
            exp_list.append(ASTR.Assign(var.type, result_local))
            exp_list.append(ASTR.Assign(super_value, var.type))
        else:
            exp_list.append(ASTR.SetAttr('self', self.currentType.attr[node.id], result_local))
            exp_list.append(ASTR.GetAttr(super_value , 'self', self.currentType.attr[node.id]))

        return exp_list

    @visitor.when(AST.IfThenElse)
    def visit(self, node: AST.IfThenElse, scope: Scope):
        cond_result = self.currentFunc.local_push(f'cond@if_else', scope)

        expr_list = self.visit(node.condition, scope)
        expr_list[-1].set_value(cond_result)
        result_if = self.currentFunc.local_push('result@if', scope)

        label_then = new_name(f'then@{self.currentFunc.name}')
        label_fin = new_name(f'fin@{self.currentFunc.name}')
        expr_list.append(ASTR.IfGoTo(cond_result, label_then))
        
        else_list = self.visit(node.else_expr, scope)
        else_list[-1].set_value(result_if)
        expr_list += else_list + [ASTR.GoTo(label_fin), ASTR.Label(label_then)]
        
        then_list = self.visit(node.then_expr) 
        then_list[-1].set_value(result_if, scope)
        
        expr_list += then_list + [ASTR.Label(label_fin)]

        return expr_list + [ASTR.Assign(super_value, result_if)]
    
    @visitor.when(AST.While)
    def visit(self, node: AST.While, scope: Scope):
        while_cond = new_name('while@cond', self.label_list)
        while_back = new_name('while@back', self.label_list)

        result_list = [ASTR.GoTo(while_cond), ASTR.Label(while_back)]
        result_list += self.visit(node.loop_expr, scope)
        result_list += [ASTR.Label(while_cond)]

        cond_local = self.currentFunc.local_push('cond@while', scope)
        result_list += self.visit(node.condition, scope)
        result_list[-1].set_value(cond_local)
        result_list.append(ASTR.IfGoTo(cond_local, while_back))

        return result_list + [ASTR.Assign(super_value, 'self')] 

    @visitor.when(AST.Block)
    def visit(self, node: AST.Block, scope: Scope):
        result_list = []
        _len = len(node.expr_list) - 1
        for i, expr in enumerate(node.expr_list):
            if i == _len: result_step = super_value
            else: result_step = self.currentFunc.local_push('step@block', scope)
            result_list += self.visit(expr, scope)
            result_list[-1].set_value(result_step)
        
        return  result_list

    @visitor.when(AST.LetIn)
    def visit(self, node: AST.LetIn, scope: Scope):
        result_list = []
        let_scope = scope.create_child('let')
        for name, _, expr in node.assing_list:
            local_name = self.currentFunc.local_push(name, let_scope)
            if not expr is None:
                result_list += self.visit(expr, let_scope)
                result_list[-1].set_value(local_name)
            
        return result_list + self.visit(node.expr, let_scope)

    @visitor.when(AST.Case)
    def visit(self, node: AST.Case, scope: Scope):
        expr_cond_list = self.visit(node.expr)
        case_cond_name = self.currentFunc.local_push('case@expr')
        expr_cond_list[-1].set_value(case_cond_name)
        case_cond_type = self.currentFunc.local_push('case@type')
        expr_cond_list.append(ASTR.TypeOf(case_cond_type, case_cond_name))

        case_result = self.currentFunc.local_push('case@result')
        case_fin_label = new_name('case@fin', self.label_list)
        expr_list = []
        for name, atype , expr in node.case_list:
            # get type for iter
            # compare type 
            # self.program.try_add_data(f'type@{atype.name}', atype.name)
            case_label = new_name('case@step@label', self.label_list)
            local_cmp = self.currentFunc.local_push('case@cmp')
            expr_cond_list.append(ASTR.IfGoTo(local_cmp, case_label))

            expr_list += [ASTR.Label(case_label)]
            expr_list += self.visit(expr)
            expr_list[-1].set_value(case_result)
            expr_list += [ASTR.GoTo(case_fin_label)]

        return (expr_cond_list 
                + expr_list 
                + [ASTR.Label(case_fin_label), ASTR.Assign(super_value, case_result)])

    def binary_op(self, name, node, astr_node, scope: Scope):
        op_1 = self.currentFunc.local_push(f'{name}@_a', scope)
        op_2 = self.currentFunc.local_push(f'{name}@_b', scope)

        result_list = self.visit(node.left, scope)
        result_list[-1].set_value(op_1)
        result_list += self.visit(node.right, scope)
        result_list[-1].set_value(op_2)

        return result_list + [astr_node(super_value, op_1, op_2)]

    @visitor.when(AST.Sum)
    def visit(self, node: AST.Sum, scope: Scope):
        return self.binary_op('sum', node, ASTR.Sum, scope)

    @visitor.when(AST.Rest)
    def visit(self, node: AST.Rest, scope: Scope):
         return self.binary_op('rest', node, ASTR.Rest, scope)

    @visitor.when(AST.Mult)
    def visit(self, node: AST.Mult, scope: Scope):
         return self.binary_op('factor', node, ASTR.Mult, scope)

    @visitor.when(AST.Div)
    def visit(self, node: AST.Div, scope: Scope):
        return self.binary_op('div', node, ASTR.Div, scope)

    @visitor.when(AST.Less)
    def visit(self, node: AST.Less, scope: Scope):
        return self.binary_op('less', node, ASTR.Less, scope)

    @visitor.when(AST.LessOrEquals)
    def visit(self, node: AST.LessOrEquals, scope: Scope):
        return self.binary_op('le', node, ASTR.LessOrEqual, scope)

    @visitor.when(AST.Equals)
    def visit(self, node: AST.Equals, scope: Scope):
        if node.static_type in [CoolInt, CoolBool]: 
            return self.binary_op('int_eq', node, ASTR.CmpInt, scope)
        if node.static_type == CoolStr: 
            return self.binary_op('str_eq', node, ASTR.CmpStr, scope)
        
        return self.binary_op('req_eq', node, ASTR.CmpRef, scope)
    
    @visitor.when(AST.New)
    def visit(self, node: AST.New, scope: Scope):
        return [ASTR.New(super_value, node.item.name)]   

    def unary_op(self, name, node, astr_node, scope: Scope):
        op = self.currentFunc.local_push(f'{name}@_unary', scope)
        result_list = self.visit(node.item, scope)
        result_list[-1].set_value(op)

        return result_list + [astr_node(super_value, op)]

    @visitor.when(AST.Complement)
    def visit(self, node: AST.Complement, scope: Scope):
        return self.unary_op('compl', node, ASTR.Complemnet, scope)

    @visitor.when(AST.Neg)
    def visit(self, node: AST.Neg, scope: Scope):
        return self.unary_op('neg', node, ASTR.Neg, scope)

    @visitor.when(AST.Void)
    def visit(self, node: AST.Void, scope: Scope):
        op_1 = self.currentFunc.local_push('void@_op', scope)
        null = self.currentFunc.local_push('void@_null', scope)
        unary_list = self.unary_op('void', node, ASTR.Complemnet, scope)
        unary_list[-1].set_value(op_1)

        return (
            [ASTR.Load(null, "NULL")] 
            + unary_list
            + [ASTR.CmpRef(super_value, null, op_1)]
        )
    
    @visitor.when(AST.Id)
    def visit(self, node: AST.Id, scope: Scope):
        var = scope.find_variable(node.item)
        if not var is None:
            return [ASTR.Assign(super_value, var.type)]
        else:
            return [ASTR.GetAttr(super_value, 'self', self.currentType.attr[node.item])]

    @visitor.when(AST.Int)
    @visitor.result(ASTR.Int)
    def visit(self, node: AST.Int, scope: Scope) -> ASTR.Node:
        return [ASTR.Assign(super_value, node.item)]

    @visitor.when(AST.Bool)
    @visitor.result(ASTR.Bool)
    def visit(self, node: AST.Bool, scope: Scope) -> ASTR.Node:
        if node.item == 'True': value = 1
        else: value = 0
        return [ASTR.Assign(super_value, value)]

    @visitor.when(AST.Str)
    def visit(self, node: AST.Str, scope: Scope):
        name = self.program.add_data('string', node.item)
        return [ASTR.Load(super_value, name)]