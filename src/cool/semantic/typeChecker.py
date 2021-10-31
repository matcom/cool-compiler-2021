from .helpers import *
from .types import *
from ..utils import *


class TypeChecker:
    def __int__(self, context: Context, errors=[]):
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

        ans = self.visit(node.body, node.pos)
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
