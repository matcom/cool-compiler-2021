from __future__ import annotations
from copy import deepcopy
from typing import List, Tuple

from coolcmp.utils import ast, cil, visitor, extract_feat_name
from coolcmp.utils.semantic import Context, Scope


class DotCodeVisitor:
    """
    Builds the .CODE section.
    """
    def __init__(self, cil_root: cil.ProgramNode, context: Context):
        super().__init__()
        self.root = cil_root
        self.code = cil_root.dot_code
        self.current_function: cil.FunctionNode | None = None
        self.current_type: str | None = None
        self.current_init: cil.FunctionNode | None = None
        self.label_count = -1
        self.context = context

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

    @property
    def current_is_init(self):
        return self.current_function.name == self.current_init.name

    @visitor.on('node')
    def visit(self, node: ast.Node, scope: Scope):
        raise NotImplementedError()

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope: Scope):
        # the root scope stores void to avoid semantic errors initializing
        # the void attribute of classes to void. After that every function
        # has access to void through that attribute in every class.
        # So, pop it to avoid repeated locals.
        scope.locals.pop(0)
        print(scope)
        # build the code functions
        for class_ in node.declarations:
            print('_' * 10, 'in classes')
            tagged_scope = scope.get_tagged_scope(class_.id)
            print(f'visiting class {class_.id}')
            print(f'with scope {tagged_scope.tag} and childrens {[c.tag for c in tagged_scope.children]}')
            # print(deepcopy(scope.get_tagged_scope(class_.id)))
            print('_' * 10)

            self.visit(class_, deepcopy(tagged_scope))

            # build the entry function:
            for class_ in node.declarations:
                if class_.id == 'Main':
                    for feature in class_.features:
                        if isinstance(feature, ast.FuncDeclarationNode) and feature.id == 'main':
                            self.add_function('main')
                            instance = self.add_local('main_instance')
                            self.add_inst(cil.StaticCallNode('Main__init', instance))
                            self.add_comment('Calling main')
                            result = self.add_local('result')
                            self.add_inst(cil.ArgNode(instance))
                            self.add_inst(cil.DynamicCallNode(instance, 'main', result, None, 'Main'))
                            self.add_inst(cil.ReturnNode(0))
                            break

        # add the default functions of COOL
        # TODO: add missing instructions
        self.code += [
            cil.FunctionNode(
                name='Object__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'Object'),
                    cil.ReturnNode('self')
                ]
            ),
            cil.FunctionNode(
                name='Object_abort',
                params=[
                    cil.ParamNode('self'),
                    cil.ParamNode('typename')
                ],
                local_vars=[],
                instructions=[
                    cil.AbortNode(),
                    cil.ReturnNode(),
                ]
            ),
            cil.FunctionNode(
                name='Object_type_name',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[
                    cil.LocalNode('name'),
                ],
                instructions=[
                    cil.TypeNameNode('name', 'self'),
                    cil.ReturnNode('name'),
                ]
            ),
            cil.FunctionNode(
                name='Object_copy',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[
                    cil.LocalNode('self_copy'),
                ],
                instructions=[
                    cil.AssignNode('self_copy', 'self'),
                    cil.ReturnNode('self_copy'),
                ]
            ),
            cil.FunctionNode(
                name='IO__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'IO'),
                    cil.ReturnNode('self'),
                ]
            ),
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
            cil.FunctionNode(
                name='IO_in_string',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[
                    cil.LocalNode('_in_string'),
                ],
                instructions=[
                    cil.ReadStringNode('_in_string'),
                    cil.ReturnNode('_in_string'),
                ]
            ),
            cil.FunctionNode(
                name='IO_in_int',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[
                    cil.LocalNode('_in_int'),
                ],
                instructions=[
                    cil.ReadIntNode('_in_int'),
                    cil.ReturnNode('_in_int'),
                ]
            ),
            cil.FunctionNode(
                name='String__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'String'),
                    cil.ReturnNode('self'),
                ]
            ),
            cil.FunctionNode(
                name='String_length',
                params=[
                    cil.ParamNode('self'),
                ],
                local_vars=[
                    cil.LocalNode('_length'),
                ],
                instructions=[
                    cil.LengthNode('self', '_length'),
                    cil.ReturnNode('_length'),
                ]
            ),
            cil.FunctionNode(
                name='String_concat',
                params=[
                    cil.ParamNode('self'),
                    cil.ParamNode('other_str'),
                ],
                local_vars=[
                    cil.LocalNode('result'),
                ],
                instructions=[
                    cil.ConcatNode('result', 'self', 'other_str'),
                    cil.ReturnNode('result'),
                ]
            ),
            cil.FunctionNode(
                name='String_substr',
                params=[
                    cil.ParamNode('self'),
                    cil.ParamNode('index'),
                    cil.ParamNode('length'),
                ],
                local_vars=[
                    cil.LocalNode('result'),
                ],
                instructions=[
                    cil.SubstringNode('result', 'value', 'index', 'length'),
                    cil.ReturnNode('result'),
                ]
            ),
            cil.FunctionNode(
                name='Bool__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'Bool'),
                    cil.ReturnNode('self'),
                ]
            ),
            cil.FunctionNode(
                name='Int__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'Int'),
                    cil.ReturnNode('self'),
                ]
            ),
            cil.FunctionNode(
                name='Void__init',
                params=[],
                local_vars=[
                    cil.LocalNode('self'),
                ],
                instructions=[
                    cil.InitNode('self', 'Void'),
                    cil.ReturnNode('self'),
                ]
            ),
        ]

    @visitor.when(ast.ClassDeclarationNode)
    def visit(self, node: ast.ClassDeclarationNode, scope: Scope):
        self.current_type = node.id
        init = cil.FunctionNode(
            name=f'{node.id}__init',
            params=[],
            local_vars=[
                cil.LocalNode('self'),
            ],
            instructions=[
                cil.InitNode('self', node.id),
            ]
        )
        self.root.dot_code.append(init)
        self.current_init = init

        self.current_function = self.current_init
        type_node = self.root.get_type(self.current_type)
        for attr_name in type_node.attributes:
            attr = self.add_local(extract_feat_name(attr_name), internal=False)
            attr_expr, attr_scope = type_node.get_attr_node(attr_name)
            attr_value = self.visit(attr_expr, attr_scope)
            attr_index = type_node.attributes.index(attr_name)
            attr_at = cil.AttributeAt(attr_name, attr_index)
            self.add_inst(cil.SetAttrNode('self', attr_at, attr_value))
            self.add_inst(cil.AssignNode(attr, attr_value))

        for feat in node.features:
            # if isinstance(feat, ast.AttrDeclarationNode):
            #     visited_attrs.append(feat.id)
            #     self.visit(feat, scope)
            if isinstance(feat, ast.FuncDeclarationNode):
                print('_' * 10, 'in feats', f'{node.id}: {feat.id}')
                tagged_scope = scope.get_tagged_scope(feat.id)
                print(f'visiting method "{feat.id}" from scope "{scope.tag}"')
                print(f'with child scope "{tagged_scope.tag}" and childrens {[c.tag for c in tagged_scope.children]}')
                # print(deepcopy(scope.get_tagged_scope(feat.id)))
                print('_' * 10)
                self.visit(feat, tagged_scope)

        init.instructions.append(cil.ReturnNode('self'))

    # @visitor.when(ast.AttrDeclarationNode)
    # def visit(self, node: ast.AttrDeclarationNode, scope: Scope):
    #     self.current_function = self.current_init
    #     attr = self.add_local(node.id, internal=False)
    #
    #     attr_index = self.root.get_type(self.current_type).attributes.index(f'{self.current_type}_{node.id}')
    #     if node.expr is not None:
    #         result = self.visit(node.expr, scope)
    #         self.add_inst(cil.SetAttrNode('self', cil.AttributeAt(attr, attr_index), result))
    #         self.add_inst(cil.AssignNode(attr, result))
    #     else:
    #         type_node = self.root.get_type(self.current_type)
    #         attr_expr = type_node.get_attr_node(node.id)
    #         attr_value = self.visit(attr_expr, scope)
    #         attr_index = type_node.attributes.index(node.id)
    #         attr_at = cil.AttributeAt(node.id, attr_index)
    #         self.add_inst(
    #             cil.SetAttrNode('self', attr_at, attr_value)
    #         )


    @visitor.when(ast.FuncDeclarationNode)
    def visit(self, node: ast.FuncDeclarationNode, scope: Scope):
        self.add_function(f'{self.current_type}_{node.id}')

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
            expr_node = node.expr
        elif node.type == 'String':
            expr_node = ast.StringNode('""')
        elif node.type == 'Bool':
            expr_node = ast.BooleanNode('false')
        elif node.type == 'Int':
            expr_node = ast.IntegerNode('0')
        else:
            expr_node = ast.VariableNode('void')
        expr_dest = self.visit(expr_node, scope)
        self.add_inst(cil.AssignNode(local, expr_dest))

    @visitor.when(ast.LetNode)
    def visit(self, node: ast.LetNode, scope: Scope):
        print('wtfffffffff!')
        let_scope = scope.children.pop(0)
        for let_declaration in node.declarations:
            self.visit(let_declaration, let_scope)

        return self.visit(node.expr, let_scope)

    @visitor.when(ast.ParenthesisExpr)
    def visit(self, node: ast.ParenthesisExpr, scope: Scope):
        return self.visit(node, scope)

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode, scope: Scope):
        last_expr = None
        for expr in node.expressions:
            last_expr = self.visit(expr, scope)

        return last_expr

    @visitor.when(ast.CaseBranchNode)
    def visit(self, node: ast.CaseBranchNode, scope: Scope):
        return self.visit(node.expr, scope)

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode, scope: Scope):
        self.add_comment("Case of")
        ret_exp = self.visit(node.expr, scope)
        typename = self.add_local('typename')
        case_ret = self.add_local('case_ret')
        end_label = self.new_label('end')
        case_match_re_label = self.new_label('case_match_re')
        expr_void_re_label = self.new_label('expr_void_re')

        self.add_inst(cil.TypeNameNode(typename, ret_exp))

        def get_depth(x: ast.CaseBranchNode):
            return self.context.type_depth(self.context.get_type(x.type))

        # Sort cases and scopes
        sorted_cases: List[Tuple[ast.CaseBranchNode, Scope]] = []
        for case in node.cases:
            child_scope = scope.children.pop(0)
            sorted_cases.append((case, child_scope))
        sorted_cases.sort(key=lambda x: get_depth(x[0]), reverse=True)

        branch_labels = [self.new_label('case_branch') for _ in sorted_cases]

        for (case, scope), label in zip(sorted_cases, branch_labels):
            self.add_comment(f"Check for case branch {case.type}")
            cond = self.add_local('case_cond')

            self.add_inst(cil.ConformsNode(cond, ret_exp, case.type))
            self.add_inst(cil.GotoIfNode(cond, label.name))

        # Does not conform to anyone => Runtime error
        self.add_inst(cil.GotoNode(case_match_re_label.name))

        for (case, child_scope), label in zip(sorted_cases, branch_labels):
            self.add_inst(label)
            idx = self.add_local(case.id, internal=False)
            self.add_inst(cil.AssignNode(idx, ret_exp))
            branch_ret = self.visit(case, child_scope)
            self.add_inst(cil.AssignNode(case_ret, branch_ret))
            self.add_inst(cil.GotoNode(end_label.name))

        # Handle Runtime Errors
        self.add_inst(case_match_re_label)
        self.add_inst(cil.CaseMatchRuntimeErrorNode())
        self.add_inst(expr_void_re_label)
        self.add_inst(cil.ExprVoidRuntimeErrorNode())

        self.add_inst(end_label)
        self.add_inst(cil.ReturnNode(ret_exp))
        return case_ret

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope: Scope):
        expr_dest = self.visit(node.expr, scope)
        self.add_inst(cil.AssignNode(node.id, expr_dest))
        variable = scope.find_variable(node.id)
        if variable.is_attr:
            attr_name = f'{self.current_type}_{node.id}'
            attr_index = self.root.get_type(self.current_type).attributes.index(attr_name)
            attr_at = cil.AttributeAt(attr_name, attr_index)
            self.add_inst(cil.SetAttrNode('self', attr_at, value=expr_dest))
        return expr_dest

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode, scope: Scope):
        """
        <local vars>
        if_dest = <if_expr>
        IF if_dest GOTO then
        GOTO else
        LABEL then
        then_dest = <then_expr>
        cond_res = then_dest
        GOTO endif
        LABEL else
        else_dest = <else_expr>
        cond_res = else_dest
        LABEL endif
        """
        self.add_comment('Conditional if-else')

        then_label = self.new_label('then')
        else_label = self.new_label('else')
        endif_label = self.new_label('endif')

        cond_res = self.add_local('cond_res')
        if_dest = self.visit(node.if_expr, scope)
        self.add_inst(cil.GotoIfNode(if_dest, then_label.name))
        self.add_inst(cil.GotoNode(else_label.name))
        self.add_inst(then_label)
        then_dest = self.visit(node.then_expr, scope)
        self.add_inst(cil.AssignNode(cond_res, then_dest))
        self.add_inst(cil.GotoNode(endif_label.name))
        self.add_inst(else_label)
        else_dest = self.visit(node.else_expr, scope)
        self.add_inst(cil.AssignNode(cond_res, else_dest))
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

        void_res = VCALL Object Void
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

        # allocate and push the args
        for arg in reversed(node.args):
            arg_dest = self.visit(arg, scope)
            self.add_inst(cil.ArgNode(arg_dest))
        self.add_inst(cil.ArgNode(obj_dest))

        # call the function
        call_res = self.add_local('call_res')
        self.add_inst(
            cil.DynamicCallNode(obj_dest, node.id, call_res, node.type, node.obj_dyn_type)
        )

        return call_res

    @visitor.when(ast.InstantiateNode)
    def visit(self, node: ast.InstantiateNode, scope: Scope):
        if node.lex == 'String':
            return self.visit(ast.StringNode('""'), scope)
        elif node.lex == 'Bool':
            return self.visit(ast.BooleanNode('false'), scope)
        elif node.lex == 'Int':
            return self.visit(ast.IntegerNode('0'), scope)

        self.add_comment(f'Instantiating type {node.lex}')

        # type_node = self.root.get_type(node.lex)
        # attr_values = []
        # for attr in type_node.attributes:
        #     attr_expr = type_node.get_attr_node(attr)
        #     attr_values.append(self.visit(attr_expr, scope))
        instance = self.add_local(f'inst_of_{node.lex}')
        self.add_inst(cil.StaticCallNode(f'{node.lex}__init', instance))
        # for attr, attr_value in zip(type_node.attributes, attr_values):
        #     attr_index = type_node.attributes.index(attr)
        #     attr_at = cil.AttributeAt(attr, attr_index)
        #     self.add_inst(
        #         cil.SetAttrNode(instance, attr_at, attr_value)
        #     )
        return instance

    @visitor.when(ast.StringNode)
    def visit(self, node: ast.StringNode, scope: Scope):
        self.add_comment(
            'Instantiating string: ' +
            (node.lex if len(node.lex) < 20 else node.lex[:15] + '...')
        )

        value = self.visit(node.lex, scope)
        str_instance = self.add_local('str_instance')
        self.add_inst(cil.StaticCallNode('String__init', str_instance))
        attr_index = self.root.get_type('String').attributes.index('String_value')
        attr_at = cil.AttributeAt('String_value', attr_index)
        self.add_inst(cil.SetAttrNode(str_instance, attr_at, value))
        return str_instance

    @visitor.when(ast.IntegerNode)
    def visit(self, node: ast.IntegerNode, scope: Scope):
        value = self.visit(int(node.lex), scope)
        int_instance = self.add_local('int_instance')
        self.add_inst(cil.StaticCallNode('Int__init', int_instance))
        attr_index = self.root.get_type('Int').attributes.index('Int_value')
        attr_at = cil.AttributeAt('Int_value', attr_index)
        self.add_inst(cil.SetAttrNode(int_instance, attr_at, value))
        return int_instance

    @visitor.when(ast.BooleanNode)
    def visit(self, node: ast.BooleanNode, scope: Scope):
        value = self.visit(node.lex == 'true', scope)
        bool_instance = self.add_local('bool_instance')
        self.add_inst(cil.StaticCallNode('Bool__init', bool_instance))
        attr_index = self.root.get_type('Bool').attributes.index('Bool_value')
        attr_at = cil.AttributeAt('Bool_Value', attr_index)
        self.add_inst(cil.SetAttrNode(bool_instance, attr_at, value))
        return bool_instance

    @visitor.when(ast.VariableNode)
    def visit(self, node: ast.VariableNode, _):
        return node.lex

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        return self.build_binary_node(cil.PlusNode, node, scope)

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode, scope: Scope):
        return self.build_binary_node(cil.MinusNode, node, scope)

    @visitor.when(ast.StarNode)
    def visit(self, node: ast.PlusNode, scope: Scope):
        return self.build_binary_node(cil.StarNode, node, scope)

    @visitor.when(ast.DivNode)
    def visit(self, node: ast.DivNode, scope: Scope):
        return self.build_binary_node(cil.DivNode, node, scope)

    @visitor.when(ast.LessThanNode)
    def visit(self, node: ast.LessThanNode, scope: Scope):
        return self.build_binary_node(cil.LessThanNode, node, scope)

    @visitor.when(ast.LessEqualNode)
    def visit(self, node: ast.LessEqualNode, scope: Scope):
        return self.build_binary_node(cil.LessEqualNode, node, scope)

    @visitor.when(ast.EqualNode)
    def visit(self, node: ast.EqualNode, scope: Scope):
        return self.build_binary_node(cil.EqualNode, node, scope)

    def build_binary_node(self, new_node_cls, node: ast.BinaryNode, scope: Scope):
        left_dest = self.visit(node.left, scope)
        right_dest = self.visit(node.right, scope)
        oper_dest = self.add_local('oper_dest')
        self.add_inst(new_node_cls(oper_dest, left_dest, right_dest))
        return oper_dest

    @visitor.when(ast.IsVoidNode)
    def visit(self, node: ast.IsVoidNode, scope: Scope):
        expr_dest = self.visit(node.expr, scope)
        comp_res = self.add_local('comp_res')
        self.add_inst(cil.IsVoidNode(comp_res, expr_dest))
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
