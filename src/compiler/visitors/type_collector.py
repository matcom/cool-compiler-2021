from typing import Dict, List, Optional, Tuple
from numpy import void
from zmq import TYPE
from compiler.cmp.utils import Token, pprint
import compiler.visitors.visitor as visitor
from ..cmp.semantic import (
    SemanticError,
    Type,
    Context,
    ObjectType,
    IOType,
    StringType,
    IntType,
    BoolType,
    SelfType,
    AutoType,
)
from ..cmp.ast import ProgramNode, ClassDeclarationNode

built_in_types = []


class TypeCollector(object):
    def __init__(self):
        self.context: Optional[Context] = None
        self.errors: List[Tuple[Exception, Tuple[int, int]]] = []
        self.parent: Dict[str, Optional[Token]] = {}

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        self.context = Context()
        self.define_built_in_types()

        # Adding built-in types to context
        for typex in built_in_types:
            self.context.types[typex.name] = typex

        for declaration in node.declarations:
            self.visit(declaration)

        self.check_parents()
        self.check_cyclic_inheritance()

        # Order class declarations according to their depth in the inheritance tree
        node.declarations = self.order_types(node)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode) -> void:
        # flag is set to True if the class is succesfully added to the context
        flag = False
        try:
            if node.id == "AUTO_TYPE":
                raise SemanticError("Name of class can't be autotype")
            self.context.create_type(node.id, node.tokenId.pos)
            flag = True
            self.parent[node.id] = node.parent
        except SemanticError as ex:
            self.errors.append((ex, node.token.pos))

        # changing class id so it can be added to context
        while not flag:
            node.id = f"1{node.id}"
            try:
                self.context.create_type(node.id)
                flag = True
                self.parent[node.id] = node.parent
            except SemanticError:
                pass

    def define_built_in_types(self) -> void:
        objectx = ObjectType()
        iox = IOType()
        intx = IntType()
        stringx = StringType()
        boolx = BoolType()
        self_type = SelfType()
        autotype = AutoType()

        # Object Methods
        objectx.define_method("abort", [], [], objectx, [])
        objectx.define_method("type_name", [], [], stringx, [])
        objectx.define_method("copy", [], [], self_type, [])

        # IO Methods
        iox.define_method("out_string", ["x"], [stringx], self_type, [None])
        iox.define_method("out_int", ["x"], [intx], self_type, [None])
        iox.define_method("in_string", [], [], stringx, [])
        iox.define_method("in_int", [], [], intx, [])

        # String Methods
        stringx.define_method("length", [], [], intx, [])
        stringx.define_method("concat", ["s"], [stringx], stringx, [None])
        stringx.define_method("substr", ["i", "l"], [intx, intx], stringx, [None])

        # Setting Object as parent
        iox.set_parent(objectx)
        stringx.set_parent(objectx)
        intx.set_parent(objectx)
        boolx.set_parent(objectx)

        built_in_types.extend([objectx, iox, stringx, intx, boolx, self_type, autotype])

    def check_parents(self) -> void:
        for item in self.parent.keys():
            item_type = self.context.get_type(item)
            if self.parent[item] is None:
                # setting Object as parent
                item_type.set_parent(built_in_types[0])
            else:
                try:
                    typex = self.context.get_type(self.parent[item].lex)
                    if not typex.can_be_inherited():
                        self.errors.append(
                            (
                                SemanticError(
                                    f"Class {item} can not inherit class {typex.name}"
                                ),
                                self.parent[item].pos,
                            )
                        )
                        typex = built_in_types[0]
                    item_type.set_parent(typex)
                except SemanticError as ex:
                    self.errors.append(
                        (
                            TypeError(
                                f"Class {item_type.name} inherits from an undefined class {self.parent[item].lex}."
                            ),
                            self.parent[item].pos,
                        )
                    )
                    item_type.set_parent(built_in_types[0])

    def check_cyclic_inheritance(self) -> void:
        flag = []

        def find(item: Type) -> int:
            for i, typex in enumerate(flag):
                if typex.name == item.name:
                    return i
            return len(flag)

        def check_path(idx: int, item: Type) -> void:
            while True:
                flag.append(item)
                parent = item.parent
                if parent is None:
                    break
                pos = find(parent)
                if pos < len(flag):
                    if pos >= idx:
                        self.errors.append(
                            (SemanticError("Cyclic heritage."), item.pos)
                        )
                        item.parent = built_in_types[0]
                    break
                item = parent

        for item in self.context.types.values():
            idx = find(item)
            if idx == len(flag):
                check_path(idx, item)

    def order_types(self, node: ProgramNode):
        sorted_declarations: List[ClassDeclarationNode] = []
        flag = [False] * len(node.declarations)

        change = True
        while change:
            change = False

            current = []
            for i, dec in enumerate(node.declarations):
                if not flag[i]:
                    typex = self.context.get_type(dec.id)
                    if typex.parent.name in [
                        item.id for item in sorted_declarations
                    ] or any(typex.parent.name == bit.name for bit in built_in_types):
                        current.append(dec)
                        flag[i] = True
                        change = True

            sorted_declarations.extend(current)

        return sorted_declarations
