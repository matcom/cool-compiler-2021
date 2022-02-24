from __future__ import annotations
from copy import deepcopy

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
        self.label_count = -1

    def new_label(self, name: str) -> cil.LabelNode:
        self.label_count += 1
        name = f'_{name}_{self.label_count}'
        return cil.LabelNode(name)

    def add_function(self, name: str):
        # if name is None:
        #     name = f'f{self.next_function_id}'
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

    def add_comment(self, text: str):
        self.add_inst(cil.CommentNode(text))

    @visitor.on('node')
    def visit(self, node: ast.Node, scope: Scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        # the root scope stores void to avoid semantic errors initializing
        # the void attribute of classes to void. After that every function
        # has access to void through that attribute in every class.
        # So, pop it to avoid repeated locals.
        scope.locals.pop(0)

        # build the entry function:
        for class_ in node.declarations:
            if class_.id == 'Main':
                for feature in class_.features:
                    if isinstance(feature, ast.FuncDeclarationNode) and feature.id == 'main':
                        self.add_function('main')
                        # void = self.add_local('void', internal=False)
                        # self.add_inst(cil.AllocateNode('<void>', void))
                        void_dest = self.visit(ast.InstantiateNode('Void'), scope)
                        void = self.add_local('void', internal=False)
                        self.add_inst(cil.AssignNode(void, void_dest))
                        main_scope = deepcopy(scope.get_tagged_scope('Main'))
                        instance = self.visit(ast.InstantiateNode('Main'), main_scope)
                        self.add_comment('Calling main')
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
            cil.FunctionNode(
                name='Object_abort',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[],
                instructions=[
                    cil.ReturnNode(),
                ]
            ),
            # cil.FunctionNode(
            #     name='type_name',
            #     params=[
            #         cil.ParamNode('self'),
            #     ],
            #     local_vars=[
            #         cil.LocalNode('name'),
            #     ],
            #     instructions=[
            #         cil.LoadNode('name', )
            #         cil.ReturnNode(),
            #     ]
            # ),
            cil.FunctionNode(
                name='IO_out_string',
                params=[
                    cil.ParamNode('self'),
                    cil.ParamNode('str_addr'),
                ],
                local_vars=[],
                instructions=[
                    cil.PrintStringNode('str_addr'),
                    cil.ReturnNode(),
                ]
            ),
            cil.FunctionNode(
                name='IO_out_int',
                params=[
                    cil.ParamNode('self'),
                    cil.ParamNode('int_addr'),
                ],
                local_vars=[],
                instructions=[
                    cil.PrintIntNode('int_addr'),
                    cil.ReturnNode(),
                ]
            ),
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
        self.add_function(f'{self.current_type}_{node.id}')

        local_name = self.add_local(f'_name', internal=False)
        self.add_inst(cil.GetAttrNode(local_name, 'self', f'{self.current_type}__name'))
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

    @visitor.when(ast.LetDeclarationNode)
    def visit(self, node: ast.LetDeclarationNode, scope: Scope):
        local = self.add_local(node.id, internal=False)
        if node.expr is not None:
            expr_dest = self.visit(node.expr, scope)
            self.add_inst(cil.AssignNode(local, expr_dest))

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        scope = scope.children.pop(0)
        for let_declaration in node.declarations:
            self.visit(let_declaration, scope)

        return self.visit(node.expr, scope)

    @visitor.when(ast.ParenthesisExpr)
    def visit(self, node: ast.ParenthesisExpr, scope: Scope):
        return self.visit(node, scope)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        scope = scope.children.pop(0)
        last_expr = None
        for expr in node.expressions:
            last_expr = self.visit(expr, scope)

        return last_expr

    @visitor.when(ast.CaseBranchNode)
    def visit(self, node: ast.CaseBranchNode, scope: Scope):
        pass

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, scope: Scope):
        pass

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        expr_dest = self.visit(node.expr, scope)
        self.add_inst(cil.AssignNode(node.id, expr_dest))
        return expr_dest

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        """
        Note that the 'else' branch comes before the 'then' branch.

        <local vars>
        if_dest = <if_expr>
        IF if_dest GOTO then
        else_dest = <else_expr>
        cond_res = else_dest
        GOTO endif
        LABEL then
        then_dest = <then_expr>
        cond_res = then_dest
        LABEL endif
        """
        self.add_comment('Conditional if-else')

        then_label = self.new_label('then')
        endif_label = self.new_label('endif')

        cond_res = self.add_local('cond_res')
        if_dest = self.visit(node.if_expr, scope)
        self.add_inst(cil.GotoIfNode(if_dest, then_label.name))
        else_dest = self.visit(node.else_expr, scope.children[1])
        self.add_inst(cil.AssignNode(cond_res, else_dest))
        self.add_inst(cil.GotoNode(endif_label.name))
        self.add_inst(then_label)
        then_dest = self.visit(node.then_expr, scope.children[0])
        self.add_inst(cil.AssignNode(cond_res, then_dest))
        self.add_inst(endif_label)
        return cond_res

    @visitor.when(ast.WhileNode)
    def visit(self, node: ast.WhileNode, scope: Scope):
        """
        <local vars>
        LABEL while_cond
        cond_dest = <cond_expr>
        IF cond_dest GOTO while_body
        GOTO end_while
        LABEL while_body
        <body_expr>     <----- the body return is not used, just side effects
        GOTO while_cond
        LABEL end_while

        void_res = VCALL Object get_void
        """
        self.add_comment('While loop')

        cond_label = self.new_label('while_cond')
        body_label = self.new_label('while_body')
        end_while_label = self.new_label('end_while')

        self.add_inst(cond_label)
        cond_dest = self.visit(node.condition, scope)
        self.add_inst(cil.GotoIfNode(cond_dest, body_label.name))
        self.add_inst(cil.GotoNode(end_while_label.name))
        self.add_inst(body_label)
        self.visit(node.body, scope)
        self.add_inst(cil.GotoNode(cond_label.name))
        self.add_inst(end_while_label)

        return 'void'

    @visitor.when(ast.CallNode)
    def visit(self, node: ast.CallNode, scope: Scope):
        self.add_comment(f'Calling function {node.id}')
        # allocate and push the object
        if node.obj is None:
            obj = ast.VariableNode('self')
        else:
            obj = node.obj
        obj_dest = self.visit(obj, scope)
        inst_type = self.add_local('inst_type')
        self.add_inst(cil.TypeOfNode(obj_dest, inst_type))
        self.add_inst(cil.ArgNode(obj_dest))

        # allocate and push the args
        for arg in node.args:
            arg_dest = self.visit(arg, scope)
            self.add_inst(cil.ArgNode(arg_dest))

        # call the function
        call_res = self.add_local('call_res')
        self.add_inst(cil.DynamicCallNode(inst_type, node.id, call_res))

        return call_res

    @visitor.when(ast.InstantiateNode)
    def visit(self, node: ast.InstantiateNode, scope: Scope):
        self.add_comment(f'Instantiating type {node.lex}')

        instance = self.add_local('instance')
        self.add_inst(cil.AllocateNode(node.lex, instance))
        type_node = self.root.get_type(node.lex)
        for attr in type_node.attributes:
            attr_expr = type_node.get_attr_node(attr)
            attr_dest = self.visit(attr_expr, scope)
            self.add_inst(cil.SetAttrNode(instance, attr, attr_dest))
        return instance

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        self.add_comment(
            'Instantiating string: ' +
            (node.lex if len(node.lex) < 20 else node.lex[:15] + '...')
        )

        str_instance = self.add_local('str_instance')
        self.add_inst(cil.AllocateNode('String', str_instance))
        type_node = self.root.get_type('String')
        for attr in type_node.attributes:
            attr_dest = self.visit(node.lex, scope)
            self.add_inst(cil.SetAttrNode(str_instance, attr, attr_dest))
        return str_instance

    @visitor.when(ast.IntegerNode)
    def visit(self, node: ast.IntegerNode, scope: Scope):
        int_instance = self.add_local('int_instance')
        self.add_inst(cil.AllocateNode('Int', int_instance))
        type_node = self.root.get_type('Int')
        for attr in type_node.attributes:
            attr_dest = self.visit(int(node.lex), scope)
            self.add_inst(cil.SetAttrNode(int_instance, attr, attr_dest))
        return int_instance

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        bool_instance = self.add_local('bool_instance')
        self.add_inst(cil.AllocateNode('Bool', bool_instance))
        type_node = self.root.get_type('Bool')
        for attr in type_node.attributes:
            attr_dest = self.visit(node.lex == 'true', scope)
            self.add_inst(cil.SetAttrNode(bool_instance, attr, attr_dest))
        return bool_instance

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, _):
        return node.lex

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        return self.build_arithmetic_node(cil.PlusNode, node, scope)

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        return self.build_arithmetic_node(cil.MinusNode, node, scope)

    @visitor.when(ast.StarNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        return self.build_arithmetic_node(cil.StarNode, node, scope)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        return self.build_arithmetic_node(cil.DivNode, node, scope)

    @visitor.when(ast.LessThanNode)
    def visit(self, node: ast.LessThanNode, scope: Scope):
        return self.build_arithmetic_node(cil.MinusNode, node, scope)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        return self.build_arithmetic_node(cil.MinusNode, node, scope)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        if isinstance(node.left, ast.IntegerNode) and isinstance(node.right, ast.IntegerNode):
            return self.build_arithmetic_node(cil.MinusNode, node, scope)
        else:
            left_dest = self.visit(node.left, scope)
            right_dest = self.visit(node.right, scope)
            left_type = self.add_local('left_type')
            right_type = self.add_local('right_type')
            self.add_inst(cil.TypeOfNode(left_dest, left_type))
            self.add_inst(cil.TypeOfNode(right_dest, right_type))
            comp_res = self.add_local('comp_res')
            self.add_inst(cil.CompareNode(comp_res, left_type, right_type))
            return comp_res

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, scope: Scope):
        expr_dest = self.visit(node.expr, scope)
        type_expr = self.add_local('expr_type')
        self.add_inst(cil.TypeOfNode(expr_dest, type_expr))
        comp_res = self.add_local('comp_res')
        self.add_inst(cil.CompareNode(comp_res, type_expr, 'Void'))
        return comp_res

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode, scope: Scope):
        neg_res = self.add_local('neg_res')
        expr_res = self.visit(node.expr, scope)
        self.add_inst(cil.NegationNode(neg_res, expr_res))
        return neg_res

    @visitor.when(ast.ComplementNode)
    def visit(self, node: ast.ComplementNode, scope: Scope):
        com_res = self.add_local('com_res')
        expr_res = self.visit(node.expr, scope)
        self.add_inst(cil.ComplementNode(com_res, expr_res))
        return com_res

    @visitor.when(str)
    def visit(self, lex: str, _):
        str_dest = self.add_local('str_dest')
        self.add_inst(cil.LoadNode(str_dest, self.root.get_data_name(lex)))
        return str_dest

    @visitor.when(bool)
    def visit(self, bool_value: bool, _):
        return int(bool_value)

    @visitor.when(int)
    def visit(self, value: int, _):
        return value

    def build_arithmetic_node(self, new_node_cls, node: ast.BinaryNode, scope: Scope):
        left_dest = self.visit(node.left, scope)
        right_dest = self.visit(node.right, scope)
        oper_dest = self.add_local('oper_dest')
        self.add_inst(new_node_cls(oper_dest, left_dest, right_dest))
        return oper_dest
