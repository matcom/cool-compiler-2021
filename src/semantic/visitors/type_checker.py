from utils.ast import *
from utils import visitor
from utils.errors import *
from semantic.tools import *
from semantic.types import *
from utils.utils import Utils

class TypeChecker:
    def __init__(self, context:Context, errors=[]):
        self.context:Context = context
        self.errors:list = errors
        self.current_type:Type = None
        self.current_method:Method = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope:Scope):
        for declaration,new_scope in zip(node.declarations, scope.children):
            self.visit(declaration, new_scope)

    def _get_type(self, ntype:str, pos:tuple):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as exception:
            self.errors.append(exception)
            return ErrorType()

    def _get_method(self, typex:Type, name:str, pos:tuple) -> Method:
        try:
            return typex.get_method(name, pos)
        except SemanticError as exception:
            if type(typex) != ErrorType and type(typex) != AutoType:
                error_text = AttributesError.DISPATCH_UNDEFINED % name
                self.errors.append(AttributesError(*pos, error_text))
            return MethodError(name, [], [], ErrorType())

    @visitor.when(ClassDeclarationNode)
    def visit(self, node:ClassDeclarationNode, scope:Scope):
        self.current_type = self.context.get_type(node.id, node.pos)
        func_declaration = [ feature for feature in node.features 
                                if isinstance(feature, FuncDeclarationNode) ]

        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)

        for feature,child_scope in zip(func_declaration, scope.functions.values()):
            self.visit(feature, child_scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node:AttrDeclarationNode, scope:Scope):
        attr = self.current_type.get_attribute(node.id, node.pos)
        var_type = Utils.GetType(attr.type, self.current_type)
        typex = self.visit(node.expr, scope)

        if not typex.conforms_to(var_type):
            error_text = TypesError.ATTR_TYPE_ERROR % (typex.name, attr.name, var_type.name)
            self.errors.append(TypesError(*node.pos, error_text))
            return ErrorType()
        return typex

    @visitor.when(FuncDeclarationNode)
    def visit(self, node:FuncDeclarationNode, scope:Scope):
        parent = self.current_type.parent
        method = self.current_type.get_method(node.id, node.pos)
        self.current_method = self.current_type.get_method(node.id, node.pos)

        if parent is not None:
            try:
                old_method = parent.get_method(node.id, node.pos)
                if old_method.return_type.name != method.return_type.name:
                    error_text = SemanticError.WRONG_SIGNATURE_RETURN % (node.id, method.return_type.name, old_method.return_type.name)
                    self.errors.append(SemanticError(*node.type_pos, error_text))
                if len(method.param_names) != len(old_method.param_names):
                    error_text = SemanticError.WRONG_NUMBER_PARAM % node.id
                    self.errors.append(SemanticError(*node.pos, error_text))
                for (name,param),type1,type2 in zip(node.params, method.param_types, old_method.param_types):
                    if type1.name != type2.name:
                        error_text = SemanticError.WRONG_SIGNATURE_PARAMETER % (name, type1.name, type2.name)
                        self.errors.append(SemanticError(*param.pos, error_text))
            except SemanticError:
                pass

        result = self.visit(node.body, scope)
        return_type = Utils.GetType(method.return_type, self.current_type)

        if not result.conforms_to(return_type):
            error_text = TypesError.RETURN_TYPE_ERROR % (result.name, return_type.name)
            self.errors.append(TypesError(*node.type_pos, error_text))

    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope:Scope):
        var_type = self._get_type(node.type, node.type_pos)
        var_type = Utils.GetType(var_type, self.current_type)
        if node.expr != None:
            typex = self.visit(node.expr, scope)
            if not typex.conforms_to(var_type):
                error_text = TypesError.UNCONFORMS_TYPE % (typex.name, node.id, var_type.name)
                self.errors.append(TypesError(*node.type_pos, error_text))
            return typex
        return var_type

    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope:Scope):
        var_info = self.find_variable(scope, node.id)
        var_type = Utils.GetType(var_info.type, self.current_type) 
        typex = self.visit(node.expr, scope)
        if not typex.conforms_to(var_type):
            error_text = TypesError.UNCONFORMS_TYPE % (typex.name, node.id, var_type.name)
            self.errors.append(TypesError(*node.pos, error_text))
        return typex

    def check_args(self, method:Method, scope:Scope, args:list, pos:tuple):
        arg_types = [ self.visit(arg, scope) for arg in args ]
        if len(arg_types) > len(method.param_types):
            error_text = SemanticError.ARGUMENT_ERROR % method.name
            self.errors.append(SemanticError(*pos, error_text))
        elif len(arg_types) < len(method.param_types):
            for arg,arg_info in zip(method.param_names[len(arg_types):], args[len(arg_types):]):
                error_text = SemanticError.ARGUMENT_ERROR % (method.name)
                self.errors.append(SemanticError(*arg_info.pos, error_text))
        for arg_type,param_type,param_name in zip(arg_types, method.param_types, method.param_names):
            if not arg_type.conforms_to(param_type):
                error_text = TypesError.INCOSISTENT_ARG_TYPE % (method.name, arg_type.name, param_name, param_type.name)
                self.errors.append(TypesError(*pos, error_text))

    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope:Scope):
        stype = self.visit(node.obj, scope)
        method = self._get_method(stype, node.id, node.pos)
        if not isinstance(method, MethodError):
            self.check_args(method, scope, node.args, node.pos)
        return Utils.GetType(method.return_type, stype)

    @visitor.when(BaseCallNode)
    def visit(self, node:BaseCallNode, scope:Scope):
        obj = self.visit(node.obj, scope)
        typex = self._get_type(node.type, node.type_pos)
        if not obj.conforms_to(typex):
            error_text = TypesError.INCOMPATIBLE_TYPES_DISPATCH % (typex.name, obj.name)
            self.errors.append(TypesError(*node.type_pos, error_text))
            return ErrorType()
        method = self._get_method(typex, node.id, node.pos)
        if not isinstance(method, MethodError):
            self.check_args(method, scope, node.args, node.pos)
        return Utils.GetType(method.return_type, typex)

    @visitor.when(StaticCallNode)
    def visit(self, node:StaticCallNode, scope:Scope):
        typex = self.current_type
        method = self._get_method(typex, node.id, node.pos)
        if not isinstance(method, MethodError):
            self.check_args(method, scope, node.args, node.pos)
        return Utils.GetType(method.return_type, typex)

    @visitor.when(ConstantNumNode)
    def visit(self, node:ConstantNumNode, scope:Scope):
        return IntType(node.pos)

    @visitor.when(ConstantBoolNode)
    def visit(self, node:ConstantBoolNode, scope:Scope):
        return BoolType(node.pos)

    @visitor.when(ConstantStrNode)
    def visit(self, node:ConstantStrNode, scope:Scope):
        return StringType(node.pos)

    @visitor.when(ConstantVoidNode)
    def visit(self, node:ConstantVoidNode, scope:Scope):
        return VoidType(node.pos)

    def find_variable(self, scope, lex):
        var_info = scope.find_local(lex)
        if var_info is None:
            var_info = scope.find_attribute(lex)
        if lex in self.current_type.attributes and var_info is None:
            return VariableInfo(lex, VoidType())
        return var_info

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope:Scope):
        typex = self.find_variable(scope, node.lex).type
        return Utils.GetType(typex, self.current_type)

    @visitor.when(InstantiateNode)
    def visit(self, node:InstantiateNode, scope:Scope):
        try:
            typex = self.context.get_type(node.lex, node.pos)
        except SemanticError:
            typex = ErrorType()
            error_text = TypesError.NEW_UNDEFINED_CLASS % node.lex
            self.errors.append(TypesError(*node.pos, error_text))
        return Utils.GetType(typex, self.current_type)

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope:Scope):
        cond = self.visit(node.cond, scope)
        if cond.name != 'Bool':
            error_text = TypesError.LOOP_CONDITION_ERROR
            self.errors.append(TypesError(*node.pos, error_text))   
        self.visit(node.expr, scope)
        return ObjectType()

    @visitor.when(IsVoidNode)
    def visit(self, node:IsVoidNode, scope:Scope):
        self.visit(node.expr, scope)
        return BoolType()

    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope:Scope):
        cond = self.visit(node.cond, scope)
        if cond.name != 'Bool':
            error_text = TypesError.PREDICATE_ERROR % ('if', 'Bool')
            self.errors.append(TypesError(*node.pos, error_text))
        true_type = self.visit(node.stm, scope)
        false_type = self.visit(node.else_stm, scope)
        return Utils.GetCommonBaseType([false_type, true_type])

    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope:Scope):
        value = None
        for exp in node.expr_list:
            value = self.visit(exp, scope)
        return value

    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope:Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        return self.visit(node.expr, child_scope)

    @visitor.when(CaseNode) 
    def visit(self, node:CaseNode, scope:Scope):
        type_expr = self.visit(node.expr, scope)
        new_scope = scope.expr_dict[node]
        types, var_types = [], []
        for case,case_scope in zip(node.case_list, new_scope.children):
            typex,_ = self.visit(case, case_scope)
            types.append(typex)
            if case.typex in var_types:
                error_text = SemanticError.DUPLICATE_CASE_BRANCH % case.typex
                self.errors.append(SemanticError(*case.type_pos, error_text))
            var_types.append(case.typex)
        return Utils.GetCommonBaseType(types)

    @visitor.when(OptionNode)
    def visit(self, node:OptionNode, scope:Scope):
        var_info = self.find_variable(scope, node.id)
        typex = self.visit(node.expr, scope)
        return typex, var_info.type

    def binary_operation(self, node, scope:Scope, operator:str):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        int_type = IntType()
        if left_type != int_type or right_type != int_type:
            error_text = TypesError.BOPERATION_NOT_DEFINED % (left_type.name, operator, right_type.name)
            self.errors.append(TypesError(*node.pos, error_text))
            return ErrorType()
        if operator == '<' or operator == '<=':
            return BoolType()
        return int_type

    @visitor.when(PlusNode)
    def visit(self, node:PlusNode, scope:Scope):
        return self.binary_operation(node, scope, '+')
    
    @visitor.when(MinusNode)
    def visit(self, node:MinusNode, scope:Scope):
        return self.binary_operation(node, scope, '-')
    
    @visitor.when(StarNode)
    def visit(self, node:StarNode, scope:Scope):
        return self.binary_operation(node, scope, '*')
    
    @visitor.when(DivNode)
    def visit(self, node:DivNode, scope:Scope):
        return self.binary_operation(node, scope, '/')
    
    @visitor.when(LessEqNode)
    def visit(self, node:LessEqNode, scope:Scope):
        return self.binary_operation(node, scope, '<=')

    @visitor.when(LessNode)
    def visit(self, node:LessNode, scope:Scope):
        return self.binary_operation(node, scope, '<')

    @visitor.when(EqualNode)
    def visit(self, node:EqualNode, scope:Scope):
        left_type = self.visit(node.left, scope)
        right_type = self.visit(node.right, scope)
        if (left_type == IntType() or right_type == IntType() or 
                left_type == StringType() or right_type == StringType() or 
                    left_type == BoolType() or right_type == BoolType()) and \
                        left_type != right_type:
            error_text = TypesError.COMPARISON_ERROR
            self.errors.append(TypesError(*node.pos, error_text))
            return ErrorType()
        else:
            return BoolType()

    @visitor.when(NotNode)
    def visit(self, node:NotNode, scope:Scope):
        left_type = self.visit(node.expr, scope)
        typex = BoolType()
        if left_type != typex:
            error_text = TypesError.UOPERATION_NOT_DEFINED % ('not', left_type.name, typex.name)
            self.errors.append(TypesError(*node.pos, error_text))
            return ErrorType()
        return typex

    @visitor.when(BinaryNotNode)
    def visit(self, node:BinaryNotNode, scope:Scope):
        left_type = self.visit(node.expr, scope)
        int_type = IntType()
        if left_type != int_type:
            error_text = TypesError.UOPERATION_NOT_DEFINED % ('~', left_type.name, int_type.name)
            self.errors.append(TypesError(*node.pos, error_text))
            return ErrorType()
        return int_type
