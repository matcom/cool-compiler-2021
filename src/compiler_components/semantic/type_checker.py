import sys
sys.path.append('../')
from ..ast import *
from .structures import *
from . import visitor

class TypeChecker:
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope=None):
        for dec in node.declarations:
            try:
                self.visit(dec,scope.create_child())
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))


    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):      
        try :
            typex = self.context.get_type(node.id, node.line)
            
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))

        self.current_type = typex
        #for at in typex.all_attributes():
        #    scope.define_variable(at[0].name, at[0].type,node.line)
        scope.define_variable("self",typex,node.line)
        mscope = scope.create_child()
        ascope = scope.create_child()
        for feat in node.features:
            if isinstance(feat, FuncDeclarationNode):
                self.visit(feat,mscope.create_child())
            else:
                self.visit(feat, ascope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode,scope:Scope):
        node_type = self.context.get_type(node.type)
        scope.define_variable(node.id, node_type)
        if not node.expr is None:
            self.visit(node.expr, scope.create_child())
            try:
    
                typex =self.current_type if node.type == "SELF_TYPE" else self.context.get_type(node.type,node.line)
                self.context.check_type(node.expr.type,typex,node.line)
            except SemanticError as e:
                self.errors.append(f"({node.type_line},{node.type_column}) - TypeError: " + str(e))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode,scope:Scope):

        method = self.current_type.get_method(node.id, node.line, node.column)
        
        for i in range(len(method.param_names)):
            try:
                if method.param_names[i] == "self":
                    raise SemanticError('Trying to assign value to self' ,node.line)
                
                scope.define_variable(method.param_names[i],method.param_types[i],node.line)
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))

        self.visit(node.body,scope.create_child())
        try:
            typex = method.return_type if not isinstance(method.return_type,SELF_TYPE) else self.current_type

            self.context.check_type(node.body.type,typex,node.line)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column-4}) - TypeError: " + str(e))
        

    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope:Scope):
        node.type = ErrorType()
        sce = scope.create_child()
        self.visit(node.expr, sce)
        scb = scope.create_child()
        common_type = None
        typesbr = set()
        for branches in node.list_case:
            tmpscope = scb.create_child()
            if branches.type in typesbr:
                self.errors.append(f"({branches.line},{branches.column}) - SemanticError: Type in more than one branch")
            typesbr.add(branches.type)
            try :
                typex = self.context.get_type(branches.type,branches.expr.line)
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
            tmpscope.define_variable(branches.id,typex,node.line)
            self.visit(branches.expr,tmpscope)
            if common_type is None:
                common_type = branches.expr.type
            else:
                common_type = self.context.closest_common_antecesor(common_type,branches.expr.type)
        
        node.type = common_type
        
        



    @visitor.when(DispatchNode)
    def visit(self, node:DispatchNode, scope:Scope):    
        self.visit(node.expr,scope.create_child())
        
        node.type = ErrorType()
        node.typexa = node.typex
        for i in range(len(node.params)):
            self.visit(node.params[i],scope.create_child())

        if not node.typex is None:            
            try:
                temp = self.context.get_type(node.typex,node.line)
                self.context.check_type(node.expr.type,temp,node.line)
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
                return
        else:
            if  isinstance( node.expr.type , ErrorType):
                return
            node.typex = node.expr.type.name
        try:
            typex = self.context.get_type(node.typex,node.line)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
            return
        try :
            if  isinstance( typex , ErrorType):
                return
            method = typex.get_method(node.id,node.line)
            
            ret_type = method.return_type  if not isinstance(method.return_type,SELF_TYPE) else typex    
            node.type = ret_type
            if len(method.param_types) != len(node.params):
                raise ParamError()
            for i in range(len(node.params)):
                try:
                    self.context.check_type(node.params[i].type,method.param_types[i],node.line)
                except SemanticError as e:
                    self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - AttributeError: dispatch undeclared method {node.f}")
        except ParamError as p:
            self.errors.append(f'({node.line},{node.column}) - SemanticError: Method takes {len(method.param_types)} params but {len(node.params)} were given')

    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):    
        node.type = ErrorType()
        for i in range(len(node.args)):
            self.visit(node.args[i],scope.create_child())

        typex = self.current_type
        try :
            if  isinstance( typex , ErrorType):
                return
            method = typex.get_method(node.id, node.line)
            ret_type = method.return_type  if not isinstance(method.return_type,SELF_TYPE) else typex    
            node.type = ret_type
            if len(method.param_types) != len(node.args):
                raise SemanticError (f'Method {node.id} takes {len(method.param_types)} params but {len(node.args)} were given')
            for i in range(len(node.args)):
                try:
                    self.context.check_type(node.args[i].type,method.param_types[i],node.line)
                except SemanticError as e:
                    self.errors.append(f"({node.line},{node.column}) - Type: " + str(e))
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - AttributeError: " + str(e))


        

    @visitor.when(IfNode)
    def visit(self,node:IfNode,scope:Scope):
        self.visit(node.if_c,scope.create_child())
        try:
            self.context.check_type(node.if_c.type,self.context.get_type("Bool"),node.line)
        except SemanticError as e:
            self.errors.append(f"({node.if_c.line},{node.if_c.column}) - TypeError: " + str(e))
        
        self.visit(node.then_c,scope.create_child())
        
        self.visit(node.else_c, scope.create_child())
        try:    
            node.type = self.context.closest_common_antecesor(node.then_c.type, node.else_c.type)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
            node.type =  ErrorType()


    @visitor.when(AssignNode)
    def visit(self, node:AssignNode,scope:Scope):
        self.visit(node.expr, scope.create_child())
        try:
            if node.id == "self":
                raise SemanticError('Trying to assign value to self' ,node.line)

            var = scope.find_variable(node.id)
            
            if var is None:
                try:
                    at =  [ at[0] for at in self.current_type.all_attributes() if at[0].name == node.id]
                    var = at[0]
                except:
                    raise SemanticError(f"({node.line}, {node.column}) - NameError: Undeclared identifier {node.id}")

            typex = self.current_type if isinstance(var.type , SELF_TYPE) else var.type

            self.context.check_type(node.expr.type, typex, node.line)
            node.type = node.expr.type
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
            node.type = node.expr.type
     

    @visitor.when(WhileNode)
    def visit(self , node:WhileNode, scope:Scope):
        self.visit(node.condition, scope.create_child())
        if self.context.get_type("Bool",node.line) != node.condition.type:
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr should be boolean")
        self.visit(node.body, scope.create_child())
        node.type = self.context.get_type("Object", node.line)
          

    @visitor.when(BlockNode)
    def visit (self, node:BlockNode, scope:Scope):
        for expr in node.expr_list:
            self.visit(expr,scope.create_child())
        node.type = node.expr_list[-1].type

    @visitor.when(SelfNode)
    def visit(self, node:SelfNode, scope:Scope):
        node.type = self.current_type    

    @visitor.when(LetNode)
    def visit(self, node:LetNode,scope:Scope):
        sc = scope.create_child()
        for init in node.list_decl:
            if not init is None:
                if(not init.expr is None):
                    self.visit(init.expr,sc)
                    try:
                        typex = self.context.get_type(init.expr.type.name,node.line) if  init.expr.type != "SELF_TYPE" else self.current_type
                        typey = self.context.get_type(init.type,node.line) if  init.expr.type != "SELF_TYPE" else self.current_type
                        self.context.check_type(typex,typey,node.line)
                    except SemanticError as e:
                        self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
                        

            sc = sc.create_child()
            typex= None
            try:
                typex = self.context.get_type(init.type,node.line) if  init.type != "SELF_TYPE" else self.current_type
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
                typex = ErrorType()
            try:    
                if init.id == "self":
                    raise SemanticError('Trying to assign value to self' ,node.line)    
                sc.define_variable(init.id,typex,node.line)
            except SemanticError as e:
                self.errors.append(f"({node.line},{node.column}) - SemanticError: " + str(e))
        
        sc = sc.create_child()
        node.body_scope=sc
        self.visit(node.expr,sc)
        node.type = node.expr.type
        

    @visitor.when(InstantiateNode)
    def visit(self, node:InstantiateNode,scope:Scope):
        try:
            if node.lex == "SELF_TYPE":
                node.type= self.current_type
            else:
                node.type = self.context.get_type(node.lex,node.line)
        except SemanticError as e:
            self.errors.append(f"({node.line},{node.column}) - TypeError: " + str(e))
            node.type = ErrorType()

        

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
       
        self.visit(node.expr,scope.create_child())
        node.type = self.context.get_type("Bool", node.line)
        

    @visitor.when(ArithmeticNode)
    def visit(self, node:ArithmeticNode,scope:Scope):
        self.visit(node.left,scope.create_child())
        self.visit(node.right,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line) or node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: static types of the two sub-expressions must be Int.")
        
        node.type = self.context.get_type("Int", node.line)
        

    @visitor.when(MinorNode)
    def visit(self, node:MinorNode,scope:Scope):
        self.visit(node.left,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be Int not " + str(node.left.type))
        self.visit(node.right,scope.create_child())
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be Int not " + str(node.right.type))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(MinorEqualsNode)
    def visit(self, node:MinorEqualsNode, scope:Scope):
        self.visit(node.left,scope.create_child())
        if node.left.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be Int not " + str(node.left.type))
        self.visit(node.right,scope.create_child())
        if node.right.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be Int not " + str(node.right.type))
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(EqualsNode)
    def visit(self, node:EqualsNode, scope:Scope):
        self.visit(node.left,scope.create_child())
        self.visit(node.right,scope.create_child())
        if node.left.type != node.right.type:
            basic = ['Int', 'String', 'Bool']
            if node.left.type.name in basic or node.right.type.name in basic:
                self.errors.append(f"({node.line},{node.column}) - TypeError: Ilegal comparison with a basic type")
        node.type = self.context.get_type("Bool", node.line)

    @visitor.when(NhanharaNode)
    def visit(self, node:NhanharaNode, scope:Scope):
        self.visit(node.expr, scope.create_child())
        if node.expr.type != self.context.get_type("Int", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be an int not " + str(node.expr.type))
        node.type = self.context.get_type("Int", node.line)

    @visitor.when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        self.visit(node.expr, scope.create_child())
        if node.expr.type != self.context.get_type("Bool", node.line):
            self.errors.append(f"({node.line},{node.column}) - TypeError: Expr must be Bool not " + str(node.expr.type))
        node.type = self.context.get_type("Bool", node.line)


    @visitor.when(ConstantNumNode)
    def visit (self, node:ConstantNumNode,scope:Scope):
        node.type = self.context.get_type("Int", node.line)        

    @visitor.when(ConstantStringNode)
    def visit (self, node:ConstantStringNode, scope:Scope):
        node.type = self.context.get_type("String", node.line)

    @visitor.when(ConstantBooleanNode)
    def visit (self, node:ConstantBooleanNode, scope:Scope):
        node.type = self.context.get_type("Bool",node.line)

    @visitor.when(VariableNode)
    def visit (self, node:VariableNode,scope:Scope):
    
        x = scope.find_variable(node.lex)
        if x is None:
            try:
                at = [at[0] for at in self.current_type.all_attributes() if at[0].name == node.lex]
                x = at[0]
            except:    
                node.type = ErrorType()
                self.errors.append(f"({node.line}, {node.column}) - NameError: Undeclared identifier {node.lex}")
                return
        node.type = x.type if not isinstance(x.type , SELF_TYPE) else self.current_type
       
