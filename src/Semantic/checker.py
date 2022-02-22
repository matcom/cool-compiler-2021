import Tools.visitor as visitor

from Parser.ast import *
from Tools.utils import *
from Tools.context import *
from Tools.scope import VariableInfo
from Tools.errors import SemanticError, AttributesError, TypesError

class TypeChecker:
    def __init__(self, context):
        self.context = context
        self.errors = []

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        for declaration, new_scope in zip(node.declarations, scope.children):
            self.visit(declaration, new_scope)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id, node.pos)
        fd = [feat for feat in node.features if isinstance(feat, FuncDeclarationNode)]
        for feat in node.features:
            if isinstance(feat, AttrDeclarationNode):
                self.visit(feat, scope)
        for feat, child_scope in zip(fd, scope.functions.values()):
            self.visit(feat, child_scope)  
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        attr = self.current_type.get_attribute(node.id, node.pos)
        vartype = get_type(attr.type, self.current_type)
        self.current_index = attr.index
        typex = self.visit(node.expr, scope)
        self.current_index = None
        if not typex.conforms_to(vartype):
            self.errors.append(TypesError(ATTR_TYPE_ERROR %(typex.name, attr.name, vartype.name), *node.pos))
            return ErrorType()
        return typex
       
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        parent = self.current_type.parent        
        self.current_method = method = self.current_type.get_method(node.id, node.pos)
        if parent is not None:
            try:
                old_meth = parent.get_method(node.id, node.pos)
                if old_meth.return_type.name != method.return_type.name:
                    self.errors.append(SemanticError(WRONG_SIGNATURE_RETURN % (node.id, method.return_type.name, old_meth.return_type.name), *node.type_pos))
                if len(method.param_names) != len(old_meth.param_names):
                    self.errors.append(SemanticError(WRONG_NUMBER_PARAM % node.id, *node.pos))
                for (name, param), type1, type2 in zip(node.params, method.param_types, old_meth.param_types):
                    if type1.name != type2.name:
                        self.errors.append(SemanticError(WRONG_SIGNATURE_PARAMETER % (name, type1.name, type2.name) , *param.pos))
            except SemanticError: pass       
        result = self.visit(node.body, scope)
        return_type = get_type(method.return_type, self.current_type)
        if not result.conforms_to(return_type):
            self.errors.append(TypesError(RETURN_TYPE_ERROR %(result.name, return_type.name), *node.type_pos))
  
    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope):
        vtype =  self.get_type(node.type, node.type_pos)
        vtype = get_type(vtype, self.current_type)
        if node.expr != None:
            typex = self.visit(node.expr, scope)
            if not typex.conforms_to(vtype):        
                self.errors.append(TypesError(UNCONFORMS_TYPE %(typex.name, node.id, vtype.name), *node.type_pos))
            return typex
        return vtype        
        
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        vinfo = self.find_variable(scope, node.id)
        vtype = get_type(vinfo.type, self.current_type)      
        typex = self.visit(node.expr, scope)
        if not typex.conforms_to(vtype):       
            self.errors.append(TypesError(UNCONFORMS_TYPE %(typex.name, node.id, vtype.name) , *node.pos))
        return typex        

    def _check_args(self, meth, scope, args, pos):
        arg_types = [self.visit(arg, scope) for arg in args]      
        if len(arg_types) > len(meth.param_types):
            self.errors.append(SemanticError(ARGUMENT_ERROR % meth.name, *pos))
        elif len(arg_types) < len(meth.param_types):
            for arg, arg_info in zip(meth.param_names[len(arg_types):], args[len(arg_types):]):
                self.errors.append(SemanticError(ARGUMENT_ERROR % (meth.name), *arg_info.pos))
        for atype, ptype, param_name in zip(arg_types, meth.param_types, meth.param_names):
            if not atype.conforms_to(ptype):
                self.errors.append(TypesError(INCOSISTENT_ARG_TYPE % (meth.name, atype.name, param_name, ptype.name), *pos))   

    @visitor.when(CallNode)
    def visit(self, node, scope):
        stype = self.visit(node.obj, scope)
        meth = self.get_method(stype, node.id, node.pos)
        if not isinstance(meth, MethodError):
            self._check_args(meth, scope, node.args, node.pos)
        return get_type(meth.return_type, stype)
        

    @visitor.when(BaseCallNode)
    def visit(self, node, scope):
        obj = self.visit(node.obj, scope)
        typex = self.get_type(node.type, node.type_pos)
        if not obj.conforms_to(typex):
            self.errors.append(TypesError(INCOMPATIBLE_TYPES_DISPATCH % (typex.name, obj.name), *node.type_pos))
            return ErrorType()       
        meth = self.get_method(typex, node.id, node.pos)
        if not isinstance(meth, MethodError):
            self._check_args(meth, scope, node.args, node.pos)    
        return get_type(meth.return_type, typex)
              

    @visitor.when(StaticCallNode)
    def visit(self, node, scope):
        typex = self.current_type
        meth = self.get_method(typex, node.id, node.pos)
        if not isinstance(meth, MethodError):
            self._check_args(meth, scope, node.args, node.pos)
        return get_type(meth.return_type, typex)

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        return IntType(node.pos)

    @visitor.when(ConstantBoolNode)
    def visit(self, node, scope):
        return BoolType(node.pos)
   
    @visitor.when(ConstantStrNode)
    def visit(self, node, scope):
        return StringType(node.pos)

    @visitor.when(ConstantVoidNode)
    def visit(self, node, scope):
        return VoidType(node.pos)

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        typex = self.find_variable(scope, node.lex).type
        return get_type(typex, self.current_type)

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            type_ = self.context.get_type(node.lex, node.pos)
        except SemanticError:
            type_ = ErrorType()
            self.errors.append(TypesError(NEW_UNDEFINED_CLASS % node.lex, *node.pos))
        return get_type(type_, self.current_type)
    
    @visitor.when(WhileNode)
    def visit(self, node, scope):
        cond = self.visit(node.cond, scope)      
        if cond.name != 'Bool':
            self.errors.append(TypesError(LOOP_CONDITION_ERROR, *node.pos))   
        self.visit(node.expr, scope)
        return ObjectType()

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        return BoolType()

    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        cond = self.visit(node.cond, scope)
        if cond.name != 'Bool':
            self.errors.append(TypesError(PREDICATE_ERROR % ('if', 'Bool'), *node.pos))     
        true_type = self.visit(node.stm, scope)
        false_type = self.visit(node.else_stm, scope)   
        return get_common_basetype([false_type, true_type])
        
    @visitor.when(BlockNode)
    def visit(self, node, scope):
        value = None
        for exp in node.expr_list:
            value = self.visit(exp, scope)
        return value

    @visitor.when(LetNode)
    def visit(self, node, scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        return self.visit(node.expr, child_scope)
    
    @visitor.when(CaseNode) 
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        new_scope = scope.expr_dict[node]
        types = []
        var_types = []
        for case, c_scope in zip(node.case_list, new_scope.children):
            case: OptionNode
            t, vt = self.visit(case, c_scope)
            types.append(t)
            if case.typex in var_types:
                self.errors.append(SemanticError(DUPLICATE_CASE_BRANCH % case.typex, *case.type_pos))
            var_types.append(case.typex)
        return get_common_basetype(types)
        
    @visitor.when(OptionNode)
    def visit(self, node, scope):
        var_info = self.find_variable(scope, node.id)
        typex = self.visit(node.expr, scope)
        return typex, var_info.type

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '+')
    
    @visitor.when(MinusNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '-')
    
    @visitor.when(StarNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '*')
    
    @visitor.when(DivNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '/')
    
    @visitor.when(LessEqNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '<=')

    @visitor.when(LessNode)
    def visit(self, node, scope):
        return self.binary_operation(node, scope, '<')

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if (ltype == IntType() or rtype == IntType() or ltype == StringType() or rtype == StringType() or ltype == BoolType() or rtype == BoolType()) and ltype != rtype:
            self.errors.append(TypesError(COMPARISON_ERROR, *node.pos))
            return ErrorType()
        else: return BoolType()

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        typex = BoolType()
        if ltype != typex:
            self.errors.append(TypesError(UOPERATION_NOT_DEFINED %('not', ltype.name, typex.name), *node.pos))
            return ErrorType()
        return typex

    @visitor.when(BinaryNotNode)
    def visit(self, node, scope):
        ltype = self.visit(node.expr, scope)
        int_type = IntType()
        if ltype != int_type:
            self.errors.append(TypesError(UOPERATION_NOT_DEFINED %('~', ltype.name, int_type.name), *node.pos))
            return ErrorType()
        return int_type

    def find_variable(self, scope, lex):
        var_info = scope.find_local(lex)
        if var_info is None:
            var_info = scope.find_attribute(lex)
        if lex in self.current_type.attributes and var_info is None:
            return VariableInfo(lex, VoidType())
        return var_info

    def binary_operation(self, node, scope, operator):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        int_type = IntType()
        if ltype != int_type or rtype != int_type:
            self.errors.append(TypesError(BOPERATION_NOT_DEFINED %(ltype.name, operator, rtype.name), *node.pos))
            return ErrorType()
        if operator == '<' or operator == '<=':
            return BoolType()
        return int_type

    def get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as error:
            self.errors.append(error)
            return ErrorType()

    def get_method(self, typex, name, pos):
        try:
            return typex.get_method(name, pos)
        except SemanticError as error:
            if type(typex) != ErrorType and type(typex) != AutoType:
                self.errors.append(AttributesError(DISPATCH_UNDEFINED % name, *pos))
            return MethodError(name, [], [], ErrorType())