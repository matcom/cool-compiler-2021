from __future__ import annotations

from coolcmp.codegen.cool2cil import CILVisitor
from coolcmp.utils import ast, cil, visitor
from coolcmp.utils.semantic import Scope


class DotCodeVisitor(CILVisitor):
    """
    Builds the .CODE section.
    """
    def __init__(self, cil_root: cil.ProgramNode):
        super().__init__()
        self.root = cil_root
        self.code = cil_root.dot_code
        self.current_function: cil.FunctionNode | None = None
        self.current_type: str | None = None

    def add_function(self, name: str = None):
        if name is None:
            name = f'f{self.next_function_id}'
        self.current_function = cil.FunctionNode(name, [], [], [])
        self.code.append(self.current_function)

    def add_param(self, name: str) -> str:
        param = cil.ParamNode(name)
        self.current_function.params.append(param)
        return name

    def add_local(self, name: str, internal: bool = True) -> str:
        if internal:
            name = f'_{name}_{len(self.current_function.local_vars)}'
        local = cil.LocalNode(name)
        self.current_function.local_vars.append(local)
        return name

    def add_inst(self, inst: cil.InstructionNode) -> cil.InstructionNode:
        self.current_function.instructions.append(inst)
        return inst

    @visitor.on('node')
    def visit(self, node: ast.Node, scope: Scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        # build the entry function:
        for class_ in node.declarations:
            if class_.id == 'Main':
                for feature in class_.features:
                    if isinstance(feature, ast.FuncDeclarationNode) and feature.id == 'main':
                        self.add_function('entry')
                        main_scope = scope.get_tagged_scope('Main')
                        instance = self.add_local('instance')
                        self.add_inst(cil.AllocateNode('Main', instance))
                        for attr in (f for f in class_.features if isinstance(f, ast.AttrDeclarationNode)):
                            if attr.expr is not None:
                                expr_dest = self.visit(attr.expr, main_scope)
                                self.add_inst(cil.SetAttrNode(instance, f'Main_{attr.id}', expr_dest))
                        result = self.add_local('result')
                        self.add_inst(cil.ArgNode(instance))
                        self.add_inst(cil.DynamicCallNode('Main', 'Main_main', result))
                        self.add_inst(cil.ReturnNode(0))
                        break

        # build the code functions
        for class_ in node.declarations:
            self.visit(class_, scope.get_tagged_scope(class_.id))

        # add the default functions of COOL
        # TODO: add missing instructions
        self.code += [
            # cil.FunctionNode('abort', [], [], []),
            # cil.FunctionNode('type_name', [], [], []),
            # cil.FunctionNode('copy', [], [], []),
            # cil.FunctionNode('out_string', [], [], []),
            cil.FunctionNode(
                name='out_string',
                params=[
                    cil.ParamNode('str_addr')
                ],
                local_vars=[],
                instructions=[
                    cil.PrintNode('str_addr'),
                    cil.ReturnNode(0),
                ]
            ),
            # cil.FunctionNode('out_int', [], [], []),
            # cil.FunctionNode('in_int', [], [], []),
        ]

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode, scope: Scope):
        self.current_type = node.id
        methods = (f for f in node.features if isinstance(f, ast.FuncDeclarationNode))
        for method in methods:
            self.visit(method, scope.get_tagged_scope(method.id))

    @visitor.when(ast.FuncDeclarationNode)
    def visit(self, node: ast.FuncDeclarationNode, scope: Scope):
        self.add_function()

        for local in scope.all_locals():
            if local.is_param:
                self.add_param(local.name)
            else:
                local_name = self.add_local(local.name, internal=False)
                if local.is_attr:
                    attr_name = f'{self.current_type}_{local.name}'
                    self.add_inst(cil.GetAttrNode(local_name, 'self', attr_name))

        result = self.visit(node.body, scope)
        self.add_inst(cil.ReturnNode(result))

    @visitor.when(ast.CallNode)
    def visit(self, node: ast.CallNode, scope: Scope):
        # allocate and push the object type
        if node.obj is None:
            obj = ast.VariableNode('self')
        else:
            obj = node.obj
        obj_dest = self.visit(obj, scope)
        internal = self.add_local('internal')
        self.add_inst(cil.TypeOfNode(obj_dest, internal))
        self.add_inst(cil.ArgNode(internal))

        # allocate and push the args
        for arg in node.args:
            arg_dest = self.visit(arg, scope)
            self.add_inst(cil.ArgNode(arg_dest))

        # call the function
        result = self.add_local('result')
        self.add_inst(cil.DynamicCallNode(internal, node.id, result))

        return result

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, scope: Scope):
        return node.lex

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        dest = self.add_local('internal')
        self.add_inst(cil.LoadNode(dest, self.root.get_data_name(node.lex)))
        return dest

    @visitor.when(ast.InstantiateNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        instance = self.add_local('instance')
        self.add_inst(cil.AllocateNode(node.lex, instance))
        type_node = self.root.get_type(node.lex)
        for attr in type_node.attributes:
            attr_expr = type_node.get_attr_node(attr)
            if attr_expr is not None:
                attr_dest = self.visit(attr_expr, scope)
                self.add_inst(cil.SetAttrNode(instance, attr, attr_dest))
        return instance
