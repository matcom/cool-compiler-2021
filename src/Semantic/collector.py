import Tools.visitor as visitor
from Parser.ast import *
from Tools.context import *
from Tools.messages import *
from Tools.errors import SemanticError, NamesError
from Tools.scope import Scope

class TypeCollector:
    def __init__(self):
        self.errors = []
        self.context = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        self.context.types['String'] = StringType()
        self.context.types['Int'] = IntType()
        self.context.types['Bool'] = BoolType()
        self.context.types['Object'] = ObjectType()
        self.context.types['SELF_TYPE'] = SelfType()
        self.context.types['IO'] = IOType()
        for dec in node.declarations:
            self.visit(dec)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        if node.id in ['String', 'Int', 'Object', 'Bool', 'SELF_TYPE', 'IO']:
            self.errors.append(SemanticError(REDEFINITION_ERROR % node.id, *node.pos))      
        try:
            self.context.create_type(node.id, node.pos)
        except SemanticError as error:
            self.errors.append(error)        
        if not node.parent:
            node.parent = 'Object'

class VariableCollector:
    def __init__(self, context):
        self.context = context
        self.errors = []
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = Scope()
        for dec in node.declarations:
            self.visit(dec, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.get_type(node.id, node.pos)
        scope.define_variable('self', self.current_type)       
        for feat in node.features:
            if isinstance(feat, AttrDeclarationNode):
                self.visit(feat, scope)              
        for attr, _ in self.current_type.all_attributes():
            if scope.find_attribute(attr.name) is None:
                scope.define_attribute(attr)      
        for feat in node.features:
            if isinstance(feat, FuncDeclarationNode):
                self.visit(feat, scope)
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        attr = self.current_type.get_attribute(node.id, node.pos)
        if node.expr is None:
            self.define_default_value(attr.type, node)
        else:
            self.visit(node.expr, scope)
        attr.expr = node.expr
        scope.define_attribute(attr)
   
    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        parent = self.current_type.parent 
        pnames = [param[0] for param in node.params]
        ptypes = [param[1] for param in node.params]
        self.current_method = self.current_type.get_method(node.id, node.pos)
        new_scope = scope.create_child()
        scope.functions[node.id] = new_scope
        for pname, ptype in node.params:
            if pname == 'self':
                self.errors.append(SemanticError(SELF_PARAM, *ptype.pos)) 
            new_scope.define_variable(pname, self.get_type(ptype.value, ptype.pos))           
        self.visit(node.body, new_scope)
  
    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):
        if node.id == 'self':
            self.errors.append(SemanticError(SELF_IN_LET, *node.pos))
            return

        try:
            vtype = self.context.get_type(node.type, node.pos)
        except SemanticError:
            self.errors.append(TypesError(UNDEFINED_TYPE_LET % (node.type, node.id), *node.type_pos))
            vtype = ErrorType()

        vtype = self.get_type(node.type, node.type_pos)
        var_info = scope.define_variable(node.id, vtype)
       
        if node.expr is not None:
            self.visit(node.expr, scope)
        else:
            self.define_default_value(vtype, node)
             
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        if node.id == 'self':
            self.errors.append(SemanticError(SELF_IS_READONLY, *node.pos))
            return   
        vinfo = scope.find_variable(node.id)
        if vinfo is None:
            var_info = scope.find_attribute(node.id)
            if var_info is None:
                self.errors.append(NamesError(VARIABLE_NOT_DEFINED %(node.id)  , *node.pos))
                vtype = ErrorType()
                scope.define_variable(node.id, vtype)         
        self.visit(node.expr, scope)
    
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        for exp in node.expr_list:
            self.visit(exp, scope)
    
    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        n_scope = scope.create_child()
        scope.expr_dict[node] = n_scope
        for init in node.init_list:
            self.visit(init, n_scope) 
        self.visit(node.expr, n_scope)

    @visitor.when(BinaryNode)
    def visit(self, node:BinaryNode, scope:Scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
 
    @visitor.when(UnaryNode)
    def visit(self, node:UnaryNode, scope:Scope):
        self.visit(node.expr, scope)
     
    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        try:
            return self.current_type.get_attribute(node.lex, node.pos).type
        except AttributesError:
            if not scope.is_defined(node.lex):
                self.errors.append(NamesError(VARIABLE_NOT_DEFINED %(node.lex), *node.pos))
                vinfo = scope.define_variable(node.lex, ErrorType(node.pos))
            else:
                vinfo = scope.find_variable(node.lex)
            return vinfo.type

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.expr, scope)

    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        self.visit(node.cond, scope)
        self.visit(node.stm, scope)
        self.visit(node.else_stm, scope)

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
        self.visit(node.expr, scope)
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        self.visit(node.obj, scope)
        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(BaseCallNode)
    def visit(self, node:BaseCallNode, scope:Scope):
        self.visit(node.obj, scope)
        for arg in node.args:
            self.visit(arg, scope)
    
    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        for arg in node.args:
            self.visit(arg, scope)

    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        self.visit(node.expr, scope)
        new_scp = scope.create_child()
        scope.expr_dict[node] = new_scp
        for case in node.case_list:
            self.visit(case, new_scp.create_child())
        
    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        try:
            typex = self.context.get_type(node.typex, node.type_pos)
        except TypesError:
            self.errors.append(TypesError(CLASS_CASE_BRANCH_UNDEFINED % node.typex, *node.type_pos))
            typex = ErrorType()
        scope.define_variable(node.id, typex)
        self.visit(node.expr, scope)

    def get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    def define_default_value(self, typex, node):
            if typex == IntType():
                node.expr = ConstantNumNode(0)
            elif typex == StringType():
                node.expr = ConstantStrNode("")
            elif typex == BoolType():
                node.expr = ConstantBoolNode('false')
            else:
                node.expr = ConstantVoidNode(node.id)