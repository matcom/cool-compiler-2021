from semantic.tools.scope import Scope
from semantic.tools.var import VariableInfo
from semantic.visitor import visitor
from nodes import ast_nodes as CoolAST
from nodes import cil_ast_nodes as CilAST
from nodes import expr_nodes as CoolExpr
from nodes import cil_expr_nodes as CilExpr
from nodes import operations_nodes as CoolOp

class CoolToCilVisitor:
    def __init__(self, context):
        self.context = context
        self.types = {}
        self.data = {}
        self.code = []
        self.current_type = None
        self.current_function = None
        self.context.set_type_tags()
        self.context.set_type_max_tags()
        self.label_num = 0

    def next_label(self):
        self.label_num += 1
        new_label = f'label_{self.label_num}'
        return new_label
    
    def register_type(self, type_name):
        type_node = CilAST.TypeNode(type_name)
        self.types[type_name] = type_node
        return type_node
    
    def register_data(self, msg):
        variable_name = f'msg_{len(self.data)}'
        self.data[variable_name] = msg
        return variable_name

    def register_function(self, function_name):
        function_node = CilAST.FunctionNode(function_name,[],[],[])
        self.code.append(function_node)
        return function_node

    def register_local_variable(self, variable_name):
        local_variable_node = CilExpr.LocalVariableDeclarationNode(variable_name)
        self.current_function.local_vars.append(local_variable_node)
        return variable_name
    
    def define_local_variable_in_scope(self, scope, type_name = None, cool_variable_name = None, variable_name = "l" ):
        cil_variable_name = f'{variable_name}_{len(self.current_function.local_vars)}'
        if type_name != None:
            cil_variable_name = f'{type_name}.{variable_name}'
        scope.define_cil_local(cool_variable_name,cil_variable_name, None)
        self.register_local_variable(cil_variable_name)
        return cil_variable_name
    
    def register_param(self, param_name):
        param_node = CilExpr.ParamDeclarationNode(param_name.name)
        self.current_function.params.append(param_node)
        return param_name.name
    
    def register_instruction(self, instruction):
        self.current_function.instructions.append(instruction)
        return instruction
    
    # ---------------------------------- Visitor ----------------------------------------------- #
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(CoolAST.ProgramNode)
    def visit(self, node, scope = None):
        scope = Scope()

        #Adding main function
        self.current_function = self.register_function('main')
        instance = self.define_local_variable_in_scope(scope = scope, variable_name="instance")
        result = self.define_local_variable_in_scope(scope = scope, variable_name="result")
        tag = self.context.get_type('Main').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Main',tag))
        self.register_instruction(CilExpr.CallNode(result,'Main','Main_init',[CilExpr.ArgNode(instance)]))
        self.register_instruction(CilExpr.CallNode(result,'Main','Main.main',[CilExpr.ArgNode(instance)]))
        self.register_instruction(CilExpr.ReturnNode(None))
        self.current_function = None

        #Auxiliar strings
        self.register_data('Abort called from class ')
        self.register_data('\n')
        self.data['empty_str'] = ''

        #Adding built-in types in .TYPES section
        for t in ['Object', 'Int', 'String', 'Bool', 'IO']:
            builtin_type = self.context.get_type(t)
            cil_type = self.register_type(t)
            cil_type.attributes = [f'{attr.name}' for attr in builtin_type.attributes]
            cil_type.methods = {f'{method}':f'{name}.{method}' for name, method in builtin_type.get_all_methods()}
            if t in ['Int','String','Bool']:
                cil_type.attributes.append('value')

        #-------------------------------------Object---------------------------------------#
        #init
        self.current_function = self.register_function('Object_init')
        self.register_param(VariableInfo('self',None))
        self.register_instruction(CilExpr.ReturnNode(None))

        #abort
        self.current_function = self.register_function('Object.abort')
        self.register_param(VariableInfo('self',None))
        msg = self.define_local_variable_in_scope(scope=scope,variable_name='msg')
        key_msg = ''
        key_eol = ''
        for key in self.data.keys():
            if self.data[key] == 'Abort called from class ':
                key_msg = key
            elif self.data[key] == '\n':
                key_eol = key
        self.register_instruction(CilExpr.LoadStrNode(msg,key_msg))
        self.register_instruction(CilExpr.PrintStringNode(msg))
        class_name = self.define_local_variable_in_scope(scope=scope,variable_name="class_name")
        self.register_instruction(CilExpr.TypeOfNode(class_name,'self'))
        self.register_instruction(CilExpr.PrintStringNode(class_name))
        end_of_line = self.define_local_variable_in_scope(scope=scope,variable_name="eol")
        self.register_instruction(CilExpr.LoadStrNode(end_of_line,key_eol))
        self.register_instruction(CilExpr.PrintStringNode(end_of_line))
        self.register_instruction(CilExpr.AbortNode())

        #type_name
        self.current_function = self.register_function('Object.type_name')
        self.register_param(VariableInfo('self',None))
        class_name = self.define_local_variable_in_scope(scope=scope,variable_name="class_name")
        self.register_instruction(CilExpr.TypeOfNode(class_name,'self'))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('String').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'String',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(class_name)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'String','String_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #copy
        self.current_function = self.register_function('Object.copy')
        self.register_param(VariableInfo('self',None))
        object_copy = self.define_local_variable_in_scope(scope=scope, variable_name='object_copy')
        self.register_instruction(CilExpr.CopyNode(object_copy,'self'))
        self.register_instruction(CilExpr.ReturnNode(object_copy))

        #-------------------------------------IO---------------------------------------#
        #init
        self.current_function = self.register_function('IO_init')
        self.register_param(VariableInfo('self',None))
        self.register_instruction(CilExpr.ReturnNode(None))

        #out_string
        self.current_function = self.register_function('IO.out_string')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('x', None))
        v = self.define_local_variable_in_scope(scope=scope, variable_name="v")
        self.register_instruction(CilExpr.GetAttrNode(v,'String','value','x'))
        self.register_instruction(CilExpr.PrintStringNode(v))
        self.register_instruction(CilExpr.ReturnNode('self'))

        #out_int
        self.current_function = self.register_function('IO.out_int')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('x', None))
        v = self.define_local_variable_in_scope(scope=scope, variable_name="v")
        self.register_instruction(CilExpr.GetAttrNode(v,'Int','value','x'))
        self.register_instruction(CilExpr.PrintIntegerNode(v))
        self.register_instruction(CilExpr.ReturnNode('self'))

        #in_string
        self.current_function = self.register_function('IO.in_string')
        self.register_param(VariableInfo('self',None))
        msg = self.define_local_variable_in_scope(scope=scope,variable_name="read_string")
        self.register_instruction(CilExpr.ReadStringNode(msg))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('String').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'String',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(msg)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'String','String_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #in_int
        self.current_function = self.register_function('IO.in_int')
        self.register_param(VariableInfo('self',None))
        num = self.define_local_variable_in_scope(scope=scope,variable_name="read_int")
        self.register_instruction(CilExpr.ReadIntegerNode(num))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Int',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(num)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'Int','Int_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #-------------------------------------Int---------------------------------------#
        #init
        self.current_function = self.register_function('Int_init')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('v',None))
        self.register_instruction(CilExpr.SetAttrNode('Int','value','v', 'self'))
        self.register_instruction(CilExpr.ReturnNode(None))

        #-------------------------------------String---------------------------------------#
        #init
        self.current_function = self.register_function('String_init')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('v',None))
        self.register_instruction(CilExpr.SetAttrNode('String','value','v', 'self'))
        self.register_instruction(CilExpr.ReturnNode(None))

        #length
        self.current_function = self.register_function('String.length')
        self.register_param(VariableInfo('self',None))
        str_length = self.define_local_variable_in_scope(scope=scope, variable_name="length")
        self.register_instruction(CilExpr.LengthNode(str_length,'self'))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Int',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(str_length)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'Int','Int_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #concat
        self.current_function = self.register_function('String.concat')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('s',None))
        str1 = self.define_local_variable_in_scope(scope=scope, variable_name="str1")
        self.register_instruction(CilExpr.GetAttrNode(str1,'String','value','self'))
        len1 = self.define_local_variable_in_scope(scope=scope, variable_name="len1")
        self.register_instruction(CilExpr.CallNode(len1,'String','String.length',[CilExpr.ArgNode('self')]))
        str2 = self.define_local_variable_in_scope(scope=scope, variable_name="str2")
        self.register_instruction(CilExpr.GetAttrNode(str2,'String','value','s'))
        len2 = self.define_local_variable_in_scope(scope=scope, variable_name="len2")
        self.register_instruction(CilExpr.CallNode(len2,'String','String.length',[CilExpr.ArgNode('s')]))
        ## Get real value from memory address returned by Length
        len1_value = self.define_local_variable_in_scope(scope=scope,variable_name="len1_value")
        self.register_instruction(CilExpr.GetAttrNode(len1_value,'Int','value',len1))
        len2_value = self.define_local_variable_in_scope(scope=scope,variable_name="len2_value")
        self.register_instruction(CilExpr.GetAttrNode(len2_value,'Int','value',len2))
        ## New string, result from concat
        result_string = self.define_local_variable_in_scope(scope=scope, variable_name="result_string")
        self.register_instruction(CilExpr.ConcatNode(result_string,str1,str2,len1_value,len2_value))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('String').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'String',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(result_string)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'String','String_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #substr
        self.current_function = self.register_function('String.substr')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('index',None))
        self.register_param(VariableInfo('len',None))
        i_value = self.define_local_variable_in_scope(scope=scope,variable_name="i_value")
        self.register_instruction(CilExpr.GetAttrNode(i_value,'Int','value','index'))
        l_value = self.define_local_variable_in_scope(scope=scope,variable_name="l_value")
        self.register_instruction(CilExpr.GetAttrNode(l_value,'Int','value','len'))
        ## New string, result from substr
        result_substr = self.define_local_variable_in_scope(scope=scope,variable_name="substr_result")
        self.register_instruction(CilExpr.SubStrNode(result_substr,i_value,'self',l_value))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('String').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'String',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(result_substr)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'String','String_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))

        #-------------------------------------Bool---------------------------------------#
        #init
        self.current_function = self.register_function('Bool_init')
        self.register_param(VariableInfo('self',None))
        self.register_param(VariableInfo('v',None))
        self.register_instruction(CilExpr.SetAttrNode('Bool','value','v', 'self'))
        self.register_instruction(CilExpr.ReturnNode(None))

        #-----------String Equals------------------#
        self.current_function = self.register_function('String_equals')
        self.register_param(VariableInfo('str1',None))
        self.register_param(VariableInfo('str2',None))
        str1_value = self.define_local_variable_in_scope(scope=scope,variable_name="str1")
        self.register_instruction(CilExpr.GetAttrNode(str1_value,'String','value','str1'))
        str2_value = self.define_local_variable_in_scope(scope=scope,variable_name="str2")
        self.register_instruction(CilExpr.GetAttrNode(str2_value,'String','value','str2'))
        equals_result = self.define_local_variable_in_scope(scope=scope,variable_name="result")
        self.register_instruction(CilExpr.StringEqualsNode(equals_result,str1_value,str2_value))
        self.register_instruction(CilExpr.ReturnNode(equals_result))

        #Visit class nodes
        for _class in node.classes:
            self.visit(_class, scope.create_child())

        program_node = CilAST.ProgramNode(self.types,self.data,self.code)
        return program_node

    @visitor.when(CoolAST.ClassNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.name)
        cil_type = self.register_type(self.current_type.name)
        cil_type.attributes = [f'{attr.name}' for _, attr in self.current_type.get_all_attributes()]
        cil_type.methods = {f'{method}':f'{name}.{method}' for name, method in self.current_type.get_all_methods()}
        scope.define_cil_local('self',self.current_type.name,self.current_type)

        function_declarations = []
        attribute_declarations = []

        for feature in node.features:
            if isinstance(feature, CoolAST.ClassMethodNode):
                function_declarations.append(feature)
            else:
                attribute_declarations.append(feature)
                scope.define_cil_local(feature.name, feature.name, node.name)
        
        #init
        self.current_function = self.register_function(f'{node.name}_init')
        self.register_param(VariableInfo('self',None))
        #init parents
        result = self.define_local_variable_in_scope(scope=scope,variable_name="result")
        self.register_instruction(CilExpr.CallNode(result, node.parent, f'{node.parent}_init',[CilExpr.ArgNode('self')]))
        self.register_instruction(CilExpr.ReturnNode(None))

        for attribute in attribute_declarations:
            self.visit(attribute,scope)

        self.current_function = None

        for function in function_declarations:
            self.visit(function,scope.create_child())

        self.current_type = None

    @visitor.when(CoolAST.AttrInitNode)
    def visit(self, node, scope):
        expression_value = self.visit(node.expression, scope)
        instruction = CilExpr.SetAttrNode(self.current_type.name,node.name,expression_value,'self')
        self.register_instruction(instruction)
    
    @visitor.when(CoolAST.AttrDefNode)
    def visit(self, node, scope):
        instance = None
        if node.attr_type in ['Int', 'Bool', 'String']:
            instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
            tag = self.context.get_type(node.attr_type).tag
            self.register_instruction(CilExpr.AllocateNode(instance,node.attr_type,tag))
            value = self.define_local_variable_in_scope(scope=scope, variable_name='value')
            if node.attr_type == 'String':
                self.register_instruction(CilExpr.LoadStrNode(value,'empty_str'))
            else:
                self.register_instruction(CilExpr.LoadIntNode(value,0))
            result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
            arg1 = CilExpr.ArgNode(value)
            arg2 = CilExpr.ArgNode(instance)
            self.register_instruction(CilExpr.CallNode(result,node.attr_type,f'{node.attr_type}_init',[arg1,arg2]))
        instruction = CilExpr.SetAttrNode(self.current_type.name,node.name,instance,'self')
        self.register_instruction(instruction)
    
    @visitor.when(CoolAST.ClassMethodNode)
    def visit(self, node, scope):
        cil_method_name = f'{self.current_type.name}.{node.name}'
        self.types[self.current_type.name].methods[node.name] = cil_method_name
        self.current_function = self.register_function(cil_method_name)
        self.register_param(VariableInfo('self',self.current_type))
        for param in node.params:
            self.register_param(VariableInfo(param.name,param.param_type))
        value = self.visit(node.expression, scope)
        self.register_instruction(CilExpr.ReturnNode(value))

    @visitor.when(CoolExpr.DynamicCallNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope,variable_name="result")

        expression_value = self.visit(node.obj, scope)

        args = []
        for arg in reversed(node.args): 
            param = self.visit(arg, scope)
            args.append(CilExpr.ArgNode(param))
        args.append(CilExpr.ArgNode(expression_value))

        dynamic_type = node.obj.expr_type.name
        self.register_instruction(CilExpr.VCallNode(result,dynamic_type,node.method,args,expression_value))
        return result

    @visitor.when(CoolExpr.StaticCallNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope,variable_name="result")

        expression_value = self.visit(node.obj, scope)

        args = []
        for arg in reversed(node.args): 
            param = self.visit(arg, scope)
            args.append(CilExpr.ArgNode(param))
        args.append(CilExpr.ArgNode(expression_value))

        instance = self.define_local_variable_in_scope(scope=scope,variable_name="instance")
        tag = self.context.get_type(node.static_type).tag
        self.register_instruction(CilExpr.AllocateNode(instance,node.static_type,tag))
        self.register_instruction(CilExpr.VCallNode(result,node.static_type,node.method,args,instance))
        return result

    @visitor.when(CoolExpr.AssignNode)
    def visit(self, node, scope):
        expression_value = self.visit(node.expression, scope)
        self.define_local_variable_in_scope(scope=scope, variable_name="result")
        is_param = False
        for param in self.current_function.params:
            if param.name == node.name:
               is_param = True
               break
        if is_param:
            self.register_instruction(CilExpr.AssignNode(node.name,expression_value))
        elif self.current_type.has_attr(node.name):
            self.register_instruction(CilExpr.SetAttrNode(self.current_type.name,node.name,expression_value,'self'))
        else:
            cil_node_name = scope.find_cil_local(node.name)
            self.register_instruction(CilExpr.AssignNode(cil_node_name, expression_value))

        return expression_value

    @visitor.when(CoolExpr.CaseNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        case_expression = self.visit(node.expression,scope)

        label = self.next_label()
        label_for_exit = self.next_label()

        self.register_instruction(CilExpr.CaseNode(case_expression,label))

        #Getting tags of each action
        tags_list = []
        act_dict = {}
        for action in node.act_list:
            tag = self.context.get_type(action.act_type).tag
            tags_list.append(tag)
            act_dict[tag] = action
        
        #Sort the tags_list
        tags_list.sort()
        #For each tag in descending order visit the corresponding action and create the nodes
        for tag in reversed(tags_list):
            action = act_dict[tag]
            self.register_instruction(CilExpr.LabelNode(label))
            label = self.next_label()
            act_type = self.context.get_type(action.act_type)
            self.register_instruction(CilExpr.ActionNode(case_expression,act_type.tag,act_type.max_tag,label))
            act_scope = scope.create_child()
            act_id = self.define_local_variable_in_scope(scope=act_scope,variable_name=action.name, cool_variable_name=action.name)
            self.register_instruction(CilExpr.AssignNode(act_id,case_expression)) 
            act_expression = self.visit(action.body,act_scope)
            self.register_instruction(CilExpr.AssignNode(result,act_expression))
            self.register_instruction(CilExpr.GotoNode(label_for_exit))

        self.register_instruction(CilExpr.LabelNode(label))
        #If not found any match case, goto error
        self.register_instruction(CilExpr.GotoNode('case_no_match_error'))
        self.register_instruction(CilExpr.LabelNode(label_for_exit))
        return result

    @visitor.when(CoolExpr.ActionNode)
    def visit(self, node, scope):
        pass

    @visitor.when(CoolExpr.IfNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        predicate_value = self.visit(node.predicate,scope)
        then_label = self.next_label()
        self.register_instruction(CilExpr.IfGotoNode(predicate_value,then_label))
        else_value = self.visit(node.else_expr,scope)
        self.register_instruction(CilExpr.AssignNode(result,else_value))
        end_if_label = self.next_label()
        self.register_instruction(CilExpr.GotoNode(end_if_label))
        self.register_instruction(CilExpr.LabelNode(then_label))
        then_value = self.visit(node.then_expr,scope)
        self.register_instruction(CilExpr.AssignNode(result,then_value))
        self.register_instruction(CilExpr.LabelNode(end_if_label))
        return result

    @visitor.when(CoolExpr.WhileNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        conditional_label = self.next_label()
        body_label = self.next_label()
        end_label = self.next_label()
        self.register_instruction(CilExpr.LabelNode(conditional_label))
        predicate_value = self.visit(node.predicate,scope)
        self.register_instruction(CilExpr.IfGotoNode(predicate_value,body_label))
        self.register_instruction(CilExpr.GotoNode(end_label))
        self.register_instruction(CilExpr.LabelNode(body_label))
        self.visit(node.expression, scope)
        self.register_instruction(CilExpr.GotoNode(conditional_label))
        self.register_instruction(CilExpr.LabelNode(end_label))
        self.register_instruction(CilExpr.LoadVoidNode(result))
        return result

    @visitor.when(CoolExpr.BlockNode)
    def visit(self, node, scope):
        for expr in node.expr_list:
            result = self.visit(expr, scope)
        return result

    @visitor.when(CoolExpr.LetNode)
    def visit(self, node, scope):
        let_scope = scope.create_child()
    
        for var in node.init_list:
            self.visit(var, let_scope)

        body_result = self.visit(node.body, let_scope)
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        self.register_instruction(CilExpr.AssignNode(result,body_result))
        return result

    @visitor.when(CoolAST.LetInitNode)
    def visit(self, node, scope):
        expression_value = self.visit(node.expression, scope)
        variable = self.define_local_variable_in_scope(scope=scope,variable_name=node.name,cool_variable_name=node.name)
        self.register_instruction(CilExpr.AssignNode(variable,expression_value))
        return variable

    @visitor.when(CoolAST.LetDefNode)
    def visit(self, node, scope):
        instance = None
        if node.let_type in ['Int', 'Bool', 'String']:
            instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
            tag = self.context.get_type(node.let_type).tag
            self.register_instruction(CilExpr.AllocateNode(instance,node.let_type,tag))
            value = self.define_local_variable_in_scope(scope=scope, variable_name='value')
            if node.let_type == 'String':
                self.register_instruction(CilExpr.LoadStrNode(value,'empty_str'))
            else:
                self.register_instruction(CilExpr.LoadIntNode(value,0))
            result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
            arg1 = CilExpr.ArgNode(value)
            arg2 = CilExpr.ArgNode(instance)
            self.register_instruction(CilExpr.CallNode(result,node.let_type,f'{node.let_type}_init',[arg1,arg2]))
        variable = self.define_local_variable_in_scope(scope=scope,variable_name=node.name,cool_variable_name=node.name)
        self.register_instruction(CilExpr.AssignNode(variable,instance))
        return variable

    @visitor.when(CoolExpr.NewNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope,variable_name="result")
        init = self.define_local_variable_in_scope(scope=scope,variable_name="init")

        if node.new_type == 'SELF_TYPE':
            tag = self.current_type.tag
            name = self.current_type.name
            self.register_instruction(CilExpr.AllocateNode(result,name,tag))
            self.register_instruction(CilExpr.CallNode(init,name,f'{name}_init',[result])) 
        else :
            tag = self.context.get_type(node.new_type).tag
            self.register_instruction(CilExpr.AllocateNode(result,node.new_type,tag))
            self.register_instruction(CilExpr.CallNode(init,self.current_type.name,f'{node.new_type}_init',[CilExpr.ArgNode(result)])) 

        return result

    @visitor.when(CoolExpr.IsVoidNode)
    def visit(self, node, scope):
        expression_value = self.visit(node.expression, scope)
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        self.register_instruction(CilExpr.IsVoidNode(result,expression_value))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Bool',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name='init')
        arg1 = CilExpr.ArgNode(result)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,'Bool','Bool_init',[arg1,arg2]))
        self.register_instruction(CilExpr.ReturnNode(instance))
        return instance

    @visitor.when(CoolOp.SumNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"+",right))

        #Allocate Int result
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Int',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Int','Int_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.SubNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"-",right))

        #Allocate Int result
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Int',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Int','Int_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.MultNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"*",right))

        #Allocate Int result
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Int',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Int','Int_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.DivNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"/",right))

        #Allocate Int result
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Int',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Int','Int_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.LessEqualNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"<=",right))

        #Allocate Bool result
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Bool',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Bool','Bool_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.LessNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
        self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))
        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"<",right))

        #Allocate Bool result
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Bool',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Bool','Bool_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.LogicNotNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        expression = self.define_local_variable_in_scope(scope=scope)

        expression_value = self.visit(node.expression, scope)

        self.register_instruction(CilExpr.GetAttrNode(expression,node.expression.expr_type.name,"value",expression_value))
        self.register_instruction(CilExpr.UnaryOperatorNode(op,"~",expression))

        #Allocate Int result
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Int',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Int','Int_init',[arg1,arg2]))

        return result

    @visitor.when(CoolOp.NotNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        expression = self.define_local_variable_in_scope(scope=scope)

        expression_value = self.visit(node.expression, scope)

        self.register_instruction(CilExpr.GetAttrNode(expression,node.expression.expr_type.name,"value",expression_value))
        self.register_instruction(CilExpr.UnaryOperatorNode(op,"not",expression))

        #Allocate Bool result
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Bool',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Bool','Bool_init',[arg1,arg2]))

        return result

    @visitor.when(CoolExpr.EqualsNode)
    def visit(self, node, scope):
        result = self.define_local_variable_in_scope(scope=scope, variable_name="result")
        op = self.define_local_variable_in_scope(scope=scope, variable_name="op")
        left = self.define_local_variable_in_scope(scope=scope, variable_name="left")
        right = self.define_local_variable_in_scope(scope=scope, variable_name="right")

        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)

        if node.left.expr_type.name == "String":
            arg1 = CilExpr.ArgNode(right_value)
            arg2 = CilExpr.ArgNode(left_value)
            self.register_instruction(CilExpr.CallNode(op,'String','String_equals',[arg1,arg2]))

            #Allocate Bool result
            tag = self.context.get_type('Bool').tag
            self.register_instruction(CilExpr.AllocateNode(result,'Bool',tag))
            init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
            arg1 = CilExpr.ArgNode(op)
            arg2 = CilExpr.ArgNode(result)
            self.register_instruction(CilExpr.CallNode(init,'Bool','Bool_init',[arg1,arg2]))

            return result

        elif node.left.expr_type.name in ['Int', 'Bool']:
            self.register_instruction(CilExpr.GetAttrNode(left,node.left.expr_type.name,"value",left_value))
            self.register_instruction(CilExpr.GetAttrNode(right,node.right.expr_type.name,"value",right_value))

        else:
            self.register_instruction(CilExpr.AssignNode(left,left_value))
            self.register_instruction(CilExpr.AssignNode(right,right_value))

        self.register_instruction(CilExpr.BinaryOperatorNode(op,left,"=",right))

        #Allocate Bool result
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(result,'Bool',tag))
        init = self.define_local_variable_in_scope(scope=scope, variable_name="init")
        arg1 = CilExpr.ArgNode(op)
        arg2 = CilExpr.ArgNode(result)
        self.register_instruction(CilExpr.CallNode(init,'Bool','Bool_init',[arg1,arg2]))

        return result

    @visitor.when(CoolExpr.IdNode)
    def visit(self, node, scope):
        is_param = False
        for param in self.current_function.params:
            if param.name == node.name:
               is_param = True
               break
        if is_param:
            return node.name
        elif self.current_type.has_attr(node.name):
            result = self.define_local_variable_in_scope(scope=scope, variable_name=node.name, type_name=self.current_type.name)
            self.register_instruction(CilExpr.GetAttrNode(result,self.current_type.name,node.name,'self'))
            return result
        else:
            return scope.find_cil_local(node.name)

    @visitor.when(CoolExpr.IntegerNode)
    def visit(self, node, scope):
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('Int').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Int',tag))
        value = self.define_local_variable_in_scope(scope=scope, variable_name='value')
        self.register_instruction(CilExpr.LoadIntNode(value,node.value))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(value)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,"Int",'Int_init',[arg1,arg2]))
        return instance

    @visitor.when(CoolExpr.BooleanNode)
    def visit(self, node, scope):
        boolean = 0
        if str(node.value) == "true":
            boolean = 1
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('Bool').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'Bool',tag))
        value = self.define_local_variable_in_scope(scope=scope, variable_name='value')
        self.register_instruction(CilExpr.LoadIntNode(value,boolean))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(value)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,"Bool",'Bool_init',[arg1,arg2]))
        return instance

    @visitor.when(CoolExpr.StringNode)
    def visit(self, node, scope):
        str_name = ""
        for s in self.data.keys():
            if self.data[s] == node.value:
                str_name = s
                break
        if str_name == "":
            str_name = self.register_data(node.value)
            
        value = self.define_local_variable_in_scope(scope=scope)
        self.register_instruction(CilExpr.LoadStrNode(value,str_name))
        instance = self.define_local_variable_in_scope(scope=scope, variable_name="instance")
        tag = self.context.get_type('String').tag
        self.register_instruction(CilExpr.AllocateNode(instance,'String',tag))
        result = self.define_local_variable_in_scope(scope=scope, variable_name='result')
        arg1 = CilExpr.ArgNode(value)
        arg2 = CilExpr.ArgNode(instance)
        self.register_instruction(CilExpr.CallNode(result,"String",'String_init',[arg1,arg2]))
        return instance





    

    








