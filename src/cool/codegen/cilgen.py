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
        f1_params = [ParamNode("self", 'Object')]
        f1_localVars = [LocalNode("local_abort_Object_self_0")]
        f1_instructions = [ast_cil.AssignNode(f1_localVars[0].name, f1_params[0].name, self.index),
                           ast_cil.ExitNode(f1_params[0].name, idx=self.index)]
        f1 = FunctionNode("function_abort_Object", f1_params, f1_localVars, f1_instructions)

        f2_params = [ParamNode("self", 'Object')]
        f2_localVars = [LocalNode("local_type_name_Object_result_0")]
        f2_instructions = [ast_cil.TypeOfNode(f2_params[0].name, f2_localVars[0].name, self.index),
                           ast_cil.ReturnNode(f2_localVars[0].name, self.index)]
        f2 = FunctionNode("function_type_name_Object", f2_params, f2_localVars, f2_instructions)

        f3_params = [ParamNode("self", 'Object')]
        f3_localVars = [LocalNode("local_copy_Object_result_0")]
        f3_instructions = [ast_cil.CopyNode(f3_localVars[0].name, f3_params[0].name, self.index),
                           ast_cil.ReturnNode(f3_localVars[0].name, self.index)]
        f3 = FunctionNode("function_copy_Object", f3_params, f3_localVars, f3_instructions)

        f4_params = [ParamNode("self", 'IO'), ParamNode("word", 'String')]
        f4_localVars = [LocalNode("local_out_string_String_self_0")]
        f4_instructions = [ast_cil.AssignNode(f4_localVars[0].name, f4_params[0].name, self.index),
                           ast_cil.OutStringNode(f4_params[1].name, self.index),
                           ast_cil.ReturnNode(f4_localVars[0].name, self.index)]
        f4 = FunctionNode("function_out_string_IO", f4_params, f4_localVars, f4_instructions)

        f5_params = [ParamNode("self", 'IO'), ParamNode("number", 'Int')]
        f5_localVars = [LocalNode("local_out_int_IO_self_0")]
        f5_instructions = [ast_cil.AssignNode(f5_localVars[0].name, f5_params[0].name, self.index),
                           ast_cil.OutIntNode(f5_params[1].name, self.index),
                           ast_cil.ReturnNode(f5_localVars[0].name, self.index)]
        f5 = FunctionNode("function_out_int_IO", f5_params, f5_localVars, f5_instructions)

        f6_params = [ParamNode("self", 'IO')]
        f6_localVars = [LocalNode("local_in_int_IO_result_0")]
        f6_instructions = [ast_cil.ReadIntNode(f6_localVars[0].name, self.index),
                           ast_cil.ReturnNode(f6_localVars[0].name, self.index)]
        f6 = FunctionNode("function_in_int_IO", f6_params, f6_localVars, f6_instructions)

        f7_params = [ParamNode("self", 'IO')]
        f7_localVars = [LocalNode("local_in_string_IO_result_0")]
        f7_instructions = [ast_cil.ReadStringNode(f7_localVars[0].name, self.index),
                           ast_cil.ReturnNode(f7_localVars[0].name, self.index)]
        f7 = FunctionNode("function_in_string_IO", f7_params, f7_localVars, f7_instructions)

        f8_params = [ParamNode("self", 'String')]
        f8_localVars = [LocalNode("local_length_String_result_0")]
        f8_instructions = [ast_cil.LengthNode(f8_localVars[0].name, f8_params[0].name, self.index),
                           ast_cil.ReturnNode(f8_localVars[0].name, self.index)]
        f8 = FunctionNode("function_length_String", f8_params, f8_localVars, f8_instructions)

        f9_params = [ParamNode("self", 'String'), ParamNode("word", 'String')]
        f9_localVars = [LocalNode("local_concat_String_result_0")]
        f9_instructions = [ast_cil.ConcatNode(f9_localVars[0].name, f9_params[0].name, f9_params[1].name, self.index),
                           ast_cil.ReturnNode(f9_localVars[0].name, self.index)]
        f9 = FunctionNode("function_concat_String", f9_params, f9_localVars, f9_instructions)

        f10_params = [ParamNode("self", 'String'), ParamNode("begin", 'Int'), ParamNode("end", 'Int')]
        f10_localVars = [LocalNode("local_substr_String_result_0")]
        f10_instructions = [
            ast_cil.SubstringNode(f10_localVars[0].name, f10_params[0].name, f10_params[1].name, f10_params[2].name,
                                  self.index),
            ast_cil.ReturnNode(f10_localVars[0].name, self.index)]
        f10 = FunctionNode("function_substr_String", f10_params, f10_localVars, f10_instructions)

        f11_params = [ParamNode("self", 'String')]
        f11_localVars = [LocalNode("local_type_name_String_result_0")]
        f11_instructions = [ast_cil.LoadNode(f11_localVars[0].name, 'type_String', self.index),
                            ast_cil.ReturnNode(f11_localVars[0].name, self.index)]
        f11 = FunctionNode("function_type_name_String", f11_params, f11_localVars, f11_instructions)

        f12_params = [ParamNode("self", 'String')]
        f12_localVars = [LocalNode("local_copy_String_result_0")]
        f12_instructions = [ast_cil.ConcatNode(f12_localVars[0].name, f12_params[0].name, None, self.index),
                            ast_cil.ReturnNode(f12_localVars[0].name, self.index)]
        f12 = FunctionNode("function_copy_String", f12_params, f12_localVars, f12_instructions)

        f17_params = [ParamNode("self", 'String')]
        f17_localVars = [LocalNode('local_abort_String_msg_0')]
        f17_instructions = [ast_cil.LoadNode(f17_params[0].name, 'string_abort'),
                            ast_cil.OutStringNode(f17_params[0].name, self.index),
                            ast_cil.ExitNode(f17_params[0].name, idx=self.index)]
        f17 = FunctionNode("function_abort_String", f17_params, f17_localVars, f17_instructions)

        f13_params = [ParamNode("self", 'Int')]
        f13_localVars = [LocalNode("local_type_name_Int_result_0")]
        f13_instructions = [ast_cil.LoadNode(f13_localVars[0].name, 'type_Int', self.index),
                            ast_cil.ReturnNode(f13_localVars[0].name, self.index)]
        f13 = FunctionNode("function_type_name_Int", f13_params, f13_localVars, f13_instructions)

        f14_params = [ParamNode("self", 'Int')]
        f14_localVars = [LocalNode("local_copy_Int_result_0")]
        f14_instructions = [ast_cil.AssignNode(f14_localVars[0].name, f14_params[0].name),
                            ast_cil.ReturnNode(f14_localVars[0].name, self.index)]
        f14 = FunctionNode("function_copy_Int", f14_params, f14_localVars, f14_instructions)

        f18_params = [ParamNode("self", 'Int')]
        f18_localVars = [LocalNode('local_abort_Int_msg_0')]
        f18_instructions = [ast_cil.LoadNode(f18_params[0].name, 'int_abort'),
                            ast_cil.OutStringNode(f18_params[0].name, self.index),
                            ast_cil.ExitNode(f18_params[0].name, idx=self.index)]
        f18 = FunctionNode("function_abort_Int", f18_params, f18_localVars, f18_instructions)

        f15_params = [ParamNode("self", 'Bool')]
        f15_localVars = [LocalNode("local_type_name_Bool_result_0")]
        f15_instructions = [ast_cil.LoadNode(f15_localVars[0].name, 'type_Bool', self.index),
                            ast_cil.ReturnNode(f15_localVars[0].name, self.index)]
        f15 = FunctionNode("function_type_name_Bool", f15_params, f15_localVars, f15_instructions)

        f16_params = [ParamNode("self", 'Bool')]
        f16_localVars = [LocalNode("local_copy_result_Bool_0")]
        f16_instructions = [ast_cil.AssignNode(f16_localVars[0].name, f16_params[0].name),
                            ast_cil.ReturnNode(f16_localVars[0].name, self.index)]
        f16 = FunctionNode("function_copy_Bool", f16_params, f16_localVars, f16_instructions)

        f19_params = [ParamNode("self", 'Bool')]
        f19_localVars = [LocalNode('local_abort_Bool_msg_0')]
        f19_instructions = [ast_cil.LoadNode(f19_params[0].name, 'bool_abort'),
                            ast_cil.OutStringNode(f19_params[0].name, self.index),
                            ast_cil.ExitNode(f19_params[0].name, idx=self.index)]
        f19 = FunctionNode("function_abort_Bool", f19_params, f19_localVars, f19_instructions)

        self.fun_nodes += [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13, f14, f15, f16, f17, f18, f19]
        object_methods = [('abort', f1.name), ('type_name', f2.name), ('copy', f3.name)]
        string_methods = [('length', f8.name), ('concat', f9.name), ('substr', f10.name), ('abort', f17.name),
                          ('type_name', f11.name), ('copy', f12.name)]
        io_methods = [('out_string', f4.name), ('out_int', f5.name), ('in_int', f6.name), ('in_string', f7.name)]
        int_methods = [('abort', f18.name), ('type_name', f13.name), ('copy', f14.name)]
        bool_methods = [('abort', f19.name), ('type_name', f15.name), ('copy', f16.name)]

        a = TypeNode("String", [], string_methods)

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
