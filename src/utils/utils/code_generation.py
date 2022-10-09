from . import ast_nodes as cool
from .semantic import *
from . import visitor
from typing import Any, Dict, List, Optional, Tuple
from copy import deepcopy

# creación del átomo y tipo que representará el NULL
 
class NullNode(cool.AtomicNode):
    def __init__(self):
        super().__init__("NULL")

class NullType(Type):
    def __init__(self):
        super().__init__("null")

    def conforms_to(self, other):
        return True

    def bypass(self):
        return True

    def __str__(self):
        return self.name


class COOLwithNULL:
    
    def __init__(self, context: Context):
        self.current_method = None
        self.current_type = None
        self.context: Context = context
        self.class_declarations = {}  # tDict[str, cool.ClassDecNode]

    @visitor.on("node")
    def visit(self, node):
        pass

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode):
        # list de ClassDecNode
        newclassdec = []

        for type_ in ["Object", "IO",  "String", "Int", "Bool"]:
            t = self.context.get_type(type_)
            t.define_method("__init__", [], [], t)
            t.methods.move_to_end("__init__", last=False)

        for class_dec in node.class_list:
            self.class_declarations[class_dec.name] = class_dec

        for class_dec in node.class_list:
            newclassdec.append(self.visit(class_dec))

        return cool.ProgramNode(newclassdec)

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode):
        self.current_type = self.context.get_type(node.name)

        parents = [
            self.class_declarations[owner.name] for _, owner in self.current_type.all_attributes()
        ]

        attrs, visited = [], set()
        
        for parent in parents:
            if parent.name in visited:
                continue

            visited.add(parent.name)
            attrs += [
                feature for feature in parent.data if isinstance(feature, cool.AttributeDecNode)
                ]

        expressions: List[cool.ExprNode] = []
        for attr in attrs:
            expressions.append(self.visit(attr))
        expressions.append(cool.VariableNode("self"))

        body = cool.BlockNode(expressions)
        constructor = cool.MethodDecNode(
            "__init__", [], self.current_type.name, body
        )

        self.current_type.define_method("__init__", [], [], self.current_type)
        self.current_type.methods.move_to_end("__init__", last=False)

        attrs = [
            attrib
            for attrib in node.data
            if isinstance(attrib, cool.AttributeDecNode)
        ]
        methods = [
            meth
            for meth in node.data
            if isinstance(meth, cool.MethodDecNode)
        ]

        features = attrs + [constructor] + methods

        return cool.ClassDecNode(node.name, features, node.parent)

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode):
        if node.expr is None:
            expr = None
            if node._type == "Int":
                expr = cool.IntegerNode("0")
            elif node._type == "Bool":
                expr = cool.BooleanNode("false")
            elif node._type == "String":
                expr = cool.StringNode('""')
            else:
                expr = NullNode()
            return cool.AssignNode(node.name, expr)
        return cool.AssignNode(node.name, deepcopy(node.expr))

