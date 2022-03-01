from cool_compiler.cmp.scope import Scope
from cool_compiler.types.cool_type_build_in_manager import OBJECT_NAME, CoolTypeBuildInManager
from ...cmp import visitor
from ...semantic.v2_semantic_checking import semantic_checking_ast as AST
from . import cool_to_cil_ast as ASTR
from .cool_to_cil_ast import super_value
from .tools import BaseCoolToCIL

CoolInt = CoolTypeBuildInManager().find("Int")
CoolBool = CoolTypeBuildInManager().find("Bool")
CoolStr = CoolTypeBuildInManager().find("String")
CoolObject = CoolTypeBuildInManager().find(OBJECT_NAME)

class CoolToCIL(BaseCoolToCIL):
    def __init__(self, error) -> None:
        self.label_list = {}
        self.type_dir = {
            OBJECT_NAME: 1
        }

    @visitor.on('node')
    def visit(node, scope: Scope):
        pass

    @visitor.when(AST.Program)
    def visit(self, node: AST.Program, scope: Scope = None):
        self.program = ASTR.Program()
        self.program.try_add_data('_______error______', 'Abort called from class ')
        self.program.try_add_data('_______null_______', 'null')
        self.program.try_add_data('_______endline_______', '\n')

        scope = Scope()

        _dictt = CoolTypeBuildInManager().dictt
        for _type in _dictt.values():
            self.create_type(_type, scope)
            self.new_type_func.expr_push(ASTR.Return('self'))
            self.program.add_func(self.new_type_func)

        for cls in node.class_list:
            _ = [self.map_type(parent.name) for parent in self.parent_list(cls.type)]   

        for cls in node.class_list:
            self.visit(cls, scope)



        main = ASTR.Function('main')
        main.force_local('self', scope)
        # main.force_local(result, scope)
        main.expr_push(ASTR.ALLOCATE('self', 'Main'))
        main.expr_push(ASTR.Comment(f'Assignacion de la insformacion de tipo a Main'))
        main.expr_push(ASTR.Load('_', 'Main'))
        main.expr_push(ASTR.SetAttr('self', 'type_name', '_'))
        main.expr_push(ASTR.Arg('self'))
        main.expr_push(ASTR.SimpleCall('new_ctr_Main'))
        main.expr_push(ASTR.Arg('self'))
        main.expr_push(ASTR.SimpleCall('Main_main'))
        # main.expr_push(ASTR.VCall(result, 'Main', 'main'))
        main.expr_push(ASTR.Return(0))
        self.program.add_func(main)

        return self.program

    @visitor.when(AST.CoolClass)
    def visit(self, node: AST.CoolClass, scope: Scope):
        self.class_scope = scope.create_child(node.type.name)
        
        self.create_type(node.type, scope)
        for feat in node.feature_list:
            self.visit(feat, self.class_scope)


        self.new_type_func.expr_push(ASTR.Return('self'))
        self.program.add_func(self.new_type_func)
    
    def create_type(self, _type, scope):
        self.currentType = ASTR.Type(_type.name)
        self.currentClass = _type
        
        self.program.add_type(self.currentType)

        type_list = []
        for parent in self.parent_list(_type):
            type_list.append(self.map_type(parent.name))
            self.currentType.attr_push('type_name', self.currentType.name)
            for attr in parent.attributes:
                self.currentType.attr_push(attr.name, f'{parent.name}@{attr.name}')
            for func in parent.methods:
                self.currentType.method_push(func.name, f'{parent.name}_{func.name}')
        
        self.program.force_data(f'{_type.name}_parents', type_list + [0])
        self.program.force_data(f'{_type.name}_Name', _type.name)
        self.program.force_data(_type.name, 
            [f'{_type.name}_Name', len(self.currentType.attr), f'{_type.name}_parents'] + 
            [self.currentType.methods[key] for key in self.currentType.methods.keys()])
        
        self.create_new_func_by_type(_type, scope)
    
    def create_new_func_by_type(self, _type, scope):
        self.new_class_scope = scope.create_child(f'new_{_type.name}')
        self.new_type_func = ASTR.Function(f'new_ctr_{_type.name}')
        self.new_type_func.force_parma('self', self.new_class_scope)
        # tn = self.new_type_func.local_push('type_name', self.new_class_scope)

        if not _type.parent is None:
            self.new_type_func.expr_push(ASTR.Arg('self'))
            self.new_type_func.expr_push(ASTR.SimpleCall(f'new_ctr_{_type.parent.name}'))

        # self.new_type_func.expr_push(ASTR.Comment(f'Assignacion de la insformacion de tipo a la instancia'))
        # self.new_type_func.expr_push(ASTR.Load('_', _type.name))
        # self.new_type_func.expr_push(ASTR.SetAttr('self', 'type_name', '_'))
        # self.new_type_func.expr_push(ASTR.Comment(f'FIN de la assignacion de la insformacion de tipo a la instancia'))

    @visitor.when(AST.AtrDef)
    def visit(self, node: AST.AtrDef, scope: Scope):
        try: 
            save_current_func = self.currentFunc
        except AttributeError:
            save_current_func = None
        self.currentFunc = self.new_type_func

        if not node.expr in [None, []]:

            # attr_name = self.new_type_func.local_push(f'value_to_set_{node.name}', self.new_class_scope)
            exp_list = [ASTR.Comment(f'Assignando el resultado de la expression al atributo {node.name} de la clase {self.currentType.name}')]
            exp_list += self.visit(node.expr, self.new_class_scope)
            exp_list[-1].set_value("_")
            exp_list.append(ASTR.SetAttr('self', self.currentType.attr[node.name], '_'))
            exp_list.append(ASTR.Comment(f"Fin De la Asignacion"))     
            self.new_type_func.expr += exp_list
        
        elif node.type in [CoolInt, CoolBool]:
            self.new_type_func.expr_push(ASTR.Assign('_', 0))
            self.new_type_func.expr_push(ASTR.VCall('_', f'__{node.type.name.lower()}__new__', '_'))
            self.new_type_func.expr_push(ASTR.SetAttr('self', self.currentType.attr[node.name], '_'))
        else: 
            self.new_type_func.expr_push(ASTR.Load('_', '_______null_______'))
            self.new_type_func.expr_push(ASTR.SetAttr('self', self.currentType.attr[node.name], '_'))
        
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
        if not any(expr_list): 
            self.visit(node.expr, func_scope)
        # self.currentFunc.force_local(result, func_scope)
        cond = expr_list[-1].try_set_value('_')

        expr_list.append(ASTR.Return('_' if cond else 'self'))

        self.currentFunc.expr = expr_list
    
    @visitor.when(AST.CastingDispatch)
    def visit(self, node: AST.CastingDispatch, scope: Scope):
        instance_expr_list = [ASTR.Comment(f"Evalua la Expresion para el CastingDispatch {node.id}")]
        instance_expr_list += self.visit(node.expr, scope)
        instance_name = self.currentFunc.local_push(f'instance_{node.type.name}_to_{node.id}', scope)
        instance_expr_list[-1].set_value(instance_name)
        instance_expr_list.append(ASTR.Comment(f"Fin de la exprecion previa al CastingDispatch {node.id}"))

        arg_list = [instance_name]
        for i, param in enumerate(node.params):
            instance_expr_list += [ASTR.Comment(f"Evalua el parametro {i} para el CastingDispatch {node.id}")]
            instance_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            instance_expr_list[-1].set_value(param_name)
            instance_expr_list.append(ASTR.Comment(f"Fin del paramentro {i} al CastingDispatch {node.id}"))
            arg_list.append(param_name)

        if len(arg_list) == 1:
            _list, new_name = self.try_funsion(instance_expr_list[0:-1], instance_name)
            _list.append(instance_expr_list[-1])
            instance_expr_list = _list 
            arg_list[0] = new_name
        
        for i, arg in enumerate(arg_list):
            instance_expr_list.append(ASTR.Arg(arg))

        instance_expr_list.append(ASTR.VCall(super_value, node.type.name, node.id))
        return instance_expr_list
    
    @visitor.when(AST.Dispatch)
    def visit(self, node: AST.Dispatch, scope: Scope):
        instance_expr_list = [ASTR.Comment(f"Evalua la Expresion para el DinamicDispatch {node.id}")]
        instance_expr_list += self.visit(node.expr, scope)
        instance_name = self.currentFunc.local_push(f'instance_dynamic_to_{node.id}', scope)
        instance_expr_list[-1].set_value(instance_name)
        instance_expr_list.append(ASTR.Comment(f"Fin de la exprecion previa al DinamicDispatch {node.id}"))

        arg_list = [instance_name]
        for i, param in enumerate(node.params):
            instance_expr_list += [ASTR.Comment(f"Evalua el parametro {i} para el CastingDispatch {node.id}")]
            instance_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            instance_expr_list[-1].set_value(param_name)
            instance_expr_list.append(ASTR.Comment(f"Fin del paramentro {i} al CastingDispatch {node.id}"))
            arg_list.append(param_name)
        
        if len(arg_list) == 1:
            _list, new_name = self.try_funsion(instance_expr_list[0:-1], instance_name)
            _list.append(instance_expr_list[-1])
            instance_expr_list = _list 
            arg_list[0] = new_name
            instance_name = new_name

        for i, arg in enumerate(arg_list):
            instance_expr_list.append(ASTR.Arg(arg))

        instance_expr_list.append(ASTR.Call(super_value, instance_name, f'{node.expr.static_type.name}@{node.id}'))
        return instance_expr_list

    @visitor.when(AST.StaticDispatch)
    def visit(self, node: AST.StaticDispatch, scope: Scope):
        instance_expr_list = [ASTR.Comment(f"StaticDispatch {node.id}")]

        arg_list = ['self']
        for i, param in enumerate(node.params):
            instance_expr_list += [ASTR.Comment(f"Evalua el parametro {i} para el CastingDispatch {node.id}")]
            instance_expr_list += self.visit(param, scope)
            param_name = self.currentFunc.local_push(f'param_{i}_to_{node.id}', scope)
            instance_expr_list[-1].set_value(param_name)
            instance_expr_list.append(ASTR.Comment(f"Fin del paramentro {i} al CastingDispatch {node.id}"))
            arg_list.append(param_name)
        
        for i, arg in enumerate(arg_list):
            instance_expr_list.append(ASTR.Arg(arg))

        instance_expr_list.append(ASTR.Call(super_value, 'self', f'{self.currentClass.name}@{node.id}'))
        # instance_expr_list.append(ASTR.VCall(super_value, self.currentClass.name, node.id))
        return instance_expr_list

    @visitor.when(AST.Assing)
    def visit(self, node: AST.Assing, scope: Scope):
        exp_list = [ASTR.Comment(f'Asignando un nuevo valor a la variable {node.id}')]
        exp_list += self.visit(node.expr, scope)
        exp_list[-1].set_value('_')

        
        var = scope.find_variable(node.id)
        if not var is None: 
            exp_list.append(ASTR.Assign(var.type, '_'))
            exp_list.append(ASTR.Assign(super_value, var.type))
        else:
            exp_list.append(ASTR.SetAttr('self', self.currentType.attr[node.id], '_'))
            exp_list.append(ASTR.GetAttr(super_value , 'self', self.currentType.attr[node.id]))

        return exp_list
    
    @visitor.when(AST.IfThenElse)
    def visit(self, node: AST.IfThenElse, scope: Scope):
        # cond_result = self.currentFunc.local_push(f'cond@if_else', scope)
        expr_list = [ASTR.Comment(f'Evalua la condicion de un If')]
        expr_list += self.visit(node.condition, scope)
        expr_list[-1].set_value('_')
        expr_list.append(ASTR.Comment(f'Fin de la evaluacion de la condicion de un IF'))

        label_then = self.new_name(f'then_{self.currentFunc.name}', self.label_list)
        label_fin = self.new_name(f'fin_{self.currentFunc.name}', self.label_list)
        expr_list.append(ASTR.IfGoTo('_', label_then))
        
        expr_list.append(ASTR.Comment(f'Else case'))
        else_list = self.visit(node.else_expr, scope)
        else_list[-1].set_value('_')
        expr_list += else_list + [ASTR.GoTo(label_fin), ASTR.Label(label_then)]
        
        expr_list.append(ASTR.Comment(f'Then case'))
        then_list = self.visit(node.then_expr, scope) 
        then_list[-1].set_value('_')
        
        expr_list += then_list + [ASTR.Label(label_fin)]
        expr_list.append(ASTR.Comment(f'Fin de un If'))

        return expr_list + [ASTR.Assign(super_value, '_')]

    @visitor.when(AST.While)
    def visit(self, node: AST.While, scope: Scope):
        while_cond = self.new_name('while_cond', self.label_list)
        while_back = self.new_name('while_back', self.label_list)

        # result_local = self.currentFunc.local_push('result@while', scope)

        result_list = [ASTR.Comment(f'Inicio de un While'), ASTR.GoTo(while_cond), ASTR.Label(while_back)]
        result_list += self.visit(node.loop_expr, scope)
        result_list[-1].set_value('_')
        result_list.append(ASTR.Comment(f'Fin del cuerpo e inicio de la condicion de un While'))
        result_list.append(ASTR.Label(while_cond))

        # cond_local = self.currentFunc.local_push('cond@while', scope)
        result_list += self.visit(node.condition, scope)
        result_list[-1].set_value("_")
        # result_list.append(self.get_value('_', 'Bool'))
        result_list.append(ASTR.IfGoTo('_', while_back))
        result_list.append(ASTR.Comment(f'Fin de la condicion de un While'))


        # while return object
        return result_list + [ASTR.Assign(super_value, 'self')] 

    @visitor.when(AST.Block)
    def visit(self, node: AST.Block, scope: Scope):
        result_list = []
        result_list.append(ASTR.Comment(f'Inicio de una secuencia Block'))
        _len = len(node.expr_list) - 1
        for i, expr in enumerate(node.expr_list):
            if i == _len: result_step = super_value
            else: result_step = '_'
            result_list.append(ASTR.Comment(f'Inicio del paso {i} de una sequencia Block'))
            result_list += self.visit(expr, scope)
            result_list[-1].set_value(result_step)

        # result_list.append(ASTR.Comment(f'Fin de una sequencia Block'))
        return  result_list

    @visitor.when(AST.LetIn)
    def visit(self, node: AST.LetIn, scope: Scope):
        result_list = []
        let_scope = scope.create_child('let')
        for name, _, expr in node.assing_list:
            local_name = self.currentFunc.force_local(name, let_scope)
            if not expr is None:
                result_list.append(ASTR.Comment(f'Eval Expression to Let {name}'))
                result_list += self.visit(expr, let_scope)
                result_list[-1].set_value(local_name)
                result_list.append(ASTR.Comment(f'Fin de la asignacion Let {name}'))

        
        return result_list + self.visit(node.expr, let_scope) 

    @visitor.when(AST.Case)
    def visit(self, node: AST.Case, scope: Scope):
        expr_cond_list = [ASTR.Comment("Eval Expression To Case")]
        expr_value =  self.currentFunc.local_push('cond@expr@value', scope)
        type_result = self.currentFunc.local_push('cond@type', scope)
        expr_cond_list += self.visit(node.expr, scope)
        expr_cond_list[-1].set_value(expr_value)
        expr_cond_list.append(ASTR.TypeOf(type_result, expr_value))
        expr_cond_list.append(ASTR.Comment("Final Expression To Case"))        


        expr_list = []
        end_label = self.new_name('case_end', self.label_list)
        
        sorted_case = sorted(node.case_list, key=lambda a: self.map_type(a[1].name), reverse=True)
        for name, atype , expr in sorted_case:
            expr_cond_list.append(ASTR.Comment(f"Check Type To Case When Option Is {atype.name}"))
            step_label = self.new_name(f'{atype.name}_step_case', self.label_list)
            expr_cond_list.append(ASTR.Assign('_', self.map_type(atype.name)))
            expr_cond_list.append(ASTR.CheckType('_', type_result, '_'))
            expr_cond_list.append(ASTR.IfGoTo('_', step_label))

            
            expr_list.append(ASTR.Label(step_label))
            step_scope = scope.create_child('step_case')
            self.currentFunc.force_local(name, step_scope)
            expr_list.append(ASTR.Comment(f"Assigan el valor de la expresion a la var {name} del case"))
            expr_list.append(ASTR.Assign(name, expr_value))
            expr_list.append(ASTR.Comment(f"Eval Expression Of {atype.name} Option"))
            expr_list += self.visit(expr, step_scope) 
            expr_list[-1].set_value('_')
            expr_list.append(ASTR.GoTo(end_label))

        return (
            expr_cond_list 
            + expr_list
            + [ASTR.Label(end_label)]
            + [ASTR.Assign(super_value, '_')] 
        )

    def binary_op(self, name, node, astr_node, scope: Scope):
        op_1 = self.currentFunc.local_push(f'{name}@_a', scope)
        op_2 = self.currentFunc.local_push(f'{name}@_b', scope)

        result_list = [ASTR.Comment(f'Evaluando el operado izquierdo de una operacion {name}')]
        result_list += self.visit(node.left, scope)
        result_list[-1].set_value(op_1)
        result_list.append(ASTR.Comment(f'Resolucion del operado izquierdo de una operacion {name}'))

        result_list += [ASTR.Comment(f'Evaluando el operado derecho de una operacion {name}')]
        result_list += self.visit(node.right, scope)
        result_list[-1].set_value(op_2)
        result_list.append(ASTR.Comment(f'Resolucion del operado derecha de una operacion {name}'))

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
        return self.binary_op('leq', node, ASTR.LessOrEqual, scope)
  
    @visitor.when(AST.Equals)
    def visit(self, node: AST.Equals, scope: Scope):
        name = 'ref_eq'
        if node.left.static_type in [CoolInt, CoolBool]: name = 'int_eq' 
        if node.left.static_type == CoolStr: name = 'str_eq'

        return self.binary_op(name, node, ASTR.Equals, scope)
    
    @visitor.when(AST.New)
    def visit(self, node: AST.New, scope: Scope):
        new = self.currentFunc.local_push(f'new_{node.item.name}', scope)
        return [
            ASTR.Comment(f'Creando instancia de tipo {node.item.name}'),
            ASTR.ALLOCATE(new, node.item.name),
            ASTR.Comment(f'Assignacion de la insformacion de tipo a la instancia'),
            ASTR.Load('_', node.item.name),
            ASTR.SetAttr(new, 'type_name', '_'),
            ASTR.Arg(new),
            ASTR.New(super_value, node.item.name)
        ]  

    def unary_op(self, node, astr_node, scope: Scope):
        result_list = [ASTR.Comment(f'Evaluando la expression de una operacion unaria')]
        result_list += self.visit(node.item, scope)        
        result_list[-1].set_value('_')
        result_list += [ASTR.Comment(f'FIN expression de una operacion unaria')]

        return result_list + [astr_node(super_value, '_')]

    @visitor.when(AST.Complement)
    def visit(self, node: AST.Complement, scope: Scope):
        return self.unary_op(node, ASTR.Complemnet, scope)

    @visitor.when(AST.Neg)
    def visit(self, node: AST.Neg, scope: Scope):
        return self.unary_op(node, ASTR.Neg, scope)
    
    @visitor.when(AST.Void)
    def visit(self, node: AST.Void, scope: Scope):
        op_1 = self.currentFunc.local_push('ref_eq@_a', scope)
        null = self.currentFunc.local_push('ref_eq@_b', scope)
        unary_list = self.visit(node.item, scope)
        unary_list[-1].set_value(op_1)
        
        return (
            [ASTR.Load(null, "_______null_______"), ASTR.Comment("void check")] 
            + unary_list
            + [ASTR.Equals(super_value, null, op_1)]
        )
 
    @visitor.when(AST.Id)
    def visit(self, node: AST.Id, scope: Scope):
        var = scope.find_variable(node.item)
        if not var is None:
            return [ASTR.Comment(f"Get Local Var {node.item}"),ASTR.Assign(super_value, var.type)]     
        else:
            return [ASTR.Comment(f"Get Self Property {node.item}"),ASTR.GetAttr(super_value, 'self', self.currentType.attr[node.item])]    
    
    @visitor.when(AST.Int)
    def visit(self, node: AST.Int, scope: Scope):
        return [ASTR.Assign('_', node.item), ASTR.VCall(super_value, '__int__new__', '_')]

    @visitor.when(AST.Bool)
    def visit(self, node: AST.Bool, scope: Scope):
        if node.item == 'true': value = 1
        else: value = 0
        return [ASTR.Assign('_', value), ASTR.VCall('_', '__int__new__', '_'), ASTR.VCall(super_value, '__bool__new__', '_')]

    @visitor.when(AST.Str)
    def visit(self, node: AST.Str, scope: Scope):
        name = self.program.add_data('string', node.item)

        return [
            ASTR.Load('_', name),
            ASTR.VCall(super_value, '__str__new__', '_')
        ]