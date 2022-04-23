import re
import CIL.ast as cil
from Parser.ast import *
from Tools.utils import *
import Tools.visitor as visitor
from Tools.context import VoidType, StringType, IntType, BoolType, ObjectType

class CIL:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.idx = 0
        self.constructors = []
        self.void_data = None
        self.inherit_graph = {}

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope):
        self.current_function = self.add_function('entry')
        idx = self.index
        instance = self.define_internal_local()
        result = self.define_internal_local()

        self.add_instruction(cil.AllocateNode('Main', instance)) 
        typex = self.context.get_type('Main', (0,0))
        if typex.all_attributes():
            self.add_instruction(cil.StaticCallNode(typex.name, typex.name, None, [cil.ArgNode(instance)], typex.name))
        
        name = self.to_function_name('main', 'Main')
        self.add_instruction(cil.StaticCallNode('Main', 'main', result, [cil.ArgNode(instance)], 'Object'))
        self.add_instruction(cil.ReturnNode(0))
        self.current_function = None

        self.void_data = self.add_data('Void').name

        self.create_built_in()
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode, idx)
    

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope):
        self.current_type = self.context.get_type(node.id, node.pos)
        
        cil_type = self.add_type(node.id)
 
        attrs = self.current_type.all_attributes()
        if len(attrs) > 0:
            constructor = FuncDeclarationNode(node.token, [], node.token, BlockNode([], node.token))
            func_declarations = [constructor]
            self.constructors.append(node.id)
            self.current_type.define_method(self.current_type.name, [], [], self.current_type, node.pos)
            scopes = [scope] + list(scope.functions.values())
        else:
            func_declarations = []
            scopes = list(scope.functions.values())
            
        for attr, a_type in attrs:
            cil_type.attributes.append((attr.name, self.to_attr_name(attr.name, a_type.name)))
            self.initialize_attr(constructor, attr, scope)
        if attrs:
            constructor.body.expr_list.append(SelfNode())


        for method, mtype in self.current_type.all_methods():
            cil_type.methods.append((method.name, self.to_function_name(method.name, mtype.name)))


        func_declarations += [f for f in node.features if isinstance(f, FuncDeclarationNode)] 
        for feature, child_scope in zip(func_declarations, scopes):
            self.visit(feature, child_scope)


    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope):
        self.current_method = self.current_type.get_method(node.id, node.pos)
        name = self.to_function_name(node.id, self.current_type.name)
        self.current_function = self.add_function(name)
     
        self.register_param('self', self.current_type.name)
        for p_name, p_type in node.params:
            self.register_param(p_name, p_type.value)
        
        value, typex = self.visit(node.body, scope)
        if not isinstance(value, str):
            result = self.define_internal_local()
            self.add_instruction(cil.AssignNode(result, value))
        else:
            result = value

        if (typex.name == 'Int' or typex.name == 'String' or typex.name == 'Bool') and self.current_method.return_type.name == 'Object':
            self.add_instruction(cil.BoxingNode(result, typex.name))

        self.add_instruction(cil.ReturnNode(result)) 
        self.current_method = None

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope):
        var_info = scope.find_variable(node.id)
        vtype = get_type(var_info.type, self.current_type)
        local_var = self.register_local(var_info.name)

        value, typex = self.visit(node.expr, scope)
        if vtype.name == 'Object' and typex.name in ['String', 'Int', 'Bool']:
            self.add_instruction(cil.BoxingNode(local_var, typex.name))
        else:
            self.add_instruction(cil.AssignNode(local_var, value))
        return local_var, vtype


    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            attributes = [attr.name for attr, a_type in self.current_type.all_attributes()]
            if var_info.type.name == 'Object' and typex.name in ['String', 'Bool', 'Int']:
                value = self.define_internal_local()
                self.add_instruction(cil.BoxingNode(value, typex.name))
            self.add_instruction(cil.SetAttribNode('self', var_info.name, self.current_type.name, value))
        else:
            local_name = self.to_var_name(var_info.name)
            if var_info.type.name == 'Object' and typex.name in ['String', 'Bool', 'Int']:
                self.add_instruction(cil.BoxingNode(local_name, typex.name))
            else:
                self.add_instruction(cil.AssignNode(local_name, value))
        return value, typex

    def _return_type(self, typex: Type, node):
        meth = typex.get_method(node.id, node.pos)
        return get_type(meth.return_type, self.current_type)

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope):
        obj, otype = self.visit(node.obj, scope)
        
        meth = otype.get_method(node.id, node.pos)
        args_node = [cil.ArgNode(obj, self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        result = None if isinstance(rtype, VoidType) else self.define_internal_local()
       
        continue_label = cil.LabelNode(f'continue__{self.index}') 
        isvoid = self.check_void(obj)
        self.add_instruction(cil.GotoIfFalseNode(isvoid, continue_label.label))
        self.add_instruction(cil.ErrorNode('dispatch_error'))
        self.add_instruction(continue_label)

        if otype in [StringType(), IntType(), BoolType()]:
            self.add_instruction(cil.StaticCallNode(otype.name, node.id, result, args_node, rtype.name))
        else:
            self.add_instruction(cil.DynamicCallNode(otype.name, obj, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope):
        obj, otype = self.visit(node.obj, scope)

        meth = otype.get_method(node.id, node.pos)
        args_node = [cil.ArgNode(obj, self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        result = None if isinstance(rtype, VoidType) else self.define_internal_local()
        
        continue_label = cil.LabelNode(f'continue__{self.index}') 
        isvoid = self.check_void(obj)
        self.add_instruction(cil.GotoIfFalseNode(isvoid, continue_label.label))
        self.add_instruction(cil.ErrorNode('dispatch_error'))
        self.add_instruction(continue_label)
        
        self.add_instruction(cil.StaticCallNode(node.type, node.id, result, args_node, rtype.name))
        return result, self._return_type(otype, node)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode, scope):
        meth = self.current_type.get_method(node.id, node.pos)
        args_node = [cil.ArgNode('self', self.index)] + self.handle_arguments(node.args, scope, meth.param_types)

        rtype = meth.return_type
        if isinstance(rtype, VoidType):
            result = None
        else: 
            result = self.define_internal_local()

        self.add_instruction(cil.DynamicCallNode(self.current_type.name, 'self', node.id, result, args_node, rtype.name))
        return result, self._return_type(self.current_type, node)

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope):
        return int(node.lex), IntType()

    @visitor.when(ConstantBoolNode)
    def visit(self, node: ConstantBoolNode, scope):
        return 1 if node.lex  == 'true' else 0, BoolType()
   
    @visitor.when(ConstantStrNode)
    def visit(self, node: ConstantStrNode, scope):
        data = self.add_data(node.lex)
        result = self.define_internal_local()
        self.add_instruction(cil.LoadNode(result, data.name))
        return result, StringType()

    @visitor.when(ConstantVoidNode)
    def visit(self, node: ConstantVoidNode, scope):
        result = self.register_local(node.lex)
        void = cil.VoidConstantNode(result)
        self.add_instruction(void)
        return result, VoidType() 

    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope):
        return 'self', self.current_type

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope):
        try:
            typex = scope.find_local(node.lex).type
            name = self.to_var_name(node.lex)
            return name, get_type(typex, self.current_type)
        except:
            var_info = scope.find_attribute(node.lex)
            local_var = self.register_local(var_info.name)
            self.add_instruction(cil.GetAttribNode('self', var_info.name, self.current_type.name, local_var, var_info.type.name))
            return local_var, get_type(var_info.type, self.current_type)

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope):
        instance = self.define_internal_local()
        typex = self.context.get_type(node.lex, node.pos)
        typex = get_type(typex, self.current_type)
        self.add_instruction(cil.AllocateNode(typex.name, instance))
        
        if typex.all_attributes():
            self.add_instruction(cil.StaticCallNode(typex.name, typex.name, instance, [cil.ArgNode(instance)], typex.name))
        
        return instance, typex

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope):
        start_label = cil.LabelNode(f'start__{self.idx}')
        end_label = cil.LabelNode(f'end__{self.idx}')
        
        result = self.define_internal_local()
        self.add_instruction(cil.VoidConstantNode(result))
        self.add_instruction(start_label)

        cond, _ = self.visit(node.cond, scope)
        self.add_instruction(cil.GotoIfFalseNode(cond, end_label.label))
        expr, typex = self.visit(node.expr, scope)
        self.add_instruction(cil.AssignNode(result, expr))
        self.add_instruction(cil.GotoNode(start_label.label))
        self.add_instruction(end_label)
        
        return result, ObjectType()

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope):
        cond, _ = self.visit(node.cond, scope)

        true_label = cil.LabelNode(f"true__{self.idx}")
        end_label = cil.LabelNode(f"end__{self.idx}")

        result = self.define_internal_local()
        self.add_instruction(cil.GotoIfNode(cond, true_label.label))

        false_expr, ftypex = self.visit(node.else_stm, scope)
        self.add_instruction(cil.AssignNode(result, false_expr))
        self.add_instruction(cil.GotoNode(end_label.label))
        self.add_instruction(true_label)
        
        true_expr, ttypex = self.visit(node.stm, scope)
        self.add_instruction(cil.AssignNode(result, true_expr))
        self.add_instruction(end_label)
        return result, get_common_basetype([ttypex, ftypex])

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope):
        value = None
        for exp in node.expr_list:
            value, typex = self.visit(exp, scope)
        result = self.define_internal_local()
        self.add_instruction(cil.AssignNode(result, value))
        return result, typex

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        
        expr, typex = self.visit(node.expr, child_scope)
        return expr, typex

    @visitor.when(CaseNode) 
    def visit(self, node: CaseNode, scope):
        expr, typex = self.visit(node.expr, scope)
        
        result = self.define_internal_local()
        end_label = cil.LabelNode(f'end__{self.idx}')
        error_label = cil.LabelNode(f'error__{self.idx}')
     
        isvoid = self.check_void(expr)
        self.add_instruction(cil.GotoIfNode(isvoid, error_label.label))

        try:
            new_scope = scope.expr_dict[node]
        except:
            new_scope = scope
        sorted_case_list = self.sort_nodes(node.case_list)
        for i, case in enumerate(sorted_case_list):
            next_label = cil.LabelNode(f'next__{self.idx}_{i}')
            expr_i = self.visit(case, new_scope.create_child(), expr, next_label, typex)
            self.add_instruction(cil.AssignNode(result, expr_i))
            self.add_instruction(cil.GotoNode(end_label.label))
            self.add_instruction(next_label)
        self.add_instruction(cil.ErrorNode('case_error'))
        self.add_instruction(error_label)
        self.add_instruction(cil.ErrorNode('case_void_error'))
        self.add_instruction(end_label)
        return result, typex

    @visitor.when(OptionNode)
    def visit(self, node: OptionNode, scope, expr, next_label, type_e):
        aux = self.define_internal_local()
        self.add_instruction(cil.ConformsNode(aux, expr, node.typex))
        self.add_instruction(cil.GotoIfFalseNode(aux, next_label.label))
        
        local_var = self.register_local(node.id)
        typex = self.context.get_type(node.typex, node.type_pos)
        scope.define_variable(node.id, typex)
        if typex.name == 'Object' and type_e.name in ['String', 'Int', 'Bool']:
            self.add_instruction(cil.BoxingNode(local_var, type_e.name))
        else:
            self.add_instruction(cil.AssignNode(local_var, expr))
        expr_i, type_expr = self.visit(node.expr, scope)
        return expr_i

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope):
        return self._define_unary_node(node, scope, cil.LogicalNotNode)

    @visitor.when(BinaryNotNode)
    def visit(self, node: BinaryNotNode, scope):
        return self._define_unary_node(node, scope, cil.NotNode)

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope):
        expr, _ = self.visit(node.expr, scope)
        result = self.check_void(expr)
        return result, BoolType()

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope):
        return self.add_binary_node(node, scope, cil.PlusNode)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope):
        return self.add_binary_node(node, scope, cil.MinusNode)

    @visitor.when(StarNode)
    def visit(self, node: StarNode, scope):
        return self.add_binary_node(node, scope, cil.StarNode)

    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope):
        return self.add_binary_node(node, scope, cil.DivNode)

    @visitor.when(LessNode)
    def visit(self, node: LessNode, scope):
        return self.add_binary_node(node, scope, cil.LessNode)
        
    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode, scope):
        return self.add_binary_node(node, scope, cil.LessEqNode)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope):
        return self.add_binary_node(node, scope, cil.EqualNode)

    @property
    def index(self):
        i = self.idx
        self.idx += 1
        return i
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property 
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, vname, vtype):
        name = f'param_{self.current_function.name[9:]}_{vname}_{len(self.params)}'
        param_node = cil.ParamNode(vname, vtype, self.index)
        self.params.append(param_node)
        return vname
    
    def register_local(self, vname):
        name = f'local_{self.current_function.name[9:]}_{vname}_{len(self.localvars)}' 
        local_node = cil.LocalNode(name, self.index)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self):
        return self.register_local('internal')

    def add_instruction(self, instruction):
        self.instructions.append(instruction)
        instruction.index = self.index
        return instruction
    
    def to_attr_name(self, attr_name, type_name):
        return f'attribute_{attr_name}_{type_name}'

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_{type_name}'
    
    def to_var_name(self, var_name):
        regex = re.compile(f'local_{self.current_function.name[9:]}_(.+)_\d+')
        for node in reversed(self.localvars):
            m = regex.match(node.name).groups()[0]
            if  m == var_name:
                return node.name
        for node in self.params:
            if node.name == var_name:
                return var_name
        return None
        
    def add_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [], self.index)
        self.dotcode.append(function_node)
        return function_node

    def add_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def add_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value, self.index)
        self.dotdata.append(data_node)  
        return data_node

    def add_binary_node(self, node: BinaryNode, scope, cil_node: cil.Node):
        result = self.define_internal_local()
        left, typex = self.visit(node.left, scope)
        right, typex = self.visit(node.right, scope)
        self.add_instruction(cil_node(result, left, right))
        return result, typex

    def _define_unary_node(self, node: UnaryNode, scope, cil_node):
        result = self.define_internal_local()
        expr, typex = self.visit(node.expr, scope)
        self.add_instruction(cil_node(result, expr))
        return result, typex

    def initialize_attr(self, constructor, attr, scope):
        if attr.expr:
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))
        else:
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantVoidNode(attr.name)))

    def create_built_in(self):

        f1_params = [cil.ParamNode("self", 'Object')]
        f1_localVars = [cil.LocalNode("local_abort_Object_self_0")]
        f1_intructions = [cil.AssignNode(f1_localVars[0].name,f1_params[0].name, self.index),
                          cil.ExitNode(f1_params[0].name, idx=self.index)]
        f1 = cil.FunctionNode("function_abort_Object",f1_params,f1_localVars,f1_intructions)

        f2_params = [cil.ParamNode("self", 'Object')]
        f2_localVars = [cil.LocalNode("local_type_name_Object_result_0")]
        f2_intructions = [cil.TypeOfNode(f2_params[0].name,f2_localVars[0].name, self.index),
                          cil.ReturnNode(f2_localVars[0].name, self.index)]
        f2 = cil.FunctionNode("function_type_name_Object",f2_params,f2_localVars,f2_intructions)

        f3_params = [cil.ParamNode("self", 'Object')]
        f3_localVars = [cil.LocalNode("local_copy_Object_result_0")]
        f3_intructions = [cil.CopyNode(f3_localVars[0].name,f3_params[0].name, self.index),
                          cil.ReturnNode(f3_localVars[0].name, self.index)]
        f3 = cil.FunctionNode("function_copy_Object",f3_params,f3_localVars,f3_intructions)

        f4_params = [cil.ParamNode("self", 'IO'), cil.ParamNode("word", 'String')]
        f4_localVars = [cil.LocalNode("local_out_string_String_self_0")]
        f4_intructions = [cil.AssignNode(f4_localVars[0].name, f4_params[0].name, self.index),
                          cil.OutStringNode(f4_params[1].name, self.index),
                          cil.ReturnNode(f4_localVars[0].name, self.index)]
        f4 = cil.FunctionNode("function_out_string_IO",f4_params,f4_localVars,f4_intructions)

        f5_params = [cil.ParamNode("self", 'IO'),cil.ParamNode("number", 'Int')]
        f5_localVars = [cil.LocalNode("local_out_int_IO_self_0")]
        f5_intructions = [cil.AssignNode(f5_localVars[0].name,f5_params[0].name, self.index),
                          cil.OutIntNode(f5_params[1].name, self.index),
                          cil.ReturnNode(f5_localVars[0].name, self.index)]
        f5 = cil.FunctionNode("function_out_int_IO",f5_params,f5_localVars,f5_intructions)

        f6_params = [cil.ParamNode("self", 'IO')]
        f6_localVars = [cil.LocalNode("local_in_int_IO_result_0")]
        f6_intructions = [cil.ReadIntNode(f6_localVars[0].name, self.index),
                          cil.ReturnNode(f6_localVars[0].name, self.index)]
        f6 = cil.FunctionNode("function_in_int_IO",f6_params,f6_localVars,f6_intructions)

        f7_params = [cil.ParamNode("self", 'IO')]
        f7_localVars = [cil.LocalNode("local_in_string_IO_result_0")]
        f7_intructions = [cil.ReadStringNode(f7_localVars[0].name, self.index),
                          cil.ReturnNode(f7_localVars[0].name, self.index)]
        f7 = cil.FunctionNode("function_in_string_IO",f7_params,f7_localVars,f7_intructions)

        f8_params = [cil.ParamNode("self", 'String')]
        f8_localVars = [cil.LocalNode("local_length_String_result_0")]
        f8_intructions = [cil.LengthNode(f8_localVars[0].name,f8_params[0].name, self.index),
                         cil.ReturnNode(f8_localVars[0].name, self.index)]
        f8 = cil.FunctionNode("function_length_String",f8_params,f8_localVars,f8_intructions)

        f9_params = [cil.ParamNode("self", 'String'),cil.ParamNode("word", 'String')]
        f9_localVars = [cil.LocalNode("local_concat_String_result_0")]
        f9_intructions = [cil.ConcatNode(f9_localVars[0].name,f9_params[0].name,f9_params[1].name, self.index),
                          cil.ReturnNode(f9_localVars[0].name, self.index)]
        f9 = cil.FunctionNode("function_concat_String",f9_params,f9_localVars,f9_intructions)

        f10_params = [cil.ParamNode("self", 'String'),cil.ParamNode("begin", 'Int'),cil.ParamNode("end", 'Int')]
        f10_localVars = [cil.LocalNode("local_substr_String_result_0")]
        f10_intructions = [cil.SubstringNode(f10_localVars[0].name,f10_params[0].name,f10_params[1].name,f10_params[2].name, self.index), 
                           cil.ReturnNode(f10_localVars[0].name, self.index)]
        f10 = cil.FunctionNode("function_substr_String",f10_params,f10_localVars,f10_intructions)

        f11_params = [cil.ParamNode("self", 'String')]
        f11_localVars = [cil.LocalNode("local_type_name_String_result_0")]
        f11_intructions = [cil.LoadNode(f11_localVars[0].name, 'type_String', self.index),
                           cil.ReturnNode(f11_localVars[0].name, self.index)]
        f11 = cil.FunctionNode("function_type_name_String",f11_params,f11_localVars,f11_intructions)

        f12_params = [cil.ParamNode("self", 'String')]
        f12_localVars = [cil.LocalNode("local_copy_String_result_0")]
        f12_intructions = [cil.ConcatNode(f12_localVars[0].name, f12_params[0].name, None, self.index),
                           cil.ReturnNode(f12_localVars[0].name, self.index)]
        f12 = cil.FunctionNode("function_copy_String",f12_params,f12_localVars,f12_intructions)

        f17_params = [cil.ParamNode("self", 'String')]
        f17_localVars = [cil.LocalNode('local_abort_String_msg_0')]
        f17_intructions = [cil.LoadNode(f17_params[0].name, 'string_abort'), 
                           cil.OutStringNode(f17_params[0].name, self.index),
                           cil.ExitNode(f17_params[0].name, idx=self.index)]
        f17 = cil.FunctionNode("function_abort_String",f17_params,f17_localVars,f17_intructions)

        f13_params = [cil.ParamNode("self", 'Int')]
        f13_localVars = [cil.LocalNode("local_type_name_Int_result_0")]
        f13_intructions = [cil.LoadNode(f13_localVars[0].name, 'type_Int', self.index),
                           cil.ReturnNode(f13_localVars[0].name, self.index)]
        f13 = cil.FunctionNode("function_type_name_Int",f13_params,f13_localVars,f13_intructions)

        f14_params = [cil.ParamNode("self", 'Int')]
        f14_localVars = [cil.LocalNode("local_copy_Int_result_0")]
        f14_intructions = [cil.AssignNode(f14_localVars[0].name, f14_params[0].name), 
                           cil.ReturnNode(f14_localVars[0].name, self.index)]
        f14 = cil.FunctionNode("function_copy_Int",f14_params,f14_localVars,f14_intructions)

        f18_params = [cil.ParamNode("self", 'Int')]
        f18_localVars = [cil.LocalNode('local_abort_Int_msg_0')]
        f18_intructions = [cil.LoadNode(f18_params[0].name, 'int_abort'), 
                           cil.OutStringNode(f18_params[0].name, self.index),
                           cil.ExitNode(f18_params[0].name, idx=self.index)]
        f18 = cil.FunctionNode("function_abort_Int",f18_params,f18_localVars,f18_intructions)

        
        f15_params = [cil.ParamNode("self", 'Bool')]
        f15_localVars = [cil.LocalNode("local_type_name_Bool_result_0")]
        f15_intructions = [cil.LoadNode(f15_localVars[0].name, 'type_Bool', self.index),
                           cil.ReturnNode(f15_localVars[0].name, self.index)]
        f15 = cil.FunctionNode("function_type_name_Bool",f15_params,f15_localVars,f15_intructions)

        f16_params = [cil.ParamNode("self", 'Bool')]
        f16_localVars = [cil.LocalNode("local_copy_result_Bool_0")]
        f16_intructions = [cil.AssignNode(f16_localVars[0].name, f16_params[0].name), 
                           cil.ReturnNode(f16_localVars[0].name, self.index)]
        f16 = cil.FunctionNode("function_copy_Bool",f16_params,f16_localVars,f16_intructions)

        f19_params = [cil.ParamNode("self", 'Bool')]
        f19_localVars = [cil.LocalNode('local_abort_Bool_msg_0')]
        f19_intructions = [cil.LoadNode(f19_params[0].name, 'bool_abort'), 
                           cil.OutStringNode(f19_params[0].name, self.index),
                           cil.ExitNode(f19_params[0].name, idx=self.index)]
        f19 = cil.FunctionNode("function_abort_Bool",f19_params,f19_localVars,f19_intructions)


        self.dotcode += [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11, f12, f13, f14, f15, f16, f17, f18, f19]
        object_methods = [('abort', f1.name), ('type_name', f2.name), ('copy', f3.name)]
        string_methods = [('length', f8.name), ('concat', f9.name), ('substr', f10.name), ('abort', f17.name), ('type_name', f11.name), ('copy', f12.name)]
        io_methods = [('out_string', f4.name), ('out_int', f5.name), ('in_int', f6.name), ('in_string', f7.name)]
        int_methods = [('abort', f18.name), ('type_name', f13.name), ('copy', f14.name)]
        bool_methods = [('abort', f19.name), ('type_name', f15.name), ('copy', f16.name)]

        self.dottypes += [cil.TypeNode("Object", [], object_methods), 
                cil.TypeNode("IO", [], object_methods + io_methods) , 
                cil.TypeNode("String", [],  string_methods), 
                cil.TypeNode('Int', [], int_methods),
                cil.TypeNode('Bool', [], bool_methods)]

    def sort_nodes(self, case_list):
        return sorted(case_list, reverse=True,
                    key=lambda x: self.context.get_depth(x.typex))

    def check_void(self, expr):
        result = self.define_internal_local()
        self.add_instruction(cil.TypeOfNode(expr, result))
        
        void_expr = self.define_internal_local()
        self.add_instruction(cil.LoadNode(void_expr, self.void_data))
        self.add_instruction(cil.EqualNode(result, result, void_expr))
        return result
        
    def handle_arguments(self, args, scope, param_types):
        args_node = []
        args = [self.visit(arg, scope) for arg in args]
        
        for (arg, typex), param_type in zip(args, param_types):
            if typex.name in ['String', 'Int', 'Bool'] and param_type.name == 'Object':
                auxiliar = self.define_internal_local()
                self.add_instruction(cil.BoxingNode(auxiliar, typex.name))
            else:
                auxiliar = arg
            args_node.append(cil.ArgNode(auxiliar, self.index))
        return args_node