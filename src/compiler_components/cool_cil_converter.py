from .code_generator.converter import Converter
from .code_generator.converter_utils import *
from .code_generator.cil_nodes import *
from .code_generator import visitor
from .ast import *


class CoolToCilConverter(Converter):
    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        self.current_function = register_function(self, 'main')
        instance = define_internal_local(self)
        result = define_internal_local(self)
        result2 = define_internal_local(self)

        register_instruction(self, CilAllocateNode('Main', instance))
        register_instruction(self, CilArgsNode([instance]))

        register_instruction(self, CilJumpNode(to_function_name('Ctr', 'Main'), result))
        register_instruction(self, CilArgsNode([result]))

        real_method = get_method(self, self.context.get_type('Main').name, 'main')
        register_instruction(self, CilDynamicCallNode('Main', real_method, result2, result))
        register_instruction(self, CilReturnNode(0))
        self.current_function = None

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return CilProgramNode(self.dottypes, self.dotdata, self.dotcode)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)

        cil_type = register_type(self, node.id)

        for attr, type_attr in self.current_type.all_attributes():
            cil_type.attributes.append(to_attribute_name(attr.name))

        for func, type_func in self.current_type.all_methods():
            cil_type.methods.append((func.name, to_function_name(func.name, type_func.name)))

        nodeFunctions = [x for x in node.features if isinstance(x, FuncDeclarationNode)]
        for feature, child_scope in zip(nodeFunctions, scope.children[0].children):
            self.visit(feature, child_scope)

        name = to_function_name("Ctr", self.current_type.name)
        self.current_function = register_function(self, name)
        register_param(self, VariableInfo('self', self.current_type))

        register_instruction(self, CilLoadNode('self', f'{self.current_type.name}_name'))
        register_instruction(self, CilLoadIntNode('self', f'{self.current_type.name}_size', 4))
        register_instruction(self, CilLoadNode('self', f'__virtual_table__{self.current_type.name}', 8))

        initResult = define_internal_local(self)
        register_instruction(self, CilArgsNode(['self']))
        register_instruction(self, CilJumpNode(to_function_name('Init', self.current_type.name), initResult))

        register_instruction(self, CilReturnNode('self'))

        name = to_function_name('Init', self.current_type.name)
        self.current_function = register_function(self, name)
        register_param(self, VariableInfo('self', self.current_type))

        parentResult = define_internal_local(self)
        register_instruction(self, CilArgsNode(['self']))
        register_instruction(self, CilJumpNode(to_function_name('Init', self.current_type.parent.name), parentResult))

        nodeatt = [x for x in node.features if isinstance(x, AttrDeclarationNode)]
        for feature, child_scope in zip(nodeatt, scope.children[1].children):
            self.visit(feature, child_scope)

        register_instruction(self, CilReturnNode('self'))

        self.current_type = None

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        self.current_method = self.current_type.get_method(node.id)

        name = to_function_name(node.id, self.current_type.name)
        self.current_function = register_function(self, name)

        register_param(self, VariableInfo('self', self.current_type))
        for param in scope.locals:
            register_param(self, param)

        value = self.visit(node.body, scope.children[0])

        register_instruction(self, CilReturnNode(value))
        self.current_method = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expr is None:
            value = self.visit(node.expr, scope.children[0])

            if node.type == 'Object' and node.expr.type.name in ['Int', 'Bool', 'String']:
                value = box(self, node.expr.type.name, value)

        else:
            if node.type == 'String':
                internal = define_internal_local(self)
                register_instruction(self, CilLoadAddressNode(internal, "_empty"))
                value = internal
            elif node.type == 'Bool' or node.type == 'Int':
                value = 0
            else:
                internal = define_internal_local(self)
                register_instruction(self, CilLoadAddressNode(internal, "_void"))
                value = internal

        attrib = get_attr(self, self.current_type.name, node.id)
        register_instruction(self, CilSetAttribNode('self', attrib, value))

    @visitor.when(LetNode)
    def visit(self, node, scope):
        scope_open = scope.children[0]

        for init in node.let_body:
            if not init[2] is None:
                value = self.visit(init[2], scope_open)

                if init[2].type.name in ['Int', 'Bool', 'String'] and init[1] == 'Object':
                    value = box(self, init[2].type.name, value)

            else:
                if init[1] == 'String':
                    internal = define_internal_local(self)
                    register_instruction(self, CilLoadAddressNode(internal, "_empty"))
                    value = internal
                elif init[1] == 'Bool' or init[1] == 'Int':
                    value = 0
                else:
                    internal = define_internal_local(self)
                    register_instruction(self, CilLoadAddressNode(internal, "_void"))
                    value = internal

            scope_open = scope_open.children[-1]
            var_info = scope_open.find_variable(init[0])
            vname = register_local(self, var_info)
            register_instruction(self, CilAssignNode(vname, value))

        return self.visit(node.in_body, scope_open.children[0])

    @visitor.when(CaseNode)
    def visit(self, node, scope):
        result = define_internal_local(self)

        internal_expression = define_internal_local(self)
        value_expression = self.visit(node.expression, scope.children[0])
        register_instruction(self, CilAssignNode(internal_expression, value_expression))

        types_ordered = sort_types([self.context.get_type(x[1]) for x in node.branches])
        list_label = []
        labels = dict()

        for typex in types_ordered:
            label_typex = register_label(self)
            labels[typex.name] = label_typex
            pre = get_preorder_types(self, typex)
            for typex2 in pre:
                if not typex2 in [x[0] for x in list_label]:
                    list_label.append((typex2, label_typex))

        for typex in list_label:
            register_instruction(self, CilCaseOption(value_expression, typex[1], typex[0]))

        label_end = register_label(self)
        for branch, scopeBranch in zip(node.branches, scope.children[1].children):
            var_info = scopeBranch.find_variable(branch[0])
            xxx = register_local(self, var_info)
            register_instruction(self, CilLabelNode(labels[branch[1]]))
            register_instruction(self, CilAssignNode(xxx, value_expression))

            value_branch = self.visit(branch[2], scopeBranch)
            register_instruction(self, CilAssignNode(result, value_branch))
            register_instruction(self, CilGotoNode(label_end))

        register_instruction(self, CilLabelNode(label_end))
        return result

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        for expression, child in zip(node.expressions, scope.children):
            value = self.visit(expression, child)

        return value

    @visitor.when(IfNode)
    def visit(self, node, scope):
        cond = self.visit(node.condition, scope.children[0])

        label_true = register_label(self)
        label_false = register_label(self)
        result = define_internal_local(self)

        register_instruction(self, CilGotoIfNode(label_true, cond))
        vfalse = self.visit(node.else_body, scope.children[2])
        register_instruction(self, CilAssignNode(result, vfalse))
        register_instruction(self, CilGotoNode(label_false))
        register_instruction(self, CilLabelNode(label_true))
        vtrue = self.visit(node.if_body, scope.children[1])
        register_instruction(self, CilAssignNode(result, vtrue))
        register_instruction(self, CilLabelNode(label_false))

        return result

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        label_while_start = register_label(self)
        label_while_continue = register_label(self)
        label_while_break = register_label(self)

        register_instruction(self, CilLabelNode(label_while_start))

        cond = self.visit(node.condition, scope.children[0])

        register_instruction(self, CilGotoIfNode(label_while_continue, cond))
        register_instruction(self, CilGotoNode(label_while_break))
        register_instruction(self, CilLabelNode(label_while_continue))
        self.visit(node.body, scope.children[1])
        register_instruction(self, CilGotoNode(label_while_start))
        register_instruction(self, CilLabelNode(label_while_break))

        result = define_internal_local(self)
        register_instruction(self, CilLoadAddressNode(result, "_void"))
        return result

    @visitor.when(AssignNode)
    def visit(self, node, scope):
        vinfo = scope.find_variable(node.id)
        value = self.visit(node.expression, scope.children[0])

        if vinfo is None:
            attrib = get_attr(self, self.current_type.name, node.id)
            register_instruction(self, CilSetAttribNode('self', attrib, value))
        else:
            register_instruction(self, CilAssignNode(vinfo.cilName, value))

        return value

    @visitor.when(DispatchNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        obj = self.visit(node.obj, scope.children[0])

        if node.obj.type.name in ['Int', 'Bool', 'String']:
            if node.id in ['abort', 'type_name', 'copy']:
                obj = self.box(node.obj.type.name, obj)

        valuesArgs = []
        for arg, child in zip(node.args, scope.children[1:]):
            value = self.visit(arg, child)

            if arg.type.name in ['Int', 'Bool', 'String']:
                method = self.context.get_type(node.typex).get_method(node.id)
                param_type = method.param_types[node.args.index(arg)]

                if param_type.name == 'Object':
                    valuesArgs.append(self.box(arg.type.name, value))
                    continue

            valuesArgs.append(value)

        if node.typexa is None:
            node.typex = node.obj.type.name

        register_instruction(self, CilArgsNode(list(reversed(valuesArgs)) + [obj]))

        if node.obj.type.name == 'String' and node.id in ['length', 'concat', 'substr']:
            register_instruction(self, CilJumpNode(self.to_function_name(node.id, 'String'), result))
        else:
            real_method = self.get_method(node.typex, node.id)
            register_instruction(self, CilDynamicCallNode(node.typexa, real_method, result, obj))
        return result

    @visitor.when(CallNode)
    def visit(self, node, scope):
        result = define_internal_local(self)

        values_args = []
        for arg, child in zip(node.args, scope.children):
            value = self.visit(arg, child)

            if arg.type.name in ['Int', 'Bool', 'String']:
                method = self.current_type.get_method(node.id)
                param_type = method.param_types[node.args.index(arg)]

                if param_type.name == 'Object':
                    values_args.append(self.box(arg.type.name, value))
                    continue

            values_args.append(value)

        register_instruction(self, CilArgsNode(list(reversed(values_args)) + ['self']))

        realMethod = get_method(self, self.current_type.name, node.id)
        register_instruction(self, CilStaticCallNode(realMethod, result))
        return result

    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        return int(node.token)

    @visitor.when(ConstantBooleanNode)
    def visit(self, node, scope):
        if node.token:
            return 1
        return 0

    @visitor.when(ConstantStringNode)
    def visit(self, node, scope):
        msg = register_data(self, node.lex).name
        internal = define_internal_local(self)
        register_instruction(self, CilLoadAddressNode(internal, msg))
        return internal

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope):
        if node.token == 'self':
            return 'self'

        vinfo = scope.find_variable(node.token)

        if vinfo is None:
            result = define_internal_local(self)
            attrib = get_attr(self, self.current_type.name, node.token)

            register_instruction(self, CilGetAttribNode('self', attrib, result))
            return result

        return vinfo.cilName

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        if not node.type.name == "Int":
            instance = define_internal_local(self)
            result = define_internal_local(self)
            register_instruction(self, CilAllocateNode(node.type.name, instance))
            register_instruction(self, CilArgsNode([instance]))
            register_instruction(self, CilJumpNode(self.to_function_name('Ctr', node.type.name), result))
            return instance
        else:
            return 0

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        register_instruction(self, CilPlusNode(result, left, right))
        return result

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        register_instruction(self, CilMinusNode(result, left, right))
        return result

    @visitor.when(StarNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        register_instruction(self, CilStarNode(result, left, right))
        return result

    @visitor.when(DivNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])
        register_instruction(self, CilDivNode(result, left, right))
        return result

    @visitor.when(EqualsNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])

        if node.left.type.name == 'String':
            register_instruction(self, CilStringComparer(result, left, right))
        else:
            label_equals = register_label(self)
            labels_end = register_label(self)

            result_comparer = define_internal_local(self)
            register_instruction(self, CilMinusNode(result_comparer, left, right))

            register_instruction(self, CilGotoIfNode(label_equals, result_comparer))
            register_instruction(self, CilAssignNode(result, 1))
            register_instruction(self, CilGotoNode(labels_end))
            register_instruction(self, CilLabelNode(label_equals))
            register_instruction(self, CilAssignNode(result, 0))
            register_instruction(self, CilLabelNode(labels_end))

        return result

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])

        label_true = register_label(self)
        label_end = register_label(self)

        register_instruction(self, CilLessNode(result, left, right, label_true, label_end))
        return result

    @visitor.when(MinorEqualsNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        left = self.visit(node.left, scope.children[0])
        right = self.visit(node.right, scope.children[1])

        label_true = register_label(self)
        label_end = register_label(self)

        register_instruction(self, CilLessEqualNode(result, left, right, label_true, label_end))
        return result

    @visitor.when(NotNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        value = self.visit(node.expression, scope.children[0])

        label_true = register_label(self)
        label_end = register_label(self)

        register_instruction(self, CilGotoIfNode(label_true, value))
        register_instruction(self, CilAssignNode(result, 1))
        register_instruction(self, CilGotoNode(label_end))
        register_instruction(self, CilLabelNode(label_true))
        register_instruction(self, CilAssignNode(result, 0))
        register_instruction(self, CilLabelNode(label_end))

        return result

    @visitor.when(NhanharaNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        expression = self.visit(node.expression, scope.children[0])

        register_instruction(self, CilComplementNode(expression, result))
        return result

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        result = define_internal_local(self)
        expression = self.visit(node.expression, scope.children[0])

        label_end = register_label(self)

        register_instruction(self, CilIsVoidNode(expression, result, label_end))
        return result
