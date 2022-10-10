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
        
        # Dict[str, cool.ClassDecNode]
        self.class_declarations = {}  

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

        parents = [self.class_declarations[owner.name] for _, owner in self.current_type.all_attributes()]

        attrs, visited = [], set()
        
        for parent in parents:
            if parent.name in visited:
                continue

            visited.add(parent.name)
            attrs += [feature for feature in parent.data if isinstance(feature, cool.AttributeDecNode)]

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

class COOLwithNULL_Type:
    def __init__(self, context: Context, errors: List[str], program: str):
        self.context: Context = context
        self.errors = errors
        self.current_type = None
        self.current_method = None
        self.current_attribute = None
        self.program = program

    def get_tokencolumn(self, str, pos):
        column = 1
        temp_pos = pos
        while str[temp_pos] != '\n':
            if temp_pos == 0: break
            temp_pos -= 1
            column += 1
        return column if column > 1 else 2

    @visitor.on("node")
    def visit(self, node, scope):
        pass

    #############
    # main flow #
    #############

    @visitor.when(cool.ProgramNode)
    def visit(self, node: cool.ProgramNode, scope: Scope=None):
        if scope is None:
            scope = Scope()
        node.scope = scope

        for item in node.class_list:
            self.visit(item, scope.create_child())
        return scope

    @visitor.when(cool.ClassDecNode)
    def visit(self, node: cool.ClassDecNode, scope: Scope):
        node.scope = scope
        self.current_type = self.context.get_type(node.name)

        attrs = [ att for att in node.data if isinstance(att, cool.AttributeDecNode)]   
        methods = [ meth for meth in node.data if isinstance(meth, cool.MethodDecNode)]

        for attr, attr_owner in self.current_type.all_attributes():
            if attr_owner != self.current_type:
                scope.define_variable(attr.name, attr.type)

        for attr in attrs:
            self.visit(attr, scope)

        for method in methods:
            self.visit(method, scope.create_child())

    @visitor.when(cool.AttributeDecNode)
    def visit(self, node: cool.AttributeDecNode, scope: Scope):
        node.scope = scope
        if node.name == "self":
            self.errors.append(f'({node.line}, {self.get_tokencolumn(self.program, node.lexpos)}) - SemanticError: Cannot set "self" as attribute of a class.')

        try:
            attr_type = (self.context.get_type(node._type) if node._type != "SELF_TYPE" else self.current_type)
        except SemanticError:
            attr_type = ErrorType()

        scope.define_variable("self", self.current_type)

        self.current_attribute = self.current_type.get_attribute(node.name)
        self.current_method = None

        if node.expr is not None:
            expr_type = self.visit(node.expr, scope.create_child())
            if not expr_type.conforms_to(attr_type):
                line, lexpos = node.expr_pos
                self.errors.append(f'({line}, {self.get_tokencolumn(self.program, lexpos)}) - TypeError: Cannot convert "{expr_type.name}" into "{attr_type.name}".')
        scope.define_variable(node.name, attr_type)

    @visitor.when(cool.MethodDecNode)
    def visit(self, node: cool.MethodDecNode, scope: Scope):
        pass
    
    ###############
    # expressions #
    ###############
    
    @visitor.when(cool.LetNode)
    def visit(self, node: cool.LetNode, scope: Scope):
        pass

    @visitor.when(cool.AssignNode)
    def visit(self, node: cool.AssignNode, scope: Scope):
        pass

    @visitor.when(cool.BlockNode)
    def visit(self, node: cool.BlockNode, scope: Scope):
        pass

    @visitor.when(cool.ConditionalNode)
    def visit(self, node: cool.ConditionalNode, scope: Scope):
        pass

    @visitor.when(cool.WhileNode)
    def visit(self, node: cool.WhileNode, scope: Scope):
        pass

    @visitor.when(cool.CaseNode)
    def visit(self, node: cool.CaseNode, scope: Scope):
        pass

    @visitor.when(cool.MethodCallNode)
    def visit(self, node: cool.MethodCallNode, scope: Scope):
        pass
    

    @visitor.when(cool.VariableNode)
    def visit(self, node: cool.VariableNode, scope: Scope):
        pass

    @visitor.when(cool.NewNode)
    def visit(self, node: cool.NewNode, scope: Scope):
        pass
    
    @visitor.when(cool.IsVoidNode)
    def visit(self, node: cool.IsVoidNode, scope: Scope):
       pass
    
    ####################
    # unary operations #
    ####################

    @visitor.when(cool.NegationNode)
    def visit(self, node: cool.NegationNode, scope: Scope):
        pass

    @visitor.when(cool.ComplementNode)
    def visit(self, node: cool.ComplementNode, scope: Scope):
        pass


    #####################
    # binary operations #
    #####################
    
    @visitor.when(cool.PlusNode)
    def visit(self, node: cool.PlusNode, scope: Scope):
        pass

    @visitor.when(cool.MinusNode)
    def visit(self, node: cool.MinusNode, scope: Scope):
        pass

    @visitor.when(cool.TimesNode)
    def visit(self, node: cool.TimesNode, scope: Scope):
        pass

    @visitor.when(cool.DivNode)
    def visit(self, node: cool.DivNode, scope: Scope):
        pass

    @visitor.when(cool.LessEqualNode)
    def visit(self, node: cool.LessEqualNode, scope: Scope):
        pass

    @visitor.when(cool.LessNode)
    def visit(self, node: cool.LessNode, scope: Scope):
        pass

    @visitor.when(cool.EqualNode)
    def visit(self, node: cool.EqualNode, scope: Scope):
        pass
    
    
    ##############
    # atomic exp #
    ##############
    
    @visitor.when(cool.NumberNode)
    def visit(self, node: cool.NumberNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Int")

    @visitor.when(cool.StringNode)
    def visit(self, node: cool.StringNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("String")

    @visitor.when(cool.BooleanNode)
    def visit(self, node: cool.BooleanNode, scope: Scope):
        node.scope = scope
        return self.context.get_type("Bool")

    @visitor.when(NullNode)
    def visit(self, node: NullNode, scope: Scope):
        node.scope = scope
        return NullType()


