from distutils.log import error
from cool_ast.cool_ast import *
import cil_ast.cil_ast as cil
from utils.semantic import Context, SemanticError, Type, Method, Scope, ErrorType, VariableInfo
import visitors.visitor as visitor
# from utils.errors import _TypeError, _NameError, _SemanticError, _AtributeError

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = context

        self.locals = {}
        self.attrs = {}#set()
        self.parameters = set()
        self.instances = []

    def transform_to_keys(self, xtype, keys):
        for i, key in enumerate(keys):
            xtype.attrs[key] = i
        return xtype.attrs
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
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

    def create_ctr(self, class_node, scope):
        attrs = [att for att in class_node.features if isinstance(att, AttrDeclarationNode)]
        while True:
            break
        self.current_function = self.register_function(self.to_function_name('ctor', self.current_type.name))
        self.register_instruction(cil.ParamNode('self'))

        for i, attr in enumerate(attrs):
            set_attr_node = self.visit(attr, scope)
            set_attr_node.index = i
            self.register_instruction(set_attr_node)
        self.register_instruction(cil.ReturnNode(VariableInfo('self', self.current_type)))
        
        
class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    def class_node_from_context(self, type):
        idx = type.name
        features = self.features_from_context(type)
        parent = 'Object' if idx not in ['Object', 'Void'] else None
        return ClassDeclarationNode(idx, features, parent)

    def features_from_context(self, type):
        feats = [AttrDeclarationNode(feat.name, feat.type) for feat in type.attributes]
        for func in type.methods:
            feats.append(FuncDeclarationNode(func.name, func.param_names, func.return_type, None))
        
        return feats

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        
        # class_nodes = [self.class_node_from_context(c) for c in self.context.types]
        built_in_classes = [self.class_node_from_context(self.context.types[c]) for c in self.context.types]



        self.current_function = self.register_function('entry')
        instance = self.define_internal_local()
        self.instances.append(instance)
        result = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('Main', instance))
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.ReturnNode(0))
        self.current_function = None
        
        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        self.instances.pop()
        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        
        # Your code here!!! (Handle all the .TYPE section)
        type_node = self.register_type(node.id)

        attributes = []
        methods = []
        # self.attrs.clear()
        self.attrs = {}
            
        current_type = self.current_type
        while True:
            attr_temp = []
            method_temp = []
            for attr in current_type.attributes:
                # self.attrs.add(attr.name)
                # self.attrs[attr.name] = []
                attr_temp.append(attr.name)
            
            for method in current_type.methods:
                method_temp.append((method.name, self.to_function_name(method.name, current_type.name)))
            
            attributes = attr_temp + attributes
            methods = method_temp + methods
            
            if current_type.parent is None:
                break
            
            current_type = current_type.parent
            
        self.attrs = self.transform_to_keys(type_node, attributes)# type_node.attributes = attributes
        type_node.methods = methods
        self.create_ctr(node, scope)
        
        # attributes
        # for feature, child_scope in zip(node.features, scope.children):
        #     if isinstance(feature, FuncDeclarationNode):
        #         continue
        #     self.visit(feature, child_scope)
        
        # func_declarations = (f for f in node.features if isinstance(f, FuncDeclarationNode))
        for feature, child_scope in zip(node.features, scope.children):
            if isinstance(feature, FuncDeclarationNode):
                self.visit(feature, child_scope)
        
        #falta visitar los atributos
        
        self.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.value = ExpressionNode
        ###############################
        # local function to determine the default value of an attribute given its type
        def default_value_init(type):
            if type == 'Int':
                return ConstantNumNode(0)
            elif type == 'Bool':
                return FalseNode()
            elif type == 'String':
                return StringNode("")
            else:
                return VoidNode()
        if node.value:
            value = self.visit(node.value, scope)

        else:
            default_value = default_value_init(node.type)
            if isinstance(default_value, VoidNode):
                value = 'void'
            else:
                value = self.visit(default_value, scope)
            self_ref = VariableInfo('self', self.current_type)
            self_ref.index = 0
            return cil.SetAttribNode(self_ref, node.id, value)
        
        ## old code
        # elif node.type in ["Int", "String", "Object", "IO", "Bool"]:
        #     value = self.define_internal_local()
        #     self.register_instruction(cil.AllocateNode(node.type, value))
        # else:
        #     value = self.define_internal_local()
        #     self.register_instruction(cil.AllocateNode("Void", value))
        # #revisar que poner como el attr del SettAttribnode
        
        # attr = self.attrs[node.id]
        # self.register_instruction(cil.SetAttribNode(self.instances[-1], attr, value))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        
        self.current_method = self.current_type.get_method(node.id, self.current_type, False)
        
        # Your code here!!! (Handle PARAMS)
        self.current_function = self.register_function(self.to_function_name(node.id, self.current_type.name))

        self.parameters.clear()
        self.params.append(cil.ParamNode('self'))
        for arg_name, ptype in node.params:
            self.parameters.add((arg_name, ptype))
            self.params.append(cil.ParamNode(arg_name))
            self.register_instruction(cil.ParamNode(arg_name))
        
        self.locals.clear()
        return_value = self.visit(node.body, scope)
        
        if node.body and 'Void' != node.type: 
            self.register_instruction(cil.ReturnNode(return_value))
        else:
            result = self.define_internal_local()
            self.register_instruction(cil.AllocateNode("Void", result))
            self.register_instruction(cil.ReturnNode(result))
            
        self.current_method = None

    @visitor.when(VarDeclarationNode) # AssignNode
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        var = scope.find_variable(node.id)
        dest = self.locals[var.name] = self.register_local(var)
        
        if node.expr is not None:
            source = self.visit(node.expr, scope)
        else:
            # asignar valor por default
            if node.type.lower() == 'int':
                source = 0
            elif node.type.lower() == 'string':
                source = ''
            elif node.type.lower() == 'bool':
                source = False
            else:
                source = None 
        self.register_instruction(cil.AssignNode(dest, source))
        return dest
            
    @visitor.when(AssignNode) # 
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        source = self.visit(node.expr, scope)
        
        if node.id in self.locals:
            dest = self.locals[node.id]
            self.register_instruction(cil.AssignNode(dest, source))
            return dest
        elif node.id in self.attrs.keys():
            attr = self.attrs[node.id]
            var = self.define_internal_local()
            self.register_instruction(cil.SetAttribNode(self.instances[-1], attr, source))
            self.register_instruction(cil.GetAttribNode(var, self.instances[-1], attr))
            return var
        else:
            for (p_name, p_type) in self.parameters:
                if node.id == p_name:
                    dest = VariableInfo(p_name, p_type)
                    self.register_instruction(cil.AssignNode(dest, source))
                    return dest

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.method -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        error_label = self.define_internal_local()
        dest = self.define_internal_local()
        if node.obj is not None: # dynamic
            obj = self.visit(node.obj, scope)
            self.instances.append(obj)
            if isinstance(node.obj, InstantiateNode):
                obj_type = node.obj.lex
            else:
                obj_type = scope.find_variable(node.obj.lex).type.name
            
            local = self.define_internal_local()
            self.register_instruction(cil.TypeOfNode(obj, local))
            
            condition = self.define_internal_local()
            self.register_instruction(cil.IsTypeNode(condition, local, "Void"))
            self.register_instruction(cil.GotoIfNode(error_label, condition))
            
            self.register_instruction(cil.ArgNode(obj))
            for arg in node.args:
                self.register_instruction(cil.ArgNode(self.visit(arg, scope)))
            
            obj_type = obj_type if node.parent == None else node.parent
            self.register_instruction(cil.DynamicCallNode(local, self.to_function_name(node.method, obj_type), dest))
        else: # static
            self.register_instruction(cil.ArgNode(self.instances[-1]))
            for arg in node.args:
                self.register_instruction(cil.ArgNode(self.visit(arg, scope)))
                
            self.register_instruction(cil.StaticCallNode(self.to_function_name(node.method, self.current_type.type.name), dest))
        
        self.register_instruction(cil.LabelNode(error_label))
        self.instances.pop()
        return dest

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        constant = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Int", constant))
        self.register_instruction(cil.SetAttribNode(constant, 0, int(node.lex)))
        return constant

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        var = self.define_internal_local()
        if node.lex in self.locals:
            var_aux = self.locals[node.lex].name
            self.register_instruction(cil.AssignNode(var, var_aux))
        elif node.lex in self.attrs.keys():
            self.register_instruction(cil.GetAttribNode(var, self.instances[-1], self.attrs[node.lex]))
        return var

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        dest = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.lex, dest))
        return dest

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.PlusNode(dest, left, right))
        return dest

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.MinusNode(dest, left, right))
        return dest

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.StarNode(dest, left, right))
        return dest

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.DivNode(dest, left, right))
        return dest

    @visitor.when(ChunkNode)
    def visit(self, node, scope):
        ###############################
        # node.chunk -> [ ExpressionNode... ]
        ###############################
        value = None
        for expression in node.chunk:
            value = self.visit(expression, scope.children[0])
        return value

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ###############################
        # node.ifChunk -> ExpressionNode
        # node.thenChunk -> ExpressionNode
        # node.elseChunk -> ExpressionNode
        ###############################

        var = self.define_internal_local()
        then_label = self.define_internal_local()
        else_label = self.define_internal_local()

        ifexpr = self.visit(node.ifChunk, scope.children[0])
        self.register_instruction(cil.GotoIfNode(then_label, ifexpr))

        # else
        elseexpr = self.visit(node.elseChunk, scope.children[2])
        self.register_instruction(cil.AssignNode(var, elseexpr))
        self.register_instruction(cil.GotoNode(else_label))

        # then 
        self.register_instruction(cil.LabelNode(then_label))
        thenexpr = self.visit(node.thenChunk, scope.children[1])
        self.register_instruction(cil.AssignNode(var, thenexpr))

        self.register_instruction(cil.LabelNode(else_label))
        return var

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        ###############################
        # node.decl_list -> [ DeclarationNode... ]
        # node.expression -> ExpressionNode
        ###############################

        for decl in node.decl_list:
            # var = self.visit(decl, scope)
            self.visit(decl, scope)

        value = self.visit(node.expression, scope)
        
        return value

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        while_label = self.define_internal_local()
        loop_label = self.define_internal_local()
        end_label = self.define_internal_local()

        self.register_instruction(cil.LabelNode(while_label))

        while_expr = self.visit(node.condition, scope)
        self.register_instruction(cil.GotoIfNode(loop_label, while_expr))
        
        self.register_instruction(cil.GotoNode(end_label))
        self.register_instruction(cil.LabelNode(loop_label))

        self.visit(node.loopChunk, scope)
        self.register_instruction(cil.GotoNode(while_label))
        
        self.register_instruction(cil.LabelNode(end_label))
        
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Void", result))
        return result

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expression -> ExpressionNode
        ###############################
        bool_instance = self.visit(node.expression, scope)
        
        one = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Int", one))
        self.register_instruction(cil.SetAttribNode(one, 0, 1))
        
        bool_value = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Int", bool_value))

        var = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(var, bool_instance, 0))
        self.register_instruction(cil.SetAttribNode(bool_value, 0, var))
        
        new_var = self.define_internal_local()
        self.register_instruction(cil.MinusNode(new_var, one, bool_value))
        self.register_instruction(cil.SetAttribNode(bool_instance, 0, new_var))
        
        return bool_instance

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        ###############################
        # node.method -> ExpressionNode
        ###############################
        expr_value = self.visit(node.method, scope)
        var = self.define_internal_local()
        self.register_instruction(cil.IsTypeNode(var, expr_value, "Void"))
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Bool", result))
        self.register_instruction(cil.SetAttribNode(result, 0, var))
        return result

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        value = self.visit(node.expr, scope)
        var = self.define_internal_local()
        zero = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Int", zero))
        self.register_instruction(cil.MinusNode(var, zero, value))
        self.regster_instruction(cil.SetAttribNode(value, 0, var))
        return value

    @visitor.when(SwitchCaseNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        # node.case_list = [ (id, type, expr)... ]
        ###############################
        start_case_label = self.define_internal_local()
        end_case_label = self.define_internal_local()
        error_label = self.define_internal_local()
        
        obj = self.visit(node.expr, scope)
        obj_type = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(obj, obj_type))
        
        result = self.define_internal_local()
        self.register_instruction(cil.LabelNode(start_case_label))
        
        condition = self.define_internal_local()
        self.register_instruction(cil.IsTypeNode( condition, obj_type, 'Void'))
        self.register_instruction(cil.GotoIfNode(error_label, condition))
        
        for case in node.case_list:
            case_id, case_type, case_expr = case 
            current_label = self.define_internal_local()
            next_label = self.define_internal_local()
            
            condition = self.define_internal_local()
            self.register_instruction(cil.IsTypeNode(condition, obj_type, case_type))
            self.register_instruction(cil.GotoIfNode(current_label, condition))
            
            self.register_instruction(cil.GotoNode(next_label))
            self.register_instruction(cil.LabelNode(current_label))
            
            info = VariableInfo(case_id, case_type)
            var = self.locals[case_id] = self.register_local(info)
            self.register_instruction(cil.AssignNode(var, obj))
            
            result_expr = self.visit(case_expr, scope)
            self.register_instruction(cil.AssignNode( result, result_expr))
            self.register_instruction(cil.GotoNode(end_case_label))
            
            self.register_instruction(next_label)
        
        var = self.define_internal_local()
        self.register_instruction(cil.ParentTypeNode(var, obj_type))
        self.register_instruction(cil.AssignNode(obj_type, var))

        self.register_instruction(cil.GotoNode(start_case_label))
        
        self.register_instruction(cil.LabelNode(error_label))
        self.register_instruction(cil.ParamNode(self.instances[-1]))
        self.regster_instruction(cil.DynamicCallNode(var, self.to_function_name("abort", self.current_type.name), result))
        
        self.register_instruction(cil.GotoNode(end_case_label))
        return result

    @visitor.when(TrueNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Bool", var))
        self.register_instruction(cil.SetAttribNode(var, 0, 1))
        return var

    @visitor.when(FalseNode)
    def visit(self, node, scope):
        var = self.define_internal_local()
        self.register_instruction(cil.AllocateNode("Bool", var))
        return var

    @visitor.when(StringNode)
    def visit(self, node, scope):
        data_node = self.register_data(node.lex)
        var = self.define_internal_local()
        self.register_instruction(cil.LoadNode(var, data_node))
        return data_node.name

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.LessNode(dest, left, right))
        return dest
    
    @visitor.when(LeqNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.LeqNode(dest, left, right))
        return dest

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        self.register_instruction(cil.EqualNode(dest, left, right))
        return dest
