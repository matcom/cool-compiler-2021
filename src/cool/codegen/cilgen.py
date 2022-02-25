from .utils import ProgramNode, LocalNode, FunctionNode, TypeNode, DataNode, ParamNode
from .utils import ast_cil
from ..semantic.helpers import Context, VariableInfo, Scope
from ..semantic.types import Attribute, Type, StringType, ObjectType, IOType, Method
import re
from ..utils.ast import BinaryNode, UnaryNode, AssignNode, ConstantBoolNode, ConstantVoidNode, ConstantStrNode, \
    ConstantNumNode


class BaseCil:
    def __init__(self, context):
        self.current_function = None
        self.current_type: Type = None
        self.current_method: Method = None
        self.fun_nodes = []
        self.data = []
        self.types_nodes = []
        self.context = context
        self.idx = 0
        self.void_data = None
        self.constructors = []
        self.void_data = None
        self.inherit_graph = {}

    @property
    def params(self):
        return self.current_function.params

    @property
    def index(self):
        t = self.idx
        self.idx += 1
        return t

    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def instructions(self):
        return self.current_function.instructions

    def register_param(self, vname, vtype):
        # name = f'param_{self.current_function.name[9:]}_{vname}_{len(self.params)}'
        param_node = ParamNode(vname, vtype, self.index)
        self.params.append(param_node)
        return vname

    def register_local(self, vname):
        name = f'local_{self.current_function.name[9:]}_{vname}_{len(self.localvars)}'
        local_node = LocalNode(name, self.index)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self):
        return self.register_local('internal')

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        instruction.index = self.index
        return instruction

    def to_attr_name(self, attr_name, type_name):
        return f'attribute_{attr_name}_{type_name}'

    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_{type_name}'

    def to_var_name(self, var_name):
        regex = re.compile(f'local_{self.current_function.name[9:]}_(.+)_\d+')
        for node in reversed(self.localvars):
            m = regex.match(node.name).groups()[0]
            if m == var_name:
                return node.name
        for node in self.params:
            if node.name == var_name:
                return var_name
        return None

    def register_function(self, function_name):
        node = FunctionNode(function_name, [], [], [], self.index)
        self.fun_nodes.append(node)
        return node

    def register_type(self, type_name):
        node = TypeNode(type_name)
        self.types_nodes.append(node)
        return node

    def register_data(self, value):
        vname = f'data_{len(self.data)}'
        node = DataNode(vname, value, self.index)
        self.data.append(node)
        return node

    def _define_binary_node(self, node: BinaryNode, scope: Scope, cil_node: ast_cil.Node):
        result = self.define_internal_local()
        left, typex = self.visit(node.left, scope)
        right, typex = self.visit(node.right, scope)
        self.register_instruction(cil_node(result, left, right))
        return result, typex

    def _define_unary_node(self, node: UnaryNode, scope: Scope, cil_node):
        result = self.define_internal_local()
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil_node(result, expr))
        return result, typex

    def initialize_attr(self, constructor, attr: Attribute, scope: Scope):
        if attr.expr:
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))
        else:
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantVoidNode(attr.name)))

    def built_in_functions(self):
        func1_params = [ParamNode("self", 'Object')]
        func1_localVars = [LocalNode("local_abort_Object_self_0")]
        func1_instructions = [ast_cil.AssignNode(func1_localVars[0].name, func1_params[0].name, self.index),
                              ast_cil.ExitNode(func1_params[0].name, idx=self.index)]
        func1 = FunctionNode("function_abort_Object", func1_params, func1_localVars, func1_instructions)

        func2_params = [ParamNode("self", 'Object')]
        func2_localVars = [LocalNode("local_type_name_Object_result_0")]
        func2_instructions = [ast_cil.TypeOfNode(func2_params[0].name, func2_localVars[0].name, self.index),
                              ast_cil.ReturnNode(func2_localVars[0].name, self.index)]
        func2 = FunctionNode("function_type_name_Object", func2_params, func2_localVars, func2_instructions)

        func3_params = [ParamNode("self", 'Object')]
        func3_localVars = [LocalNode("local_copy_Object_result_0")]
        func3_instructions = [ast_cil.CopyNode(func3_localVars[0].name, func3_params[0].name, self.index),
                              ast_cil.ReturnNode(func3_localVars[0].name, self.index)]
        func3 = FunctionNode("function_copy_Object", func3_params, func3_localVars, func3_instructions)

        func4_params = [ParamNode("self", 'IO'), ParamNode("word", 'String')]
        func4_localVars = [LocalNode("local_out_string_String_self_0")]
        func4_instructions = [ast_cil.AssignNode(func4_localVars[0].name, func4_params[0].name, self.index),
                              ast_cil.OutStringNode(func4_params[1].name, self.index),
                              ast_cil.ReturnNode(func4_localVars[0].name, self.index)]
        func4 = FunctionNode("function_out_string_IO", func4_params, func4_localVars, func4_instructions)

        func5_params = [ParamNode("self", 'IO'), ParamNode("number", 'Int')]
        func5_localVars = [LocalNode("local_out_int_IO_self_0")]
        func5_instructions = [ast_cil.AssignNode(func5_localVars[0].name, func5_params[0].name, self.index),
                              ast_cil.OutIntNode(func5_params[1].name, self.index),
                              ast_cil.ReturnNode(func5_localVars[0].name, self.index)]
        func5 = FunctionNode("function_out_int_IO", func5_params, func5_localVars, func5_instructions)

        func6_params = [ParamNode("self", 'IO')]
        func6_localVars = [LocalNode("local_in_int_IO_result_0")]
        func6_instructions = [ast_cil.ReadIntNode(func6_localVars[0].name, self.index),
                              ast_cil.ReturnNode(func6_localVars[0].name, self.index)]
        func6 = FunctionNode("function_in_int_IO", func6_params, func6_localVars, func6_instructions)

        func7_params = [ParamNode("self", 'IO')]
        func7_localVars = [LocalNode("local_in_string_IO_result_0")]
        func7_instructions = [ast_cil.ReadStringNode(func7_localVars[0].name, self.index),
                              ast_cil.ReturnNode(func7_localVars[0].name, self.index)]
        func7 = FunctionNode("function_in_string_IO", func7_params, func7_localVars, func7_instructions)

        func8_params = [ParamNode("self", 'String')]
        func8_localVars = [LocalNode("local_length_String_result_0")]
        func8_instructions = [ast_cil.LengthNode(func8_localVars[0].name, func8_params[0].name, self.index),
                              ast_cil.ReturnNode(func8_localVars[0].name, self.index)]
        func8 = FunctionNode("function_length_String", func8_params, func8_localVars, func8_instructions)

        func9_params = [ParamNode("self", 'String'), ParamNode("word", 'String')]
        func9_localVars = [LocalNode("local_concat_String_result_0")]
        func9_instructions = [
            ast_cil.ConcatNode(func9_localVars[0].name, func9_params[0].name, func9_params[1].name, self.index),
            ast_cil.ReturnNode(func9_localVars[0].name, self.index)]
        func9 = FunctionNode("function_concat_String", func9_params, func9_localVars, func9_instructions)

        func10_params = [ParamNode("self", 'String'), ParamNode("begin", 'Int'), ParamNode("end", 'Int')]
        func10_localVars = [LocalNode("local_substr_String_result_0")]
        func10_instructions = [
            ast_cil.SubstringNode(func10_localVars[0].name, func10_params[0].name, func10_params[1].name,
                                  func10_params[2].name,
                                  self.index),
            ast_cil.ReturnNode(func10_localVars[0].name, self.index)]
        func10 = FunctionNode("function_substr_String", func10_params, func10_localVars, func10_instructions)

        func11_params = [ParamNode("self", 'String')]
        func11_localVars = [LocalNode("local_type_name_String_result_0")]
        func11_instructions = [ast_cil.LoadNode(func11_localVars[0].name, 'type_String', self.index),
                               ast_cil.ReturnNode(func11_localVars[0].name, self.index)]
        func11 = FunctionNode("function_type_name_String", func11_params, func11_localVars, func11_instructions)

        func12_params = [ParamNode("self", 'String')]
        func12_localVars = [LocalNode("local_copy_String_result_0")]
        func12_instructions = [ast_cil.ConcatNode(func12_localVars[0].name, func12_params[0].name, None, self.index),
                               ast_cil.ReturnNode(func12_localVars[0].name, self.index)]
        func12 = FunctionNode("function_copy_String", func12_params, func12_localVars, func12_instructions)

        func17_params = [ParamNode("self", 'String')]
        func17_localVars = [LocalNode('local_abort_String_msg_0')]
        func17_instructions = [ast_cil.LoadNode(func17_params[0].name, 'string_abort'),
                               ast_cil.OutStringNode(func17_params[0].name, self.index),
                               ast_cil.ExitNode(func17_params[0].name, idx=self.index)]
        func17 = FunctionNode("function_abort_String", func17_params, func17_localVars, func17_instructions)

        func13_params = [ParamNode("self", 'Int')]
        func13_localVars = [LocalNode("local_type_name_Int_result_0")]
        func13_instructions = [ast_cil.LoadNode(func13_localVars[0].name, 'type_Int', self.index),
                               ast_cil.ReturnNode(func13_localVars[0].name, self.index)]
        func13 = FunctionNode("function_type_name_Int", func13_params, func13_localVars, func13_instructions)

        func14_params = [ParamNode("self", 'Int')]
        func14_localVars = [LocalNode("local_copy_Int_result_0")]
        func14_instructions = [ast_cil.AssignNode(func14_localVars[0].name, func14_params[0].name),
                               ast_cil.ReturnNode(func14_localVars[0].name, self.index)]
        func14 = FunctionNode("function_copy_Int", func14_params, func14_localVars, func14_instructions)

        func18_params = [ParamNode("self", 'Int')]
        func18_localVars = [LocalNode('local_abort_Int_msg_0')]
        func18_instructions = [ast_cil.LoadNode(func18_params[0].name, 'int_abort'),
                               ast_cil.OutStringNode(func18_params[0].name, self.index),
                               ast_cil.ExitNode(func18_params[0].name, idx=self.index)]
        func18 = FunctionNode("function_abort_Int", func18_params, func18_localVars, func18_instructions)

        func15_params = [ParamNode("self", 'Bool')]
        func15_localVars = [LocalNode("local_type_name_Bool_result_0")]
        func15_instructions = [ast_cil.LoadNode(func15_localVars[0].name, 'type_Bool', self.index),
                               ast_cil.ReturnNode(func15_localVars[0].name, self.index)]
        func15 = FunctionNode("function_type_name_Bool", func15_params, func15_localVars, func15_instructions)

        func16_params = [ParamNode("self", 'Bool')]
        func16_localVars = [LocalNode("local_copy_result_Bool_0")]
        func16_instructions = [ast_cil.AssignNode(func16_localVars[0].name, func16_params[0].name),
                               ast_cil.ReturnNode(func16_localVars[0].name, self.index)]
        func16 = FunctionNode("function_copy_Bool", func16_params, func16_localVars, func16_instructions)

        func19_params = [ParamNode("self", 'Bool')]
        func19_localVars = [LocalNode('local_abort_Bool_msg_0')]
        func19_instructions = [ast_cil.LoadNode(func19_params[0].name, 'bool_abort'),
                               ast_cil.OutStringNode(func19_params[0].name, self.index),
                               ast_cil.ExitNode(func19_params[0].name, idx=self.index)]
        func19 = FunctionNode("function_abort_Bool", func19_params, func19_localVars, func19_instructions)

        self.fun_nodes += [func1, func2, func3, func4, func5, func6, func7, func8, func9, func10, func11, func12,
                           func13, func14, func15, func16, func17, func18, func19]
        object_methods = [('abort', func1.name), ('type_name', func2.name), ('copy', func3.name)]
        string_methods = [('length', func8.name), ('concat', func9.name), ('substr', func10.name),
                          ('abort', func17.name),
                          ('type_name', func11.name), ('copy', func12.name)]
        io_methods = [('out_string', func4.name), ('out_int', func5.name), ('in_int', func6.name),
                      ('in_string', func7.name)]
        int_methods = [('abort', func18.name), ('type_name', func13.name), ('copy', func14.name)]
        bool_methods = [('abort', func19.name), ('type_name', func15.name), ('copy', func16.name)]

        self.types_nodes += [TypeNode("Object", [], object_methods),
                             TypeNode("IO", [], object_methods + io_methods),
                             TypeNode("String", [], string_methods),
                             TypeNode('Int', [], int_methods),
                             TypeNode('Bool', [], bool_methods)]

    def sort_option_nodes_by_type(self, case_list):
        return sorted(case_list, reverse=True,
                      key=lambda x: self.context.get_depth(x.typex))

    def check_void(self, expr):
        result = self.define_internal_local()
        self.register_instruction(ast_cil.TypeOfNode(expr, result))

        void_expr = self.define_internal_local()
        self.register_instruction(ast_cil.LoadNode(void_expr, self.void_data))
        self.register_instruction(ast_cil.EqualNode(result, result, void_expr))
        return result

    def handle_arguments(self, args, scope, param_types):
        args_node = []
        args = [self.visit(arg, scope) for arg in args]

        for (arg, typex), param_type in zip(args, param_types):
            if typex.name in ['String', 'Int', 'Bool'] and param_type.name == 'Object':
                auxiliar = self.define_internal_local()
                self.register_instruction(ast_cil.BoxingNode(auxiliar, typex.name))
            else:
                auxiliar = arg
            args_node.append(ast_cil.ArgNode(auxiliar, self.index))
        return args_node
