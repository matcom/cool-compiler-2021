import cil_ast as cil
class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.constructors = []
        self.context = context
        self.inherit_graph = {}
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, type, name):
        #'param_{self.current_function.name[9:]}_{vinfo.name}_{len(self.params)}'
        param_node = cil.ParamNode(type, name)
        self.params.append(param_node)
        return name
    
    def register_local(self, name):
        #vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(name)
        self.localvars.append(local_node)
        return name

    def define_internal_local(self):
        return self.register_local('internal')

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
        ###############################
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def to_attribute_name(self, attr_name, type_name):
        return f'function_{attr_name}_at_{type_name}'

    def to_variable_name(self, var_name):
        return f'function_{var_name}'

    def define_method(self, name, param_names, param_types, return_type, pos):
        if name in self.methods:
            error_text = SemanticError.METHOD_ALREADY_DEFINED % name
            raise SemanticError(error_text, *pos)

        method = self.methods[name] = Method(name, param_names, param_types, return_type)
        return method

    def initialize_attr(self, constructor, attr, scope):
        if attr.expr:
            constructor.body.expr_list.append(AssignNode(attr.name, attr.expr))
        elif attr.type == 'Int':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantNumNode(0)))
        elif attr.type == 'Bool':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantBoolNode(False)))
        elif attr.type == 'String':
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantStrNode("")))
        else:
            constructor.body.expr_list.append(AssignNode(attr.name, ConstantVoidNode(atrr.name)))
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def get_all_attributes(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.get_all_attributes(False)
        for attr in self.attributes.values():
            plain[attr.name] = (attr, self)
        return plain.values() if clean else plain

    def get_all_methods(self, clean=True):
        plain = OrderedDict() if self.parent is None else self.parent.get_all_methods(False)
        for method in self.methods.values():
            plain[method.name] = (method, self)
        return plain.values() if clean else plain

    def define_built_in(self):
        #regular function
        f1_params = [cil.ParamNode("self", 'Object')]
        f1_localVars = [cil.LocalNode("local_abort_Object_self_0")]
        f1_intructions = [cil.AssignNode(f1_localVars[0].name,f1_params[0].name),
                          cil.ExitNode(f1_params[0].name)]
        f1 = cil.FunctionNode("function_abort_Object",f1_params,f1_localVars,f1_intructions)

        f2_params = [cil.ParamNode("self", 'Object')]
        f2_localVars = [cil.LocalNode("local_type_name_Object_result_0")]
        f2_intructions = [cil.TypeOfNode(f2_params[0].name,f2_localVars[0].name),
                          cil.ReturnNode(f2_localVars[0].name)]
        f2 = cil.FunctionNode("function_type_name_Object",f2_params,f2_localVars,f2_intructions)

        f3_params = [cil.ParamNode("self", 'Object')]
        f3_localVars = [cil.LocalNode("local_copy_Object_result_0")]
        f3_intructions = [cil.CopyNode(f3_localVars[0].name,f3_params[0].name),
                          cil.ReturnNode(f3_localVars[0].name)]
        f3 = cil.FunctionNode("function_copy_Object",f3_params,f3_localVars,f3_intructions)

        #IO out
        f4_params = [cil.ParamNode("self", 'IO'), cil.ParamNode("word", 'String')]
        f4_localVars = [cil.LocalNode("local_out_string_String_self_0")]
        f4_intructions = [cil.AssignNode(f4_localVars[0].name, f4_params[0].name),
                          cil.OutStringNode(f4_params[1].name),
                          cil.ReturnNode(f4_localVars[0].name)]
        f4 = cil.FunctionNode("function_out_string_IO",f4_params,f4_localVars,f4_intructions)

        f5_params = [cil.ParamNode("self", 'IO'), cil.ParamNode("number", 'Int')]
        f5_localVars = [cil.LocalNode("local_out_int_IO_self_0")]
        f5_intructions = [cil.AssignNode(f5_localVars[0].name,f5_params[0].name),
                          cil.OutIntNode(f5_params[1].name),
                          cil.ReturnNode(f5_localVars[0].name)]
        f5 = cil.FunctionNode("function_out_int_IO",f5_params,f5_localVars,f5_intructions)

        #IO in
        f6_params = [cil.ParamNode("self", 'IO')]
        f6_localVars = [cil.LocalNode("local_in_int_IO_result_0")]
        f6_intructions = [cil.ReadIntNode(f6_localVars[0].name),
                          cil.ReturnNode(f6_localVars[0].name)]
        f6 = cil.FunctionNode("function_in_int_IO",f6_params,f6_localVars,f6_intructions)

        f7_params = [cil.ParamNode("self", 'IO')]
        f7_localVars = [cil.LocalNode("local_in_string_IO_result_0")]
        f7_intructions = [cil.ReadStringNode(f7_localVars[0].name),
                          cil.ReturnNode(f7_localVars[0].name)]
        f7 = cil.FunctionNode("function_in_string_IO",f7_params,f7_localVars,f7_intructions)

        #Functions from String type
        f8_params = [cil.ParamNode("self", 'String')]
        f8_localVars = [cil.LocalNode("local_length_String_result_0")]
        f8_intructions = [cil.LengthNode(f8_localVars[0].name,f8_params[0].name),
                         cil.ReturnNode(f8_localVars[0].name)]
        f8 = cil.FunctionNode("function_length_String",f8_params,f8_localVars,f8_intructions)

        f9_params = [cil.ParamNode("self", 'String'), cil.ParamNode("word", 'String')]
        f9_localVars = [cil.LocalNode("local_concat_String_result_0")]
        f9_intructions = [cil.ConcatNode(f9_localVars[0].name,f9_params[0].name,f9_params[1].name),
                          cil.ReturnNode(f9_localVars[0].name)]
        f9 = cil.FunctionNode("function_concat_String",f9_params,f9_localVars,f9_intructions)

        f10_params = [cil.ParamNode("self", 'String'), cil.ParamNode("begin", 'Int'), cil.ParamNode("end", 'Int')]
        f10_localVars = [cil.LocalNode("local_substr_String_result_0")]
        f10_intructions = [cil.SubstringNode(f10_localVars[0].name,f10_params[0].name,f10_params[1].name,f10_params[2].name), 
                           cil.ReturnNode(f10_localVars[0].name)]
        f10 = cil.FunctionNode("function_substr_String",f10_params,f10_localVars,f10_intructions)

        f11_params = [cil.ParamNode("self", 'String')]
        f11_localVars = [cil.LocalNode("local_type_name_String_result_0")]
        f11_intructions = [cil.LoadNode(f11_localVars[0].name, 'type_String'),
                           cil.ReturnNode(f11_localVars[0].name)]
        f11 = cil.FunctionNode("function_type_name_String",f11_params,f11_localVars,f11_intructions)

        f12_params = [cil.ParamNode("self", 'String')]
        f12_localVars = [cil.LocalNode("local_copy_String_result_0")]
        f12_intructions = [cil.ConcatNode(f12_localVars[0].name, f12_params[0].name, None),
                           cil.ReturnNode(f12_localVars[0].name)]
        f12 = cil.FunctionNode("function_copy_String",f12_params,f12_localVars,f12_intructions)

        #Functions from Int type
        f13_params = [cil.ParamNode("self", 'Int')]
        f13_localVars = [cil.LocalNode("local_type_name_Int_result_0")]
        f13_intructions = [cil.LoadNode(f13_localVars[0].name, 'type_Int'),
                           cil.ReturnNode(f13_localVars[0].name)]
        f13 = cil.FunctionNode("function_type_name_Int",f13_params,f13_localVars,f13_intructions)

        f14_params = [cil.ParamNode("self", 'Int')]
        f14_localVars = [cil.LocalNode("local_copy_Int_result_0")]
        f14_intructions = [cil.AssignNode(f14_localVars[0].name, f14_params[0].name), 
                           cil.ReturnNode(f14_localVars[0].name)]
        f14 = cil.FunctionNode("function_copy_Int",f14_params,f14_localVars,f14_intructions)

        #Functions from Bool type
        f15_params = [cil.ParamNode("self", 'Bool')]
        f15_localVars = [cil.LocalNode("local_type_name_Bool_result_0")]
        f15_intructions = [cil.LoadNode(f15_localVars[0].name, 'type_Bool'),
                           cil.ReturnNode(f15_localVars[0].name)]
        f15 = cil.FunctionNode("function_type_name_Bool",f15_params,f15_localVars,f15_intructions)

        f16_params = [cil.ParamNode("self", 'Bool')]
        f16_localVars = [cil.LocalNode("local_copy_result_Bool_0")]
        f16_intructions = [cil.AssignNode(f16_localVars[0].name, f16_params[0].name), 
                           cil.ReturnNode(f16_localVars[0].name)]
        f16 = cil.FunctionNode("function_copy_Bool",f16_params,f16_localVars,f16_intructions)

        self.dotcode += [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11, f12, f13, f14, f15, f16]
        object_methods = [('abort', f1.name), ('type_name', f2.name), ('copy', f3.name)]
        string_methods = [('length', f8.name), ('concat', f9.name), ('substr', f10.name), ('type_name', f11.name), ('copy', f12.name)]
        io_methods = [('out_string', f4.name), ('out_int', f5.name), ('in_int', f6.name), ('in_string', f7.name)]
        int_methods = [('type_name', f13.name), ('copy', f14.name)]
        bool_methods = [('type_name', f15.name), ('copy', f16.name)]

        self.dottypes += [cil.TypeNode("Object", [], object_methods), 
                cil.TypeNode("IO", [], object_methods + io_methods) , 
                cil.TypeNode("String", [],  string_methods), 
                cil.TypeNode('Int', [], int_methods),
                cil.TypeNode('Bool', [], bool_methods)]

    #este metodo tiene que ver con los types de la semantica REVISAAAARRRR!
    def get_type(self, name) -> Type:
        try:
            return self.types[name]
        except KeyError:
            error_text = TypesError.TYPE_NOT_DEFINED % name
            raise TypesError(error_text)

    def check_void(self, expr):
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(expr, result))
        
        void_expr = self.define_internal_local()
        self.register_instruction(cil.LoadNode(void_expr, self.void_data))
        self.register_instruction(cil.EqualNode(result, result, void_expr))
        return result

    def sort_option_nodes_by_type(self, case_list):
        return sorted(case_list, reverse=True,
                    key=lambda x: self.context.get_depth(x.typex))

    #esto esta asociado al context que define la semantica igual que el hierarchy_types
    def get_depth(self, class_name):
        typex = self.types[class_name]
        if typex.parent is None:
            return 0
        return 1 + self.get_depth(typex.parent.name)

    def _define_unary_node(self, node, scope, cil_node):
        result = self.define_internal_local()
        expr, typex = self.visit(node.expr, scope)
        self.register_instruction(cil_node(result, expr))
        return result, typex

    def load_var_if_occupied(self, var):
        if var is not None:
            self.code.append(f'# Restore {var}')
            self.load_var_code(var)

    def save_reg_if_occupied(self, reg):
        var = self.reg_desc.get_content(reg)
        if var is not None:
            self.code.append(f'# Saving {reg} to memory')
            self.save_var_code(var)
        return var