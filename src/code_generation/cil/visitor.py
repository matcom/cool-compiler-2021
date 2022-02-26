import re
from utils.ast import *
from utils import visitor
from semantic.tools import *
from semantic.types import *
from utils.ast import AssignNode
from code_generation.cil.nodes import *
from utils.utils import Utils
from code_generation.cil.built_in.Object.object_functions import build_object_functions
from code_generation.cil.built_in.IO.IO_functions import build_io_functions
from code_generation.cil.built_in.Bool.bool_functions import build_bool_functions
from code_generation.cil.built_in.Int.int_functions import build_int_functions
from code_generation.cil.built_in.String.string_functions import build_string_functions
from constants import INT, LOCAL, STRING, BOOL, OBJECT, IO, MAIN, VOID, VISITOR_NODE, ENTRY, SELF_LOWERCASE, FUNCTION, ATTRIBUTE, TYPE, DATA, CODE, LOCAL
from code_generation.cil.utils import *
from collections import defaultdict
import random
import string

def randStr(chars = string.ascii_lowercase + string.digits, N=10):
	return ''.join(random.choice(chars) for _ in range(N))

COUNT = 0

def increment():
    global COUNT
    COUNT = COUNT+1

class Visitor:
    def __init__(self, context):
        self.cil_program_node_info = defaultdict(lambda: [])
        self.current = defaultdict(lambda: None)
        self.context: Context = context
        self.constrs = []

    def saveCilInstruction(self, instruction):
        self.current[FUNCTION].instructions.append(instruction)
        instruction.index = COUNT
        increment()
        return instruction

    def generateLocalNode(self, input_name):
        name = f'local_{self.current[FUNCTION].name[9:]}_{input_name}_{len(self.current[FUNCTION].local_variables)}'
        local_node = CILLocalNode(name, COUNT)
        increment()
        self.current[FUNCTION].local_variables.append(local_node)
        return name

    def generateDataNode(self, value):
        input_name = f'data_{len(self.cil_program_node_info[DATA])}'
        data_node = CILDataNode(input_name, value, COUNT)
        increment()
        self.cil_program_node_info[DATA].append(data_node)
        return data_node

    @visitor.on(VISITOR_NODE)
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope: Scope):
        function_node = CILFunctionNode(ENTRY, [], [], [], COUNT)
        increment()
        self.cil_program_node_info[CODE].append(function_node)
        self.current[FUNCTION] = function_node
        idx = COUNT
        increment()
        instance = self.generateLocalNode(LOCAL)
        local_node = self.generateLocalNode(LOCAL)

        self.saveCilInstruction(CILAllocateNode(MAIN, instance))
        typex = self.context.get_type(MAIN, (0, 0))
        if typex.all_attributes():
            self.saveCilInstruction(CILStaticCallNode(typex.name, typex.name, None, [CILArgNode(instance)], typex.name))

        self.saveCilInstruction(CILStaticCallNode(MAIN, MAIN.lower(), local_node, [CILArgNode(instance)], OBJECT))
        self.saveCilInstruction(CILReturnNode(0))
        self.current[FUNCTION] = None

        (object_cil_code, object_methods) = build_object_functions(COUNT)
        increment()
        (bool_cil_code, bool_methods) = build_bool_functions(COUNT)
        increment()
        (string_cil_code, string_methods) = build_string_functions(COUNT)
        increment()
        (io_cil_code, io_methods) = build_io_functions(COUNT)
        increment()
        (int_cil_code, int_methods) = build_int_functions(COUNT)
        increment()

        self.cil_program_node_info[CODE] += [*object_cil_code, *io_cil_code,
                         *string_cil_code, *int_cil_code, *bool_cil_code]
        self.cil_program_node_info[TYPE] += [CILTypeNode(OBJECT, [], object_methods), CILTypeNode(IO, [], object_methods + io_methods),
                          CILTypeNode(STRING, [],  string_methods), CILTypeNode(INT, [], int_methods), CILTypeNode(BOOL, [], bool_methods)]

        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)

        return CILProgramNode(self.cil_program_node_info, idx)

    @visitor.when(ClassDeclarationNode)
    def visit(self, node: ClassDeclarationNode, scope: Scope):
        self.current[TYPE] = self.context.get_type(node.id, node.pos)
        cil_type = CILTypeNode(node.id)
        self.cil_program_node_info[TYPE].append(cil_type)

        attrs = self.current[TYPE].all_attributes()
        if len(attrs) > 0:
            constr = FuncDeclarationNode(node.token, [], node.token, BlockNode([], node.token))
            func_declarations = [constr]
            self.constrs.append(node.id)
            self.current[TYPE].define_method(self.current[TYPE].name, [], [], self.current[TYPE], node.pos)
            scopes = [scope] + list(scope.functions.values())
        else:
            func_declarations = []
            scopes = list(scope.functions.values())

        for attr, a_type in attrs:
            cil_type.attributes.append(
                (attr.name, create_name2(ATTRIBUTE, attr.name, a_type.name)))
            if attr.expr:
                constr.body.expr_list.append(AssignNode(attr.name, attr.expr))
            elif attr.type == INT:
                constr.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
            elif attr.type == BOOL:
                constr.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
            elif attr.type == STRING:
                constr.body.expr_list.append( AssignNode(attr.name, ConstantStrNode("")))
            else:
                constr.body.expr_list.append(AssignNode(attr.name, ConstantVoidNode(attr.name)))
            if attrs:
                constr.body.expr_list.append(SelfNode())

        for method, mtype in self.current[TYPE].all_methods():
            cil_type.methods.append(
                (method.name, create_name2(FUNCTION, method.name, mtype.name)))

        func_declarations += [
            f for f in node.features if isinstance(f, FuncDeclarationNode)]
        for feature, child_scope in zip(func_declarations, scopes):
            self.visit(feature, child_scope)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node: FuncDeclarationNode, scope: Scope):
        current_method = self.current[TYPE].get_method(node.id, node.pos)

        name = create_name2(FUNCTION, node.id, self.current[TYPE].name)
        function_node = CILFunctionNode(name, [], [], [], COUNT)
        increment()
        self.cil_program_node_info[CODE].append(function_node)
        self.current[FUNCTION] = function_node

        param_node = CILParamNode(SELF_LOWERCASE, self.current[TYPE].name, COUNT)
        increment()
        self.current[FUNCTION].params.append(param_node)
        for p_name, p_type in node.params:
            param_node = CILParamNode(p_name, p_type.value, COUNT)
            increment()
            self.current[FUNCTION].params.append(param_node)

        value, typex = self.visit(node.body, scope)
        if not isinstance(value, str):
            local_node = self.generateLocalNode(LOCAL)
            self.saveCilInstruction(CILAssignNode(local_node, value))
        else:
            local_node = value

        if typex.name in [STRING, BOOL, INT] and current_method.return_type.name == OBJECT:
            self.saveCilInstruction(CILBoxingNode(local_node, typex.name))

        self.saveCilInstruction(CILReturnNode(local_node))

    @visitor.when(VarDeclarationNode)
    def visit(self, node: VarDeclarationNode, scope: Scope):
        var_info = scope.find_variable(node.id)
        vtype = Utils.GetType(var_info.type, self.current[TYPE])
        local_var = self.generateLocalNode(var_info.name)

        value, typex = self.visit(node.expr, scope)
        if vtype.name == OBJECT and typex.name in [STRING, INT, BOOL]:
            self.saveCilInstruction(CILBoxingNode(local_var, typex.name))
        else:
            self.saveCilInstruction(CILAssignNode(local_var, value))
        return local_var, vtype

    def toVarName(self, var_name):
        regex = re.compile(f'local_{self.current[FUNCTION].name[9:]}_(.+)_\d+')
        for node in reversed(self.current[FUNCTION].local_variables):
            m = regex.match(node.name).groups()[0]
            if m == var_name:
                return node.name
        for node in self.current[FUNCTION].params:
            if node.name == var_name:
                return var_name
        return None

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        var_info = scope.find_local(node.id)
        value, typex = self.visit(node.expr, scope)
        if var_info is None:
            var_info = scope.find_attribute(node.id)
            if var_info.type.name == OBJECT and typex.name in [STRING, BOOL, INT]:
                value = self.generateLocalNode(LOCAL)
                self.saveCilInstruction(CILBoxingNode(value, typex.name))
            self.saveCilInstruction(CILSetAttribNode(SELF_LOWERCASE, var_info.name, self.current[TYPE].name, value))
        else:
            local_name = self.toVarName(var_info.name)
            if var_info.type.name == OBJECT and typex.name in [STRING, BOOL, INT]:
                self.saveCilInstruction(
                    CILBoxingNode(local_name, typex.name))
            else:
                self.saveCilInstruction(CILAssignNode(local_name, value))
        return value, typex

    def rt_type(self, typex: Type, node):
        meth = typex.get_method(node.id, node.pos)
        return Utils.GetType(meth.return_type, self.current[TYPE])

    def checkingVoid(self, expr):
        local_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILTypeOfNode(expr, local_node))

        void_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILLoadNode(void_node, self.generateDataNode(VOID).name))
        self.saveCilInstruction(CILEqualNode(local_node, local_node, void_node))
        return local_node

    def argumentsNode(self, args, scope, param_types):
        args_node = []
        args = [self.visit(arg, scope) for arg in args]

        for (arg, typex), param_type in zip(args, param_types):
            if typex.name in [STRING, INT, BOOL] and param_type.name == OBJECT:
                local_node = self.generateLocalNode(LOCAL)
                self.saveCilInstruction(CILBoxingNode(local_node, typex.name))
            else:
                local_node = arg
            args_node.append(CILArgNode(local_node, COUNT))
            increment()
        return args_node

    @visitor.when(CallNode)
    def visit(self, node: CallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)

        meth = otype.get_method(node.id, node.pos)
        args_node = [CILArgNode(
            obj, COUNT)] + self.argumentsNode(node.args, scope, meth.param_types)
        increment()

        rtype = meth.return_type
        result = None if isinstance(
            rtype, VoidType) else self.generateLocalNode(LOCAL)

        continue_label = CILLabelNode(f'continue__{COUNT}')
        increment()
        isvoid = self.checkingVoid(obj)
        self.saveCilInstruction(
            CILGotoIfFalseNode(isvoid, continue_label.label))
        self.saveCilInstruction(CILErrorNode('dispatch_error'))
        self.saveCilInstruction(continue_label)

        if otype in [StringType(), IntType(), BoolType()]:
            self.saveCilInstruction(CILStaticCallNode(
                otype.name, node.id, result, args_node, rtype.name))
        else:
            self.saveCilInstruction(CILDynamicCallNode(
                otype.name, obj, node.id, result, args_node, rtype.name))
        return result, self.rt_type(otype, node)

    @visitor.when(BaseCallNode)
    def visit(self, node: BaseCallNode, scope: Scope):
        obj, otype = self.visit(node.obj, scope)

        meth = otype.get_method(node.id, node.pos)
        args_node = [CILArgNode(
            obj, COUNT)] + self.argumentsNode(node.args, scope, meth.param_types)
        increment()

        rtype = meth.return_type
        result = None if isinstance(
            rtype, VoidType) else self.generateLocalNode(LOCAL)

        continue_label = CILLabelNode(f'continue__{COUNT}')
        increment()
        isvoid = self.checkingVoid(obj)
        self.saveCilInstruction(
            CILGotoIfFalseNode(isvoid, continue_label.label))
        self.saveCilInstruction(CILErrorNode('dispatch_error'))
        self.saveCilInstruction(continue_label)

        self.saveCilInstruction(CILStaticCallNode(
            node.type, node.id, result, args_node, rtype.name))
        return result, self.rt_type(otype, node)

    @visitor.when(StaticCallNode)
    def visit(self, node: StaticCallNode, scope: Scope):
        meth = self.current[TYPE].get_method(node.id, node.pos)
        args_node = [CILArgNode(SELF_LOWERCASE, COUNT)] + \
            self.argumentsNode(node.args, scope, meth.param_types)
        increment()

        rtype = meth.return_type
        if isinstance(rtype, VoidType):
            local_node = None
        else:
            local_node = self.generateLocalNode(LOCAL)

        self.saveCilInstruction(CILDynamicCallNode(
            self.current[TYPE].name, SELF_LOWERCASE, node.id, local_node, args_node, rtype.name))
        return local_node, self.rt_type(self.current[TYPE], node)

    @visitor.when(ConstantNumNode)
    def visit(self, node: ConstantNumNode, scope: Scope):
        return int(node.lex), IntType()

    @visitor.when(ConstantBoolNode)
    def visit(self, node: ConstantBoolNode, scope: Scope):
        return 1 if node.lex == 'true' else 0, BoolType()

    @visitor.when(ConstantStrNode)
    def visit(self, node: ConstantStrNode, scope: Scope):
        data = self.generateDataNode(node.lex)
        local_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILLoadNode(local_node, data.name))
        return local_node, StringType()

    @visitor.when(ConstantVoidNode)
    def visit(self, node: ConstantVoidNode, scope: Scope):
        local_node = self.generateLocalNode(node.lex)
        void = CILVoidConstantNode(local_node)
        self.saveCilInstruction(void)
        return local_node, VoidType()

    @visitor.when(SelfNode)
    def visit(self, node: SelfNode, scope: Scope):
        return SELF_LOWERCASE, self.current[TYPE]

    @visitor.when(VariableNode)
    def visit(self, node: VariableNode, scope: Scope):
        try:
            typex = scope.find_local(node.lex).type
            name = self.toVarName(node.lex)
            return name, Utils.GetType(typex, self.current[TYPE])
        except:
            var_info = scope.find_attribute(node.lex)
            local_var = self.generateLocalNode(var_info.name)
            self.saveCilInstruction(CILGetAttribNode(
                SELF_LOWERCASE, var_info.name, self.current[TYPE].name, local_var, var_info.type.name))
            return local_var, Utils.GetType(var_info.type, self.current[TYPE])

    @visitor.when(InstantiateNode)
    def visit(self, node: InstantiateNode, scope: Scope):
        instance = self.generateLocalNode(LOCAL)
        typex = self.context.get_type(node.lex, node.pos)
        typex = Utils.GetType(typex, self.current[TYPE])
        self.saveCilInstruction(CILAllocateNode(typex.name, instance))

        if typex.all_attributes():
            self.saveCilInstruction(CILStaticCallNode(
                typex.name, typex.name, instance, [CILArgNode(instance)], typex.name))

        return instance, typex

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        start = CILLabelNode(f'start__{COUNT}')
        end = CILLabelNode(f'end__{COUNT}')

        local_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILVoidConstantNode(local_node))
        self.saveCilInstruction(start)

        cond, _ = self.visit(node.cond, scope)
        self.saveCilInstruction(CILGotoIfFalseNode(cond, end.label))
        expr, typex = self.visit(node.expr, scope)
        self.saveCilInstruction(CILAssignNode(local_node, expr))
        self.saveCilInstruction(CILGotoNode(start.label))
        self.saveCilInstruction(end)

        return local_node, ObjectType()

    @visitor.when(ConditionalNode)
    def visit(self, node: ConditionalNode, scope: Scope):
        cond, _ = self.visit(node.cond, scope)

        true_label = CILLabelNode(f"true__{COUNT}")
        end = CILLabelNode(f"end__{COUNT}")

        local_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILGotoIfNode(cond, true_label.label))

        false_expr, ftypex = self.visit(node.else_stm, scope)
        self.saveCilInstruction(CILAssignNode(local_node, false_expr))
        self.saveCilInstruction(CILGotoNode(end.label))
        self.saveCilInstruction(true_label)

        true_expr, ttypex = self.visit(node.stm, scope)
        self.saveCilInstruction(CILAssignNode(local_node, true_expr))
        self.saveCilInstruction(end)
        return local_node, Utils.GetCommonBaseType([ttypex, ftypex])

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        value = None
        for exp in node.expr_list:
            value, typex = self.visit(exp, scope)
        local_node = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILAssignNode(local_node, value))
        return local_node, typex

    def sorting(self, case_list):
        return sorted(case_list, reverse=True, key=lambda x: self.context.get_depth(x.typex))

    @visitor.when(CaseNode)
    def visit(self, node: CaseNode, scope: Scope):
        expr, typex = self.visit(node.expr, scope)

        local_node = self.generateLocalNode(LOCAL)
        end = CILLabelNode(f'end__{COUNT}')
        error_label = CILLabelNode(f'error__{COUNT}')

        isvoid = self.checkingVoid(expr)
        self.saveCilInstruction(CILGotoIfNode(isvoid, error_label.label))

        try:
            new_scope = scope.expr_dict[node]
        except:
            new_scope = scope
        sorted_case_list = self.sorting(node.case_list)
        for i, case in enumerate(sorted_case_list):
            next_label = CILLabelNode(f'next__{COUNT}_{i}')
            expr_i = self.visit(
                case, new_scope.create_child(), expr, next_label, typex)
            self.saveCilInstruction(CILAssignNode(local_node, expr_i))
            self.saveCilInstruction(CILGotoNode(end.label))
            self.saveCilInstruction(next_label)
        self.saveCilInstruction(CILErrorNode('case_error'))
        self.saveCilInstruction(error_label)
        self.saveCilInstruction(CILErrorNode('case_void_error'))
        self.saveCilInstruction(end)
        return local_node, typex

    @visitor.when(OptionNode)
    def visit(self, node: OptionNode, scope: Scope, expr, next_label, type_e):
        aux = self.generateLocalNode(LOCAL)
        self.saveCilInstruction(CILConformsNode(aux, expr, node.typex))
        self.saveCilInstruction(
            CILGotoIfFalseNode(aux, next_label.label))

        local_var = self.generateLocalNode(node.id)
        typex = self.context.get_type(node.typex, node.type_pos)
        scope.define_variable(node.id, typex)
        if typex.name == OBJECT and type_e.name in [STRING, INT, BOOL]:
            self.saveCilInstruction(
                CILBoxingNode(local_var, type_e.name))
        else:
            self.saveCilInstruction(CILAssignNode(local_var, expr))
        expr_i, type_expr = self.visit(node.expr, scope)
        return expr_i

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        return self.create_u_node(node, scope, CILLogicalNotNode)

    @visitor.when(BinaryNotNode)
    def visit(self, node: BinaryNotNode, scope: Scope):
        return self.create_u_node(node, scope, CILNotNode)

    @visitor.when(IsVoidNode)
    def visit(self, node: IsVoidNode, scope: Scope):
        expr, _ = self.visit(node.expr, scope)
        result = self.checkingVoid(expr)
        return result, BoolType()

    def create_b_node(self, node: CILBinaryNode, scope: Scope, cil_node: CILNode):
        local_node = self.generateLocalNode(LOCAL)
        left, typex = self.visit(node.left, scope)
        right, typex = self.visit(node.right, scope)
        self.saveCilInstruction(cil_node(local_node, left, right))
        return local_node, typex

    def create_u_node(self, node: CLIUnaryNode, scope: Scope, cil_node):
        local_node = self.generateLocalNode(LOCAL)
        expr, typex = self.visit(node.expr, scope)
        self.saveCilInstruction(cil_node(local_node, expr))
        return local_node, typex

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode, scope: Scope):
        return self.create_b_node(node, scope, CILPlusNode)

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode, scope: Scope):
        return self.create_b_node(node, scope, CILMinusNode)

    @visitor.when(StarNode)
    def visit(self, node: StarNode, scope: Scope):
        return self.create_b_node(node, scope, CILStarNode)

    @visitor.when(DivNode)
    def visit(self, node: DivNode, scope: Scope):
        return self.create_b_node(node, scope, CILDivNode)

    @visitor.when(LessNode)
    def visit(self, node: LessNode, scope: Scope):
        return self.create_b_node(node, scope, CILLessNode)

    @visitor.when(LessEqNode)
    def visit(self, node: LessEqNode, scope: Scope):
        return self.create_b_node(node, scope, CILLessEqNode)

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        return self.create_b_node(node, scope, CILEqualNode)

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = scope.expr_dict[node]
        for init in node.init_list:
            self.visit(init, child_scope)

        expr, typex = self.visit(node.expr, child_scope)
        return expr, typex