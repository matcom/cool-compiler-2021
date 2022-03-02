from ...cmp.ast import (
    ProgramNode,
    ClassDeclarationNode,
    AttrDeclarationNode,
    FuncDeclarationNode,
)
from ...cmp.semantic import (
    Context,
    SemanticError,
    ErrorType,
    InferencerManager,
    AutoType,
    SelfType,
    Type,
)
from ..utils import (
    ALREADY_DEFINED,
    MAIN_CLASS_ERROR,
    MAIN_PROGRAM_ERROR,
    SELF_ERROR,
)
from typing import List, Optional, Tuple
import compiler.visitors.visitor as visitor


class TypeBuilder:
    def __init__(self, context):
        self.context: Context = context
        self.current_type: Optional[Type] = None
        self.errors: List[Tuple[Exception, Tuple[int, int]]] = []
        self.manager = InferencerManager()

        self.obj_type = self.context.get_type("Object")

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for dec in node.declarations:
            self.visit(dec)

        self.check_main_class()

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode):
        self.current_type = self.context.get_type(node.id)
        for feat in node.features:
            self.visit(feat)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode):
        ## Building param-names and param-types of the method
        param_names = []
        param_types = []
        node.index = []
        for namex, typex in node.params:
            n, t = namex.lex, typex.lex
            node.index.append(None)

            # Checking param name can't be self
            if n == "self":
                self.errors.append((SemanticError(SELF_ERROR), namex.pos))

            # Generate valid parameter name
            if n in param_names:
                self.errors.append(
                    (
                        SemanticError(ALREADY_DEFINED % (n)),
                        namex.pos,
                    )
                )
            while True:
                if n in param_names:
                    n = f"1{n}"
                else:
                    param_names.append(n)
                    break

            try:
                t = self.context.get_type(t)
                if isinstance(t, SelfType):
                    t = SelfType(self.current_type)
                elif isinstance(t, AutoType):
                    node.index[-1] = self.manager.assign_id(self.obj_type)
            except TypeError as ex:
                self.errors.append((ex, typex.pos))
                t = ErrorType()
            param_types.append(t)

        # Checking return type
        try:
            rtype = self.context.get_type(node.type)
            if isinstance(rtype, SelfType):
                rtype = SelfType(self.current_type)
        except TypeError as ex:
            self.errors.append((ex, node.typeToken.pos))
            rtype = ErrorType()

        node.idx = (
            self.manager.assign_id(self.obj_type)
            if isinstance(rtype, AutoType)
            else None
        )

        # Defining the method in the current type. There can not be another method with the same name.
        try:
            self.current_type.define_method(
                node.id, param_names, param_types, rtype, node.index, node.idx
            )
        except SemanticError as ex:
            self.errors.append((ex, node.token.pos))

    @visitor.when(AttrDeclarationNode)
    def visit(self, node: AttrDeclarationNode):
        # Checking attribute type
        try:
            attr_type = self.context.get_type(node.type)
            if isinstance(attr_type, SelfType):
                attr_type = SelfType(self.current_type)
        except TypeError as ex:
            self.errors.append((ex, node.typeToken.pos))
            attr_type = ErrorType()

        node.idx = (
            self.manager.assign_id(self.obj_type)
            if isinstance(attr_type, AutoType)
            else None
        )

        # Checking attribute can't be named self
        if node.id == "self":
            self.errors.append(
                (
                    SemanticError(SELF_ERROR),
                    node.idToken.pos,
                )
            )

        # Checking attribute name. No other attribute can have the same name
        flag = False
        try:
            self.current_type.define_attribute(node.id, attr_type, node.idx)
            flag = True
        except SemanticError as ex:
            self.errors.append(
                (
                    SemanticError(ALREADY_DEFINED % (node.id)),
                    node.idToken.pos,
                )
            )

        while not flag:
            node.id = f"1{node.id}"
            try:
                self.current_type.define_attribute(node.id, attr_type, node.idx)
                flag = True
            except SemanticError:
                pass

    def check_main_class(self):
        try:
            typex = self.context.get_type("Main")
            if not any(method.name == "main" for method in typex.methods):
                self.errors.append((SemanticError(MAIN_CLASS_ERROR), (0, 0)))
        except TypeError:
            self.errors.append((SemanticError(MAIN_PROGRAM_ERROR), (0, 0)))
