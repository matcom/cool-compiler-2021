from typing import Dict, List, Optional

import cool.code_generation.cil as cil
import cool.code_generation.icool as icool
import cool.semantics.utils.astnodes as cool
import cool.visitor.visitor as visitor
from cool.code_generation.base import BaseCOOLToCILVisitor
from cool.semantics.utils.scope import Context, Method, Scope, Type


class ConstructorCreator:
    def __init__(self, context: Context):
        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.context: Context = context
        self.class_declarations = {}  # type: Dict[str, cool.ClassDeclarationNode]

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        declarations: List[cool.ClassDeclarationNode] = []

        for declaration in node.declarations:
            self.class_declarations[declaration.id] = declaration

        for declaration in node.declarations:
            declarations.append(self.visit(declaration, scope))

        return cool.ProgramNode(declarations)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        ancestors = [
            self.class_declarations[owner.name]
            for _, owner in self.current_type.all_attributes()
        ]

        attrs = []
        visited = set()
        for ancestor in ancestors:
            if ancestor.id in visited:
                continue

            visited.add(ancestor.id)
            attrs += [
                feature
                for feature in ancestor.features
                if isinstance(feature, cool.AttrDeclarationNode)
            ]

        expressions: List[cool.ExprNode] = []
        for attr in attrs:
            expressions.append(self.visit(attr, scope))
        expressions.append(cool.VariableNode("self"))

        body = cool.BlockNode(expressions)
        constructor = cool.MethodDeclarationNode(
            "__init__", [], self.current_type.name, body
        )

        # Added the Type
        self.current_type.define_method("__init__", [], [], self.current_type)

        attr = [
            feature
            for feature in node.features
            if isinstance(feature, cool.AttrDeclarationNode)
        ]
        methods = [
            feature
            for feature in node.features
            if isinstance(feature, cool.MethodDeclarationNode)
        ]
        features = attrs + [constructor] + methods

        return cool.ClassDeclarationNode(node.id, features, node.parent)

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        if node.expr is None:
            expr = None
            if node.type == "Int":
                expr = cool.IntegerNode("0")
            elif node.type == "Bool":
                expr = cool.BooleanNode("false")
            elif node.type == "String":
                expr = cool.StringNode('""')
            else:
                expr = (
                    icool.VoidNode()
                )  # cool.WhileNode(cool.BooleanNode("false"), cool.IntegerNode("0"))

            return cool.AssignNode(node.id, expr)

        return cool.AssignNode(node.id, node.expr)


# Notes:
# 1 - All the expression nodes are going to return a tuple [str, Type]


class CoolToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on("node")
    def visit(self, node, scope):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope):
        for declaration in node.declarations:
            self.visit(declaration, scope)

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(cool.ClassDeclarationNode)
    def visit(self, node: cool.ClassDeclarationNode, scope: Scope):
        self.current_type = self.context.get_type(node.id)

        type_node = self.register_type(self.current_type.name)

        methods = [
            feature
            for feature in node.features
            if isinstance(feature, cool.MethodDeclarationNode)
        ]

        for attr, _ in self.current_type.all_attributes():
            self.visit(attr, scope)
            type_node.attributes.append(attr.name)

        visited = set()
        for method, _ in self.current_type.all_methods():

            if method.name in visited:
                continue

            visited.add(method.name)
            _, ancestor = self.current_type.get_method(method.name, get_owner=True)

            type_node.methods.append(
                (method.name, self.to_function_name(method.name, ancestor.name))
            )

        for method, child_scope in zip(methods, scope.children):
            self.visit(method, child_scope)

    @visitor.when(cool.AttrDeclarationNode)
    def visit(self, node: cool.AttrDeclarationNode, scope: Scope):
        pass

    @visitor.when(cool.MethodDeclarationNode)
    def visit(self, node: cool.MethodDeclarationNode, scope: Scope):
        self.current_method, owner_type = self.current_type.get_method(
            node.id, get_owner=True
        )
        function_name = self.to_function_name(self.current_method.name, owner_type.name)
        self.current_function = self.register_function(function_name)

        self.current_function.params = [cil.ParamNode("self")] + [
            cil.ParamNode(param_name) for param_name, _ in node.params
        ]

        self.visit(node.body, scope)

    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        i = 0
        for name, _, expr in node.declarations:
            self.register_local(name)

            if expr:
                source, _ = self.visit(expr, scope.children[i])
                if source:
                    self.register_instruction(cil.AssignNode(name, source))
                i += 1

        self.register_instruction(cil.ReturnNode(0))

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        child_scope = scope.create_child()
        return_type = ErrorType()
        for expr in node.expressions:
            return_type = self.visit(expr, child_scope)
        return return_type

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        obj_source, obj_type = self.visit(node.obj, scope)

        args_sources = []
        for arg in node.args:
            arg_source, _ = self.visit(arg, scope)
            args_sources.append(arg_source)

        self.register_instruction(cil.ArgNode(obj_source))
        for arg_source in args_sources:
            self.register_instruction(cil.ArgNode(arg_source))

        call_dest = self.define_internal_local()
        method = obj_type.get_method(node.id)
        self.register_instruction(
            cil.DynamicCallNode(
                obj_type.name, self.to_function_name(node.id, obj_type.name), call_dest
            )
        )
        return call_dest, method.return_type

    @visitor.when(cool.IntegerNode)
    def visit(self, node: cool.IntegerNode, scope: Scope):
        return node.lex, self.context.get_type("Int")

    
    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        return node.lex, self.context.get_type("String")
    
    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        return node.lex, self.context.get_type("Bool")

    @visitor.when(cool.InstantiateNode)
    def visit(self, node: cool.InstantiateNode, scope: Scope):
        local = self.define_internal_local()
        self.instructions.append(cil.AllocateNode(node.lex, local))
        return local, self.context.get_type(node.lex)
