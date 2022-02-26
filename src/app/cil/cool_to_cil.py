import app.cil.ast_cil as cil
import app.utils.visitor as visitor
from app.semantics.tools.scope import VariableInfo
from app.semantics.tools.errors import AttributeError
import app.semantics.inference.inferencer_ast as cool


def get_token(node):
    for attr in ['tid', 'token', 'ttype', 'symbol']:
        if hasattr(node, attr):
            return getattr(node, attr)
    raise Exception(f'{node} has no token')


class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context
        self.vself = VariableInfo('self', None)
        self.value_types = ['String', 'Int', 'Bool']

    @property
    def params(self):
        return self.current_function.params

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def ids(self):
        return self.current_function.ids

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_param(self, vinfo):
        # # print(vinfo.name)
        # 'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        vinfo.name = vinfo.name
        param_node = cil.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name

    def register_local(self, vinfo, id=False):
        new_vinfo = VariableInfo('', None)
        if len(self.current_function.name) >= 8 and self.current_function.name[:8] == 'function':
            new_vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        else:
            new_vinfo.name = f'local_{self.current_function.name[5:]}_{vinfo.name}_{len(self.localvars)}'

        local_node = cil.LocalNode(new_vinfo.name)
        if id:
            # # print(f"toy registrando {vinfo.name}")
            self.ids[vinfo.name] = new_vinfo.name
            # # print("los ids actualizados", self.ids)
        self.localvars.append(local_node)
        return new_vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###############################

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def init_name(self, type_name, attr=False):
        if attr:
            return f'init_attr_at_{type_name}'
        return f'init_at_{type_name}'

    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return cil.LabelNode(lname)

    def register_built_in(self):
        # Object
        type_node = self.register_type('Object')

        self.current_function = self.register_function(
            self.init_name('Object'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Object', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('abort', 'Object'))
        self.register_param(self.vself)
        vname = self.define_internal_local()
        data_node = [dn for dn in self.dotdata if dn.value ==
                     'Abort called from class '][0]
        self.register_instruction(cil.LoadNode(vname, data_node))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.TypeNameNode(vname, self.vself.name))
        self.register_instruction(cil.PrintStrNode(vname))
        data_node = self.register_data('\n')
        self.register_instruction(cil.LoadNode(vname, data_node))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ExitNode())
        # No need for RETURN here right??

        self.current_function = self.register_function(
            self.to_function_name('type_name', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeNameNode(result, self.vself.name))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('copy', 'Object'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self.vself.name))
        self.register_instruction(cil.ReturnNode(result))

        type_node.methods = [(name, self.to_function_name(name, 'Object'))
                             for name in ['abort', 'type_name', 'copy']]
        type_node.methods += [('init', self.init_name('Object'))]
        obj_methods = ['abort', 'type_name', 'copy']

        # IO
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.init_name('IO'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('IO', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('out_string', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(
            cil.GetAttribNode(vname, 'x', 'value', 'String'))
        self.register_instruction(cil.PrintStrNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(
            self.to_function_name('out_int', 'IO'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(
            cil.GetAttribNode(vname, 'x', 'value', 'Int'))
        self.register_instruction(cil.PrintIntNode(vname))
        self.register_instruction(cil.ReturnNode(self.vself.name))

        self.current_function = self.register_function(
            self.to_function_name('in_string', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadStrNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('in_int', 'IO'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in obj_methods]
        type_node.methods += [(name, self.to_function_name(name, 'IO'))
                              for name in ['out_string', 'out_int', 'in_string', 'in_int']]
        type_node.methods += [('init', self.init_name('IO'))]

        # String
        type_node = self.register_type('String')
        type_node.attributes = ['value', 'length']

        self.current_function = self.register_function(
            self.init_name('String'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('String', instance))
        self.register_instruction(cil.SetAttribNode(
            instance, 'value', 'val', 'String'))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, 'val'))
        attr = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name('Int'), attr))
        self.register_instruction(cil.SetAttribNode(
            instance, 'length', attr, 'String'))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('length', 'String'))
        self.register_param(self.vself)
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(
            result, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(
            self.to_function_name('concat', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('s', None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        length_1 = self.define_internal_local()
        length_2 = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(
            str_1, self.vself.name, 'value', 'String'))
        self.register_instruction(
            cil.GetAttribNode(str_2, 's', 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(
            length_1, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(
            length_2, 's', 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(
            length_1, length_1, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(
            length_2, length_2, 'value', 'Int'))
        self.register_instruction(cil.PlusNode(length_1, length_1, length_2))

        result = self.define_internal_local()
        self.register_instruction(
            cil.ConcatNode(result, str_1, str_2, length_1))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(
            self.to_function_name('substr', 'String'))
        self.register_param(self.vself)
        self.register_param(VariableInfo('i', None))
        self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(
            str_value, self.vself.name, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(
            index_value, 'i', 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(
            length_value, 'l', 'value', 'Int'))
        # Check Out of range error
        self.register_instruction(cil.GetAttribNode(
            length_attr, self.vself.name, 'length', 'String'))
        self.register_instruction(cil.PlusNode(
            length_substr, length_value, index_value))
        self.register_instruction(cil.LessNode(
            less_value, length_attr, length_substr))
        self.register_runtime_error(less_value, 'Substring out of range')
        self.register_instruction(cil.SubstringNode(
            result, str_value, index_value, length_value))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in obj_methods]
        type_node.methods += [(name, self.to_function_name(name, 'String'))
                              for name in ['length', 'concat', 'substr']]
        type_node.methods += [('init', self.init_name('String'))]

        # Int
        type_node = self.register_type('Int')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Int'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Int', instance))
        self.register_instruction(cil.SetAttribNode(
            instance, 'value', 'val', 'Int'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in obj_methods]
        type_node.methods += [('init', self.init_name('Int'))]

        # Bool
        type_node = self.register_type('Bool')
        type_node.attributes = ['value']

        self.current_function = self.register_function(self.init_name('Bool'))
        self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Bool', instance))
        self.register_instruction(cil.SetAttribNode(
            instance, 'value', 'val', 'Bool'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = [(method, self.to_function_name(
            method, 'Object')) for method in obj_methods]
        type_node.methods += [('init', self.init_name('Bool'))]

    def register_runtime_error(self, condition, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.GotoIfNode(condition, error_node.label))
        self.register_instruction(cil.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(cil.ErrorNode(data_node))

        self.register_instruction(continue_node)


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    def __init__(self, context):
        super().__init__(context)

    def buildHierarchy(self, t: str):
        if t == 'Object':
            return None
        # print("Building hierarchy for", t)
        # print("el type en el context es:", self.context.get_type(
            # t), "y es de tipo", type(self.context.get_type(t)))
        # print([*map(lambda x: (x.name, type(x)), self.context.types.values())])
        return {x.name for x in self.context.types.values() if x.name != 'AUTO_TYPE' and x.conforms_to(self.context.get_type(t))}

    @ visitor.on('node')
    def visit(self, node):
        pass

    @ visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        scope = node.scope
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################

        self.current_function = self.register_function('entry')
        result = self.define_internal_local()
        instance = self.register_local(VariableInfo('instance', None))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Main'), instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(
            self.to_function_name('main', 'Main'), result))
        self.register_instruction(cil.ReturnNode(0))
        # Error message raised by Object:abort()
        self.register_data('Abort called from class ')
        self.register_built_in()
        self.current_function = None

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @ visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################

        self.current_type = self.context.get_type(node.id)
        # # print('La bolsa', self.current_type.type_set, type(self.current_type))
        # (Handle all the .TYPE section)
        type_node = self.register_type(node.id)
        # # print('El tipo registrao es: ', type_node)
        type_node.attributes = [attr.name for attr,
                                _ in self.current_type.all_attributes()]
        type_node.methods = [(method.name, self.to_function_name(
            method.name, xtype.name)) for method, xtype in self.current_type.all_methods()]

        func_declarations = (f for f in node.features if isinstance(
            f, cool.MethodDeclarationNode))
        for feature, child_scope in zip(func_declarations, scope.children):
            self.visit(feature, child_scope)

        # init
        self.current_function = self.register_function(self.init_name(node.id))
        # allocate
        instance = self.register_local(VariableInfo('instance', None))
        self.register_instruction(cil.AllocateNode(node.id, instance))

        func = self.current_function
        vtemp = self.define_internal_local()

        # init_attr
        self.current_function = self.register_function(
            self.init_name(node.id, attr=True))
        self.register_param(self.vself)
        if node.parent != 'Object' and node.parent != 'IO':
            self.register_instruction(cil.ArgNode(self.vself.name))
            self.register_instruction(cil.StaticCallNode(
                self.init_name(node.parent, attr=True), vtemp))
        attr_declarations = (f for f in node.features if isinstance(
            f, cool.AttrDeclarationNode))
        for feature in attr_declarations:
            self.visit(feature, scope)

        self.current_function = func
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(
            self.init_name(node.id, attr=True), vtemp))

        self.register_instruction(cil.ReturnNode(instance))
        self.current_function = None

        self.current_type = None

    @ visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(cil.SetAttribNode(
                self.vself.name, node.id, scope.ret_expr, self.current_type))
        elif node.type in self.value_types:
            vtemp = self.define_internal_local()
            self.register_instruction(cil.AllocateNode(node.type, vtemp))
            self.register_instruction(cil.SetAttribNode(
                self.vself.name, node.id, vtemp, self.current_type))

    @ visitor.when(cool.MethodDeclarationNode)
    def visit(self, node: cool.MethodDeclarationNode, scope):

        # # print(f'Los parametros de la method {node.id} son: {node.params}')
        #####################################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> ExpressionNode
        #####################################
        # # print('La bolsa ahora es:', self.current_type.type_set)
        self.current_method = self.current_type.get_method(node.id)
        # print(
        #     f"El current method de {node.id}({self.current_type.name}) es ", self.current_method.return_type.name, type(self.current_method))
        type_name = self.current_type.name
        # # print('El metodaco es: ', self.current_method.name,
        #       'y el type es', type_name)
        self.current_function = self.register_function(
            self.to_function_name(self.current_method.name, type_name))

        # (Handle PARAMS)
        # # print("el vself", type(self.vself))
        self.register_param(self.vself)
        # # print("los params", self.params)

        # TODO: Review node.params[0], node.params tiene la forma ([Types],[Names]) o ([Names],[Types])
        # # print(f'Los params de {node.id} son: {node.params}')
        if(len(node.params)):
            # # print(
            #     f'Los parametros de la method {node.id} son: {node.params}')
            for param_name, param_type in node.params:
                self.register_param(
                    VariableInfo(param_name, param_type))

        # # print("la funcion actul es ", self.current_function.params)
        scope.ret_expr = None
        # # print("params despues de registrarlos", self.params)
        # //TODO: scope children used here ???
        # # print('EL body del method es', node.body)
        self.visit(node.body, scope)
        # (Handle RETURN)
        if scope.ret_expr is None:
            self.register_instruction(cil.ReturnNode(''))
        elif self.current_function.name == 'entry':
            self.register_instruction(cil.ReturnNode(0))
        else:
            self.register_instruction(cil.ReturnNode(scope.ret_expr))

        self.current_method = None

    @ visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.if_body -> ExpressionNode
        # node.else_body -> ExpressionNode
        ##################################
        vret = self.register_local(VariableInfo('if_then_else_value', None))
        vcondition = self.define_internal_local()

        then_label_node = self.register_label('then_label')
        else_label_node = self.register_label('else_label')
        continue_label_node = self.register_label('continue_label')

        # If condition GOTO then_label
        self.visit(node.condition, scope)
        self.register_instruction(cil.GetAttribNode(
            vcondition, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.GotoIfNode(
            vcondition, then_label_node.label))
        # GOTO else_label
        self.register_instruction(cil.GotoNode(else_label_node.label))
        # Label then_label
        self.register_instruction(then_label_node)
        self.visit(node.then_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
        self.register_instruction(cil.GotoNode(continue_label_node.label))
        # Label else_label
        self.register_instruction(else_label_node)
        self.visit(node.else_body, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))

        self.register_instruction(continue_label_node)
        scope.ret_expr = vret

    @ visitor.when(cool.LoopNode)
    def visit(self, node: cool.LoopNode, scope):
        ###################################
        # node.condition -> ExpressionNode
        # node.body -> ExpressionNode
        ###################################

        vcondition = self.define_internal_local()
        while_label_node = self.register_label('while_label')
        loop_label_node = self.register_label('loop_label')
        pool_label_node = self.register_label('pool_label')
        # Label while
        self.register_instruction(while_label_node)
        # If condition GOTO loop
        # print(node.condition)
        self.visit(node.condition, scope)
        # print("scope", scope.ret_expr)
        self.register_instruction(cil.GetAttribNode(
            vcondition, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.GotoIfNode(
            vcondition, loop_label_node.label))
        # GOTO pool
        # print(pool_label_node.label)
        self.register_instruction(cil.GotoNode(pool_label_node.label))
        # Label loop
        self.register_instruction(loop_label_node)
        # print("el body es:", node.body)
        self.visit(node.body, scope)
        # GOTO while
        self.register_instruction(cil.GotoNode(while_label_node.label))
        # Label pool
        self.register_instruction(pool_label_node)

        # The result of a while loop is void
        scope.ret_expr = cil.VoidNode()

    @ visitor.when(cool.BlocksNode)
    def visit(self, node: cool.BlocksNode, scope):
        #######################################
        # node.exprs -> [ ExpressionNode ... ]
        #######################################
        for expr in node.expr_list:
            self.visit(expr, scope)

    @ visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope):
        ############################################
        # node.let_body -> [ LetAttributeNode ... ]
        # node.in_body -> ExpressionNode
        ############################################
        vret = self.register_local(VariableInfo('let_in_value', None))

        for let_attr_node in node.var_decl_list:
            self.visit(let_attr_node, scope)
        self.visit(node.in_expr, scope)
        self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
        scope.ret_expr = vret

    @ visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope):
        ##############################################
        # node.expr -> ExpressionNode
        # node.branches -> [ CaseExpressionNode ... }
        ##############################################
        vexpr = self.register_local(VariableInfo('case_expr_value', None))
        vtype = self.register_local(VariableInfo('typeName_value', None))
        vcond = self.register_local(VariableInfo('equal_value', None))
        vret = self.register_local(VariableInfo('case_value', None))
        self.visit(node.case_expr, scope)
        self.register_instruction(cil.AssignNode(vexpr, scope.ret_expr))
        self.register_instruction(cil.TypeNameNode(vtype, scope.ret_expr))

        # Check if node.expr is void and raise proper error if vexpr value is void
        void = cil.VoidNode()
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vexpr, void))
        # # print('La expresion a analizar es', node.case_expr)

        # token = get_token(node.case_expr)
        # self.register_runtime_error(
        # equal_result,  f'({token.row},{token.column}) - RuntimeError: Case on void\n')

        end_label = self.register_label('end_label')
        labels = []
        old = {}

        # sorting the branches
        order = []
        for b in node.options:
            count = 0
            t1 = self.context.get_type(b.type)
            # print("t1 es", t1, type(t1))
            for other in node.options:
                t2 = self.context.get_type(other.type)
                # print("t2 es:", t2, type(t2))
                # print("el conforms da", t2.conforms_to(t1))
                count += t2.conforms_to(t1)
            order.append((count, b))
        order.sort(key=lambda x: x[0])
        # print([* map(lambda x: x[1].branch_type, order)])
        for idx, (_, b) in enumerate(order):
            # print(b.type)
            labels.append(self.register_label(f'{idx}_label'))
            h = self.buildHierarchy(b.type)
            # print(h)
            if not h:
                self.register_instruction(cil.GotoNode(labels[-1].label))
                break
            h.add(b.type)
            # print(h)
            for s in old:
                h -= s
            for t in h:
                vbranch_type_name = self.register_local(
                    VariableInfo('branch_type_name', None))
                self.register_instruction(cil.NameNode(vbranch_type_name, t))
                self.register_instruction(cil.EqualNode(
                    vcond, vtype, vbranch_type_name))
                self.register_instruction(
                    cil.GotoIfNode(vcond, labels[-1].label))

        # Raise runtime error if no Goto was executed
        data_node = self.register_data(
            f'({node.lineno + 1 + len(node.options)},{node.columnno - 5}) - RuntimeError: Execution of a case statement without a matching branch\n')
        self.register_instruction(cil.ErrorNode(data_node))

        for idx, l in enumerate(labels):
            self.register_instruction(l)
            vid = self.register_local(VariableInfo(
                order[idx][1].id, None), id=True)
            self.register_instruction(cil.AssignNode(vid, vexpr))
            self.visit(order[idx][1], scope)
            self.register_instruction(cil.AssignNode(vret, scope.ret_expr))
            self.register_instruction(cil.GotoNode(end_label.label))

        scope.ret_expr = vret
        self.register_instruction(end_label)

    @ visitor.when(cool.CaseOptionNode)
    def visit(self, node: cool.CaseOptionNode, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        self.visit(node.expr, scope)

    @ visitor.when(cool.VarDeclarationNode)
    def visit(self, node: cool.VarDeclarationNode, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        if node.id in self.ids:
            vname = self.ids[node.id]
        else:
            vname = self.register_local(
                VariableInfo(node.id, node.type), id=True)
        if node.expr:
            self.visit(node.expr, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
        elif node.type in self.value_types:
            self.register_instruction(cil.AllocateNode(node.type, vname))

    @ visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################

        self.visit(node.expr, scope)

        try:
            self.current_type.get_attribute(node.id)
            self.register_instruction(cil.SetAttribNode(
                self.vself.name, node.id, scope.ret_expr, self.current_type.name))
        except AttributeError:
            vname = None
            param_names = [pn.name for pn in self.current_function.params]
            if node.id in param_names:
                for n in param_names:
                    if node.id in n.split("_"):
                        vname = n
                        break
            else:
                for n in [lv.name for lv in self.current_function.localvars]:
                    if node.id in n.split("_"):
                        vname = n
                        break
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))

    @ visitor.when(cool.NotNode)
    def visit(self, node: cool.NotNode, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        value = self.define_internal_local()
        instance = self.define_internal_local()

        self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(
            value, scope.ret_expr, 'value', 'Bool'))
        self.register_instruction(cil.MinusNode(vname, 1, value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Bool'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.LessOrEqualNode)
    def visit(self, node: cool.LessOrEqualNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.GetAttribNode(
            left_value, left, 'value', 'Bool'))
        self.register_instruction(cil.GetAttribNode(
            right_value, right, 'value', 'Bool'))
        self.register_instruction(
            cil.LessEqualNode(vname, left_value, right_value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Bool'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        self.visit(node.left, scope)
        left = scope.ret_expr
        self.visit(node.right, scope)
        right = scope.ret_expr
        self.register_instruction(cil.GetAttribNode(
            left_value, left, 'value', 'Bool'))
        self.register_instruction(cil.GetAttribNode(
            right_value, right, 'value', 'Bool'))
        self.register_instruction(cil.LessNode(vname, left_value, right_value))

        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Bool'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.EqualsNode)
    def visit(self, node: cool.EqualsNode, scope):
        # print("estoy en un equals, por favor no te imprimas")
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        type_left = self.define_internal_local()
        type_int = self.define_internal_local()
        type_bool = self.define_internal_local()
        type_string = self.define_internal_local()
        equal_result = self.define_internal_local()
        left_value = self.define_internal_local()
        right_value = self.define_internal_local()
        instance = self.define_internal_local()

        self.visit(node.left, scope)
        left = scope.ret_expr
        # print("left", scope.ret_expr)
        self.visit(node.right, scope)
        # print("right", scope.ret_expr)
        right = scope.ret_expr

        self.register_instruction(cil.TypeNameNode(type_left, left))
        self.register_instruction(cil.NameNode(type_int, 'Int'))
        self.register_instruction(cil.NameNode(type_bool, 'Bool'))
        self.register_instruction(cil.NameNode(type_string, 'String'))

        int_node = self.register_label('int_label')
        string_node = self.register_label('string_label')
        reference_node = self.register_label('reference_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.EqualNode(
            equal_result, type_left, type_int))
        self.register_instruction(cil.GotoIfNode(equal_result, int_node.label))
        self.register_instruction(cil.EqualNode(
            equal_result, type_left, type_bool))
        self.register_instruction(cil.GotoIfNode(equal_result, int_node.label))
        self.register_instruction(cil.EqualNode(
            equal_result, type_left, type_string))
        self.register_instruction(cil.GotoIfNode(
            equal_result, string_node.label))
        self.register_instruction(cil.GotoNode(reference_node.label))

        self.register_instruction(int_node)
        self.register_instruction(cil.GetAttribNode(
            left_value, left, 'value', 'Int'))
        self.register_instruction(cil.GetAttribNode(
            right_value, right, 'value', 'Int'))
        self.register_instruction(
            cil.EqualNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(string_node)
        self.register_instruction(cil.GetAttribNode(
            left_value, left, 'value', 'String'))
        self.register_instruction(cil.GetAttribNode(
            right_value, right, 'value', 'String'))
        self.register_instruction(
            cil.EqualStrNode(vname, left_value, right_value))
        self.register_instruction(cil.GotoNode(continue_node.label))

        self.register_instruction(reference_node)
        self.register_instruction(cil.EqualNode(vname, left, right))

        self.register_instruction(continue_node)
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Bool'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        # # print(f'El node plus es {node.left} + {node.right}')
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(
            vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(
            vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.PlusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(
            vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(
            vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.MinusNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.StarNode)
    def visit(self, node: cool.StarNode, scope):
        # print("entre a un star node")
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(
            vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(
            vright, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.StarNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        vleft = self.define_internal_local()
        vright = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(
            vleft, scope.ret_expr, 'value', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(
            vright, scope.ret_expr, 'value', 'Int'))

        # Check division by 0
        equal_result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(equal_result, vright, 0))
        # token = get_token(node.right)
        # self.register_runtime_error(
        # equal_result, f'({token.row},{token.column}) - RuntimeError: Division by zero\n')

        self.register_instruction(cil.DivNode(vname, vleft, vright))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        void = cil.VoidNode()
        value = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.AssignNode(value, scope.ret_expr))
        result = self.define_internal_local()
        self.register_instruction(cil.EqualNode(result, value, void))
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(
            cil.StaticCallNode(self.init_name("Bool"), result))
        scope.ret_expr = result

    @ visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        vname = self.define_internal_local()
        value = self.define_internal_local()
        instance = self.define_internal_local()
        self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(
            value, scope.ret_expr, 'value', 'Int'))
        self.register_instruction(cil.ComplementNode(vname, value))
        self.register_instruction(cil.ArgNode(vname))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    # TODO: Unir este con el de abajo
    @ visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope):
        if(node.caller_type == 'SELF_TYPE'):
            return self.visitWhenStatic(node, scope)
        else:

            # print('El id del methodCall es', node.id, node.inferenced_type)
            ######################################
            # node.obj -> ExpressionNode
            # node.id -> str
            # node.args -> [ ExpressionNode ... ]
            # node.type -> str
            #####################################

            args = []
            for arg in node.args:
                vname = self.register_local(
                    VariableInfo(f'{node.id}_arg', None), id=True)
                self.visit(arg, scope)
                self.register_instruction(
                    cil.AssignNode(vname, scope.ret_expr))
                args.append(cil.ArgNode(vname))
            result = self.register_local(VariableInfo(
                f'return_value_of_{node.id}', None), id=True)

            vobj = self.define_internal_local()
            # TODO: esto puede q se parta
            self.visit(node.expr, scope)
            self.register_instruction(cil.AssignNode(vobj, scope.ret_expr))

            # Check if node.obj is void
            void = cil.VoidNode()
            equal_result = self.define_internal_local()
            self.register_instruction(cil.EqualNode(equal_result, vobj, void))

            # token = get_token(node.expr)
            self.register_runtime_error(
                equal_result, f'({node.lineno},{node.columnno}) - RuntimeError: Dispatch on void\n')

            # self
            self.register_instruction(cil.ArgNode(vobj))
            for arg in args:
                self.register_instruction(arg)

            if node.static_type:
                # Call of type<obj>@<type>.id(<expr>,...,<expr>)
                self.register_instruction(cil.StaticCallNode(
                    self.to_function_name(node.id, node.type), result))
            else:
                # Call of type <obj>.<id>(<expr>,...,<expr>)
                type_of_node = self.register_local(
                    VariableInfo(f'{node.id}_type', None), id=True)
                self.register_instruction(cil.TypeOfNode(vobj, type_of_node))
                computed_type = node.expr.exec_inferred_type
                if computed_type.name == 'SELF_TYPE':
                    computed_type = self.current_type
                self.register_instruction(cil.DynamicCallNode(
                    type_of_node, node.id, result, computed_type.name))

            scope.ret_expr = result

    # @visitor.when(cool.MethodCallNode)
    def visitWhenStatic(self, node: cool.MethodCallNode, scope):
        # print('Q tipo es este en el segunndo', node)
        ######################################
        # node.id -> str
        # node.args -> [ ExpressionNode ... ]
        ######################################
        # method = [self.to_function_name(method.name, xtype.name) for method, xtype in self.current_type.all_methods() if method.name == node.id][0]

        args = []
        for arg in node.args:
            vname = self.register_local(
                VariableInfo(f'{node.id}_arg', None), id=True)
            self.visit(arg, scope)
            self.register_instruction(cil.AssignNode(vname, scope.ret_expr))
            args.append(cil.ArgNode(vname))
        result = self.register_local(VariableInfo(
            f'return_value_of_{node.id}', None), id=True)

        self.register_instruction(cil.ArgNode(self.vself.name))
        for arg in args:
            self.register_instruction(arg)

        type_of_node = self.register_local(
            VariableInfo(f'{self.vself.name}_type', None))
        self.register_instruction(
            cil.TypeOfNode(self.vself.name, type_of_node))
        self.register_instruction(cil.DynamicCallNode(
            type_of_node, node.id, result, self.current_type.name))
        # self.register_instruction(cil.StaticCallNode(method, result))
        scope.ret_expr = result

    @ visitor.when(cool.InstantiateNode)
    def visit(self, node: cool.InstantiateNode, scope):
        ###############################
        # node.type -> str
        ###############################
        instance = self.define_internal_local()

        if node.type == 'SELF_TYPE':
            vtype = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(self.vself.name, vtype))
            self.register_instruction(cil.AllocateNode(vtype, instance))
        elif node.type == 'Int' or node.type == 'Bool':
            self.register_instruction(cil.ArgNode(0))
        elif node.type == 'String':
            data_node = [dn for dn in self.dotdata if dn.value == ''][0]
            vmsg = self.register_local(VariableInfo('msg', None))
            self.register_instruction(cil.LoadNode(vmsg, data_node))
            self.register_instruction(cil.ArgNode(vmsg))

        self.register_instruction(cil.StaticCallNode(
            self.init_name(node.type), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.IntNode)
    def visit(self, node: cool.IntNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(int(node.value)))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Int'), instance))
        scope.ret_expr = instance

    # TODO: estoy asumiendo q es VariableNode pero no estoy seguro ni pinga
    @ visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        try:
            # # print(
            #     f"el current cuando analizo {node.value} es {self.current_type}")
            self.current_type.get_attribute(node.value)
            # # print("pude encontrar el tipo")
            attr = self.register_local(VariableInfo(node.value, None), id=True)
            self.register_instruction(cil.GetAttribNode(
                attr, self.vself.name, node.value, self.current_type.name))
            scope.ret_expr = attr
            # # print('En el Variable, llegue al final del try')
        except AttributeError:
            # # print('En el Variable, me fui x el except AttributeError')
            # # print(f"los params de la function {self.current_function.name} son ",
            #       list(map(lambda x: x.name, self.current_function.params)))
            param_names = [pn.name for pn in self.current_function.params]
            if node.value in param_names:
                for n in param_names:
                    if node.value == n:
                        scope.ret_expr = n
                        break
            else:
                # # print(
                #     f"la variable q toy buscando en {self.ids} aqui e", node.value)
                scope.ret_expr = self.ids[node.value]

    @ visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope):
        ###############################
        # node.lex -> str
        ###############################
        try:
            data_node = [
                dn for dn in self.dotdata if dn.value == node.value][0]
        except IndexError:
            data_node = self.register_data(node.value)
        vmsg = self.register_local(VariableInfo('msg', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.LoadNode(vmsg, data_node))
        self.register_instruction(cil.ArgNode(vmsg))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('String'), instance))
        scope.ret_expr = instance

    @ visitor.when(cool.BooleanNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        if node.value == 'false':
            scope.ret_expr = 0
        else:
            scope.ret_expr = 1
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(scope.ret_expr))
        self.register_instruction(cil.StaticCallNode(
            self.init_name('Bool'), instance))
        scope.ret_expr = instance
