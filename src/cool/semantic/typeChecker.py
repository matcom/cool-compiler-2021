from .helpers import *
from .types import *
from ..utils import *


class TypeChecker:
    def __init__(self, context: Context, errors=[]):
        self.context: Context = context
        self.current_type: Type = None
        self.current_method: Method = None
        self.errors = errors
        self.current_index = None

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        for d, new_scope in zip(node.declarations, scope.children):
            self.visit(d, new_scope)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id, node.pos)

        for f in node.features:
            if isinstance(f, AttrDeclarationNode):
                self.visit(f, scope)

        for f, child_scope in zip([ft for ft in node.features if isinstance(ft, FuncDeclarationNode)],
                                  scope.functions.values()):
            self.visit(f, child_scope)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode, scope: Scope):
        attr = self.current_type.get_attribute(node.id, node.pos)
        attr_type = get_type(attr.type, self.current_type)

        self.current_index = attr.index
        _type = self.visit(node.expr, scope)
        self.current_index = None

        if not _type.conforms_to(attr_type):
            error_text = TypesError.ATTR_TYPE_ERROR % (_type.name, attr.name, attr_type.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()

        return _type

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        parent = self.current_type.parent

        self.current_method = c_m = self.current_type.get_method(node.id, node.pos)

        if parent is not None:
            try:
                old_meth = parent.get_method(node.id, node.pos)
                if old_meth.return_type.name != c_m.return_type.name:
                    error_text = SemanticError.WRONG_SIGNATURE_RETURN % (
                        node.id, c_m.return_type.name, old_meth.return_type.name)
                    self.errors.append(SemanticError(error_text, *node.type_pos))
                if len(c_m.param_names) != len(old_meth.param_names):
                    error_text = SemanticError.WRONG_NUMBER_PARAM % node.id
                    self.errors.append(SemanticError(error_text, *node.pos))
                for (name, param), type1, type2 in zip(node.params, c_m.param_types, old_meth.param_types):
                    if type1.name != type2.name:
                        error_text = SemanticError.WRONG_SIGNATURE_PARAMETER % (name, type1.name, type2.name)
                        self.errors.append(SemanticError(error_text, *param.pos))
            except SemanticError:
                pass

        ans = self.visit(node.body, scope)
        return_type = get_type(c_m.return_type, self.current_type)

        if not ans.conforms_to(return_type):
            error_text = TypesError.RETURN_TYPE_ERROR % (ans.name, return_type.name)
            self.errors.append(TypesError(error_text, *node.type_pos))

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        _type = get_type(self.context.get_type(node.type, node.pos), self.current_type)

        if node.expr is not None:
            _n_type = self.visit(node.expr, scope)
            if not _n_type.conforms_to(_type):
                error_text = TypesError.UNCONFORMS_TYPE % (_type.name, node.id, _type.name)
                self.errors.append(TypesError(error_text, *node.type_pos))
            return _n_type

        return _type

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        _info = self.find_variable(scope, node.id)
        _type = get_type(_info.type, self.current_type)

        n_type = self.visit(node.expr, scope)

        if not n_type.conforms_to(_type):
            error_text = TypesError.UNCONFORMS_TYPE % (n_type.name, node.id, _type.name)
            self.errors.append(TypesError(error_text, *node.pos))
        return n_type

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        _type = self.visit(node.obj, scope)

        try:
            method = _type.get_method(node.id, node.pos)
        except SemanticError as e:
            if type(_type) != ErrorType and type(_type) != AutoType:
                error_text = AttributesError.DISPATCH_UNDEFINED % node.id
                self.errors.append(AttributesError(error_text, *node.pos))
            method = MethodError(node.id, [], [], ErrorType())

        if not isinstance(method, MethodError):
            self._validate_args(method, scope, node.args, node.pos)

        return get_type(method.return_type, _type)

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        obj = self.visit(node.obj, scope)
        _type = self._get_type(node.type, node.type_pos)

        if not obj.conforms_to(_type):
            error_text = TypesError.INCOMPATIBLE_TYPES_DISPATCH % (_type.name, obj.name)
            self.errors.append(TypesError(error_text, *node.type_pos))
            return ErrorType()

        method = self._get_method(_type, node.id, node.pos)
        if not isinstance(method, MethodError):
            self._validate_args(method, scope, node.args, node.pos)

        return get_type(method.return_type, _type)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode, scope: Scope):
        _type = self.current_type

        method = self._get_method(_type, node.id, node.pos)
        if not isinstance(method, MethodError):
            self._validate_args(method, scope, node.args, node.pos)

        return get_type(method.return_type, _type)

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):
        return IntType(node.pos)

    @visitor.when(ConstantBoolNode)
    def visit(self, node: ConstantBoolNode, scope: Scope):
        return BoolType(node.pos)

    @visitor.when(ConstantStrNode)
    def visit(self, node: ConstantStrNode, scope: Scope):
        return StringType(node.pos)

    @visitor.when(ConstantVoidNode)
    def visit(self, node: ConstantVoidNode, scope: Scope):
        return VoidType(node.pos)

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        _type = self.find_variable(scope, node.lex).type
        return get_type(_type, self.current_type)

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope: Scope):
        try:
            _type = self.context.get_type(node.lex, node.pos)
        except SemanticError:
            _type = ErrorType()
            error_text = TypesError.NEW_UNDEFINED_CLASS % node.lex
            self.errors.append(TypesError(error_text, *node.pos))

        return get_type(_type, self.current_type)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        cond = self.visit(node.cond, scope)

        if cond.name != 'Bool':
            self.errors.append(TypesError(TypesError.LOOP_CONDITION_ERROR, *node.pos))

        self.visit(node.expr, scope)
        return ObjectType()

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        self.visit(node.expr, scope)
        return BoolType()

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        cond = self.visit(node.cond, scope)

        if cond.name != 'Bool':
            error_text = TypesError.PREDICATE_ERROR % ('if', 'Bool')
            self.errors.append(TypesError(error_text, *node.pos))

        true_type = self.visit(node.stm, scope)
        false_type = self.visit(node.else_stm, scope)

        return get_common_base_type([false_type, true_type])

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        value = None
        for exp in node.expr_list:
            value = self.visit(exp, scope)
        return value

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)
        return self.visit(node.expr, child_scope)

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        type_expr = self.visit(node.expr, scope)

        new_scope = scope.expr_dict[node]
        types = []
        var_types = []
        for case, c_scope in zip(node.case_list, new_scope.children):
            case: OptionNode
            t, vt = self.visit(case, c_scope)
            types.append(t)
            if case.typex in var_types:
                error_text = SemanticError.DUPLICATE_CASE_BRANCH % case.typex
                self.errors.append(SemanticError(error_text, *case.type_pos))
            var_types.append(case.typex)

        return get_common_base_type(types)

    @visitor.when(OptionNode)
    def visit(self, node: OptionNode, scope: Scope):
        var_info = self.find_variable(scope, node.id)
        _type = self.visit(node.expr, scope)
        return _type, var_info.type

    def binary_operation(self, node, scope, operator):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        int_type = IntType()
        if ltype != int_type or rtype != int_type:
            error_text = TypesError.BOPERATION_NOT_DEFINED % (ltype.name, operator, rtype.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        if operator == '<' or operator == '<=':
            return BoolType()
        return int_type

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        return self.binary_operation(node, scope, '+')

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        return self.binary_operation(node, scope, '-')

    @visitor.when(StarNode)
    def visit(self, node: StarNode, scope: Scope):
        return self.binary_operation(node, scope, '*')

    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: Scope):
        return self.binary_operation(node, scope, '/')

    @visitor.when(LessEqNode)
    def visit(self, node: DivNode, scope: Scope):
        return self.binary_operation(node, scope, '<=')

    @visitor.when(LessNode)
    def visit(self, node: DivNode, scope: Scope):
        return self.binary_operation(node, scope, '<')

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        ltype = self.visit(node.left, scope)
        rtype = self.visit(node.right, scope)
        if (
                ltype == IntType() or rtype == IntType() or ltype == StringType() or rtype == StringType() or ltype == BoolType() or rtype == BoolType()) and ltype != rtype:
            error_text = TypesError.COMPARISON_ERROR
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        else:
            return BoolType()

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        ltype = self.visit(node.expr, scope)
        _type = BoolType()
        if ltype != _type:
            error_text = TypesError.UOPERATION_NOT_DEFINED % ('not', ltype.name, _type.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        return _type

    @visitor.when(BinaryNotNode)
    def visit(self, node: BinaryNotNode, scope: Scope):
        ltype = self.visit(node.expr, scope)
        int_type = IntType()
        if ltype != int_type:
            error_text = TypesError.UOPERATION_NOT_DEFINED % ('~', ltype.name, int_type.name)
            self.errors.append(TypesError(error_text, *node.pos))
            return ErrorType()
        return int_type

    def _validate_args(self, method: Method, scope: Scope, args, pos):
        arg_types = [self.visit(arg, scope) for arg in args]

        if len(arg_types) > len(method.param_types):
            error_text = SemanticError.ARGUMENT_ERROR % method.name
            self.errors.append(SemanticError(error_text, *pos))
        elif len(arg_types) < len(method.param_types):
            for arg, arg_info in zip(method.param_names[len(arg_types):], args[len(arg_types):]):
                error_text = SemanticError.ARGUMENT_ERROR % method.name
                self.errors.append(SemanticError(error_text, *arg_info.pos))

        for atype, ptype, param_name in zip(arg_types, method.param_types, method.param_names):
            if not atype.conforms_to(ptype):
                error_text = TypesError.INCOSISTENT_ARG_TYPE % (method.name, atype.name, param_name, ptype.name)
                self.errors.append(TypesError(error_text, *pos))

    def _get_type(self, _type: str, pos):
        try:
            return self.context.get_type(_type, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    def _get_method(self, _type: Type, name: str, pos) -> Method:
        try:
            return _type.get_method(name, pos)
        except SemanticError as e:
            if type(_type) != ErrorType and type(_type) != AutoType:
                error_text = AttributesError.DISPATCH_UNDEFINED % name
                self.errors.append(AttributesError(error_text, *pos))
            return MethodError(name, [], [], ErrorType())

    def find_variable(self, scope, lex):
        var_info = scope.find_local(lex)

        if var_info is None:
            var_info = scope.find_attribute(lex)

        if lex in self.current_type.attributes and var_info is None:
            return VariableInfo(lex, VoidType())

        return var_info
