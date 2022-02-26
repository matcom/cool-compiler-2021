import cool.cil_builder.cil_ast as cil
from cool.Parser.AstNodes import *
from cool.semantic import visitor
from cool.utils.Errors.semantic_errors import *
from cool.semantic.semantic import *

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.current_type_dir = None
        self.type_node_dict = {}
        self.dottype_dict = {}
        self.type_tree = {}
        self.context = context
        self.label_id = 0
        self.tag_id = 0
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions

    def register_param(self,vinfo):
        vinfo.name = f'{vinfo.name}'
        param_node = cil.ParamCilNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name
    
    def is_in_actual_params(self,param_name):
        return f'param_{param_name}' in (param.name for param in self.params)


    def register_local(self, vinfo,scope = None):
        cool_name = vinfo.name
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalCilNode(vinfo.name)
        self.localvars.append(local_node)
        if scope is not None:
            scope.define_cil_local(cool_name,vinfo.name)
        return vinfo.name

    def define_internal_local(self,scope = None):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo,scope)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionCilNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeCilNode(name)
        self.dottypes.append(type_node)
        self.dottype_dict[name] = type_node
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataCilNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def fill_cil_types(self,type_name):
        try:
            object_type_childs = self.type_tree[type_name]

            for child in object_type_childs:
                new_methods = self.fill_cil_types_(child.name)
                self.dottype_dict[child.name].methods = new_methods
                self.fill_cil_types(child.name)
        
        except KeyError:
            pass

    
    def fill_cil_types_(self,type_):
        dot_type = self.dottype_dict[type_]
        type_name = dot_type.name
        parent_type = self.context.get_type(type_name).parent
        parent_name = parent_type.name
        dot_parent = self.dottype_dict[parent_name]

        new_method_list = []

        for (old_methName,new_methName) in dot_parent.methods:
            #Tener acceso a los nuevos nombres
            method_original = {}
            for method in dot_type.methods:
                method_original[method[0]] = method[1]

            if old_methName in (method[0] for method in dot_type.methods):
                new_method_list.append((old_methName,method_original[old_methName]))
            else:
                new_method_list.append((old_methName,new_methName))
        for method_touple in dot_type.methods:
            if method_touple not in new_method_list:
                new_method_list.append(method_touple)
        return new_method_list

    def create_label(self):
        self.label_id += 1
        return f'label{self.label_id}'

    def create_tag(self):
        self.tag_id += 1
        return self.tag_id - 1

    def get_parentAttr_declarations(self,programNode):
        for classNode in programNode.declarations:
            class_type = self.context.get_type(classNode.id)
            attr_list = self.put_attr_on_type(class_type)

            classNode.features = attr_list + classNode.features

                

    def put_attr_on_type(self,type_):
        parent_ = self.context.get_type(type_.name).parent
        
        if parent_.name == 'Object' or parent_.name == 'IO':
            return []
        else:
            list_attr = self.type_node_dict[parent_.name]
            return self.put_attr_on_type(parent_)+list_attr
            
            

    def generateTree(self):
        classList = {}
        for classNode in self.context.types.values():
            if classNode.name == 'Error':
                continue
            if classNode.parent is not None:
                try:
                    classList[classNode.parent.name].append(classNode)
                except KeyError:
                    classList[classNode.parent.name] = [classNode]
        return classList

    def enumerateTypes(self):
        parentTree = self.generateTree()
        self.context.types['Object'].class_tag = self.create_tag()
        for Node in parentTree.values():
            for child in Node:
                child.class_tag = self.create_tag()

    def set_default_values(self,node):
        class_dir = self.current_type_dir
        if node.type == 'Int':
            int_internal = self.define_internal_local()
            result_location = self.define_internal_local()
            self.register_instruction(cil.IntCilNode(0,int_internal))
            self.register_instruction(cil.AllocateCilNode('Int',result_location))
            self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result_location,int_internal],result_location))
            self.register_instruction(cil.SetAttribCilNode(class_dir,self.current_type.name,node.id,result_location))
        elif node.type == 'String':
            result_location = self.define_internal_local()
            data_location = self.define_internal_local()
            len_str = self.define_internal_local()
            self.register_instruction(cil.AllocateCilNode('String',result_location)) #Creo el espacio en memoria para guardar el String (Method_dir,String_value,Length)
            self.register_instruction(cil.GetDataCilNode('empty_str_data',data_location)) #Paso al sp en una local interna el data
            self.register_instruction(cil.IntCilNode(0,len_str))
            self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result_location,data_location,len_str],result_location)) #LLamo al init del string y lo relleno con los valores que se calcularon de: [Direccion de string val],  [Len del string] 
            self.register_instruction(cil.SetAttribCilNode(class_dir,self.current_type.name,node.id,result_location))
        elif node.type == 'Bool':
            bool_internal = self.define_internal_local()
            result_location = self.define_internal_local()
            self.register_instruction(cil.IntCilNode(0,bool_internal))
            self.register_instruction(cil.AllocateCilNode('Bool',result_location))
            self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result_location,bool_internal],result_location))
            self.register_instruction(cil.SetAttribCilNode(class_dir,self.current_type.name,node.id,result_location))
        else:
            void_location = self.define_internal_local()
            self.register_instruction(cil.GetDataCilNode('void_data',void_location))
            self.register_instruction(cil.SetAttribCilNode(class_dir,self.current_type.name,node.id,void_location))


    def fill_builtin(self):
        built_in_types = [
            self.context.get_type('Object'),
            self.context.get_type('IO'),
            self.context.get_type('Int'),
            self.context.get_type('String'),
            self.context.get_type('Bool')]
        for t in built_in_types:
            cilType = self.register_type(t.name)
            cilType.methods = [(m,self.to_function_name(m,t.name)) for m in t.methods]
            if cilType.name in ['Int','String','Bool']:
                cilType.attributes.append('value')
                if cilType.name == 'String':
                    cilType.attributes.append('len')


        #=============================Object=========================================
        self.current_type = self.context.get_type('Object')

        #INIT_Object
        self.current_function = self.register_function('INIT_Object')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        self.register_instruction(cil.ReturnCilNode(self_param))

        #function abort
        self.current_function = self.register_function(self.to_function_name('abort',self.current_type.name))
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        self.register_instruction(cil.AbortCilNode(self_param))
        self.register_instruction(cil.ReturnCilNode())

        #function type_name
        self.current_function = self.register_function(self.to_function_name('type_name',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        result = self.define_internal_local()
        adress = self.define_internal_local()
        self.register_instruction(cil.TypeNameCilNode(param_self,adress))
        self.register_instruction(cil.AllocateCilNode('String',result))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result,adress],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #function copy
        self.current_function = self.register_function(self.to_function_name('copy',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        result = self.define_internal_local()
        self.register_instruction(cil.CopyCilNode(param_self,result))
        self.register_instruction(cil.ReturnCilNode(result))
        
        #=========================Int=========================================
        self.current_type = self.context.get_type('Int')
        
        #INIT_Int
        self.current_function = self.register_function('INIT_Int')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('value',self.current_type.name))
        self.register_instruction(cil.SetAttribCilNode(self_param,'Int','value', param1))
        self.register_instruction(cil.ReturnCilNode(self_param))

        #=========================String=========================================
        self.current_type = self.context.get_type('String')

        #INIT_String
        self.current_function = self.register_function('INIT_String')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        param1_data = self.register_param(VariableInfo('value',self.current_type.name))
        param2_len = self.register_param(VariableInfo('len',self.current_type.name))

        self.register_instruction(cil.SetAttribCilNode(self_param,'String','value',param1_data))
        self.register_instruction(cil.SetAttribCilNode(self_param,'String','len',param2_len))
        self.register_instruction(cil.ReturnCilNode(self_param))

        #function length
        self.current_function = self.register_function(self.to_function_name('length',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        len_value = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribCilNode(param_self,'String','len',len_value))
        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,len_value],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #function INIT_length
        self.current_function = self.register_function('INIT_length')
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthCilNode(param_self,result))
        self.register_instruction(cil.ReturnCilNode(result))

        #function concat
        self.current_function = self.register_function(self.to_function_name('concat',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('var2',self.current_type.name))
        result = self.define_internal_local()
        dir_concat = self.define_internal_local()
        len_value = self.define_internal_local()
        self.register_instruction(cil.AllocateCilNode('String',result))
        self.register_instruction(cil.ConcatCilNode(param_self,param1,dir_concat))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_length',[dir_concat],len_value))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result,dir_concat,len_value],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #function substr
        self.current_function = self.register_function(self.to_function_name('substr',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('param1','Int'))
        param2 = self.register_param(VariableInfo('param2','Int'))
        result = self.define_internal_local()
        dir_subs = self.define_internal_local()
        len_value = self.define_internal_local()

        self.register_instruction(cil.AllocateCilNode('String',result))
        self.register_instruction(cil.SubstringCilNode(param_self,param1,param2,dir_subs))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_length',[dir_subs],len_value))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result,dir_subs,len_value],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #=========================Bool=========================================
        self.current_type = self.context.get_type('Bool')
        # INIT_Bool
        self.current_function = self.register_function('INIT_Bool')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('value',self.current_type.name))
        self.register_instruction(cil.SetAttribCilNode(self_param,'Bool','value', param1))
        self.register_instruction(cil.ReturnCilNode(self_param))

        #=========================IO=========================================
        self.current_type = self.context.get_type('IO')
        #INIT_IO
        self.current_function = self.register_function('INIT_IO')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        self.register_instruction(cil.ReturnCilNode(self_param))

        #function out_string
        self.current_function = self.register_function(self.to_function_name('out_string',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('param1',self.context.get_type('String')))
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribCilNode(param1,'String','value',result))
        self.register_instruction(cil.PrintStringCilNode(result))
        self.register_instruction(cil.ReturnCilNode(param_self))

        #function out_int
        self.current_function = self.register_function(self.to_function_name('out_int',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        param1 = self.register_param(VariableInfo('param1',self.context.get_type('Int')))
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribCilNode(param1,'Int','value',result))
        self.register_instruction(cil.PrintIntCilNode(result))
        self.register_instruction(cil.ReturnCilNode(param_self))

        #function in_int
        self.current_function = self.register_function(self.to_function_name('in_int',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        result = self.define_internal_local()
        input_int = self.define_internal_local()
        self.register_instruction(cil.ReadIntCilNode(input_int))
        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,input_int],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #function in_string
        self.current_function = self.register_function(self.to_function_name('in_string',self.current_type.name))
        param_self = self.register_param(VariableInfo('self',self.current_type.name))
        result = self.define_internal_local()
        data_aux_location = self.define_internal_local()
        len_input_str = self.define_internal_local()
        self.register_instruction(cil.ReadStringCilNode(data_aux_location))
        self.register_instruction(cil.StaticCallCilNode('String','INIT_length',[data_aux_location],len_input_str))

        self.register_instruction(cil.AllocateCilNode('String',result))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_String',[result,data_aux_location,len_input_str],result))
        self.register_instruction(cil.ReturnCilNode(result))

        #Limpiar Todo
        self.current_type = None
        self.current_function = None
        self.current_method = None


class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        self.current_function = self.register_function('entry')
        instance = self.define_internal_local(scope)
        result = self.define_internal_local(scope)
        self.register_instruction(cil.AllocateCilNode('Main', instance))
        self.register_instruction(cil.StaticCallCilNode('Main','INIT_Main',[instance],instance))
        self.register_instruction(cil.StaticCallCilNode('Main','main',[instance], result))
        self.register_instruction(cil.ReturnCilNode(0))
        self.fill_builtin()

        for declaration in node.declarations:
            self.type_node_dict[declaration.id] = [dec for dec in declaration.features if isinstance(dec,AttrDeclarationNode)]
        
        self.get_parentAttr_declarations(node)


        for declaration, child_scope in zip(node.declarations, scope.children):
            self.visit(declaration, child_scope)


        # self.enumerateTypes() 

        self.type_tree = self.generateTree()
        self.fill_cil_types('Object')
        self.current_function = None

        return cil.ProgramCilNode(self.dottypes, self.dotdata, self.dotcode)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        
        self.current_type = self.context.get_type(node.id)
        self.current_type.tag = len(self.dottypes)
        cil_type = self.register_type(node.id)
        cil_type.attributes = [v.name for (v,_) in self.current_type.all_attributes()]


        #Register INIT_Class Function
        self.current_function = self.register_function(f'INIT_{self.current_type.name}')
        self_param = self.register_param(VariableInfo('self',self.current_type.name))
        self.current_type_dir = self_param

        attr_list =[attr for attr in node.features if isinstance(attr,AttrDeclarationNode)]
        for attr in attr_list:
            self.visit(attr,scope)

        self.register_instruction(cil.ReturnCilNode(self_param))

        self.current_function = None
        #End register INIT_Class Function


        func_declarations = [f for f in node.features if isinstance(f, FuncDeclarationNode)]
        for feature, child_scope in zip(func_declarations, scope.children):
            value = self.visit(feature,scope.create_child())
        

        self.current_type = None

                
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        self.current_method = self.current_type.get_method(node.id)

        function_name = self.to_function_name(node.id,self.current_type.name)
        self.dottypes[-1].methods.append((node.id,function_name))
        self.current_function = self.register_function(function_name)

        self.register_param(VariableInfo('self',self.current_type.name))
        for param in node.params:
            self.register_param(VariableInfo(f'param_{param.id}',param.type))
        value = self.visit(node.body, scope)

        self.register_instruction(cil.ReturnCilNode(value))
        self.current_method = None

        return self.current_function

    @visitor.when(AttrDeclarationNode)
    def visit(self,node,scope):
        ###############################################
        # node.id = str
        # node.type = str
        # node.expr = ExpressionNode
        #################################################
        if node.expr is not None:
            result = self.visit(node.expr,scope)
            self.register_instruction(cil.SetAttribCilNode('self',self.current_type.name,node.id,result))
        else:
            self.set_default_values(node)


    @visitor.when(ConstantNumNode) #7.1 Constant
    def visit(self, node,scope):
        ###############################
        # node.lex -> str
        ###############################
        int_internal = self.define_internal_local()
        result_location = self.define_internal_local()

        self.register_instruction(cil.AllocateCilNode('Int',result_location))
        self.register_instruction(cil.IntCilNode(int(node.lex),int_internal))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result_location,int_internal],result_location))

        return result_location

    @visitor.when(StringNode) #7.1 Constant
    def visit(self, node,scope):
    ###############################
    # node.lex -> str
    ###############################
        returnVal = self.define_internal_local()
        result_location = self.define_internal_local()

        data_location = self.define_internal_local()
        length_str = self.define_internal_local()

        data_name = self.register_data(node.lex)
        self.register_instruction(cil.AllocateCilNode('String',result_location)) #Creo el espacio en memoria para guardar el String (Method_dir,String_value,Length)
        self.register_instruction(cil.GetDataCilNode(data_name.name,data_location)) #Paso al sp en una local interna el data
        self.register_instruction(cil.StaticCallCilNode('String','INIT_length',[data_location],length_str)) #Call a length usando lo que cargue de data como selfy dejando el resultado en lenght_str
        self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result_location,data_location,length_str],returnVal)) #LLamo al init del string y lo relleno con los valores que se calcularon de: [Direccion de string val],  [Len del string] 
        return result_location

    @visitor.when(BooleanNode) #7.1 Constant
    def visit(self, node,scope):
        ###############################
        # node.lex -> str
        ###############################
        int_internal = self.define_internal_local()
        result_location = self.define_internal_local()

        self.register_instruction(cil.AllocateCilNode('Bool',result_location))
        if node.lex == 'true':
            self.register_instruction(cil.IntCilNode(1,int_internal))
        elif node.lex == 'false':
            self.register_instruction(cil.IntCilNode(0,int_internal))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result_location,int_internal],result_location))

        return result_location

    

    @visitor.when(VariableNode) #7.2 Identifiers
    def visit(self, node,scope):
        ###############################
        # node.lex -> str
        ###############################
        if scope.is_cil_defined(node.lex):
            cool_var = scope.find_cil_variable(node.lex)
            self.register_local(VariableInfo(cool_var,None))
            return cool_var
        elif f'param_{node.lex}' in [param_nodes.name for param_nodes in self.params]:
            return f'param_{node.lex}'
        else:
            new_local = self.define_internal_local()
            self.register_instruction(cil.GetAttribCilNode('self',self.current_type.name,node.lex,new_local))
            return new_local


    @visitor.when(AssignNode) #7.3 Assignement
    def visit(self, node,scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        source = self.visit(node.expr,scope)
        local_var = scope.find_cil_variable(node.id)
        if local_var is not None: #local
            dest = local_var
            self.register_instruction(cil.AssignCilNode(dest,source))
        elif self.is_in_actual_params(node.id): #param
            dest = f'param_{node.id}'
            self.register_instruction(cil.AssignCilNode(dest,source))
        else: #attribute
            self.register_instruction(cil.SetAttribCilNode('self',self.current_type.name,node.id,source))
            dest = node.id
            
        return source

    @visitor.when(CallNode) #7.4 Dispatch
    def visit(self, node, scope):
        ###############################
        #node.obj = ExpressionNode
        #node.id = str
        #node.args = args
        #node.parent = Type
        ###############################
        result = self.define_internal_local()
        arg_list = []

        for a in (node.args):
            method_arg = self.visit(a,scope)
            arg_list.append(method_arg)

        if node.call_type == 2 or ( hasattr(node.obj,'lex') and node.obj.lex == 'self' and node.call_type != 3) :

            arg_list.insert(0,'self')
            self.register_instruction(cil.StaticCallCilNode(self.current_type.name,node.id,arg_list,result))
        else:
            expresion = self.visit(node.obj,scope)
            # arg_list.append(expresion)
            if node.call_type == 1:
                self.register_instruction(cil.DynamicCallCilNode(expresion,node.obj.computed_type.name,node.id,[expresion]+arg_list,result))
            else:
                self.register_instruction(cil.DynamicParentCallCilNode(expresion,node.parent,node.id,[expresion]+arg_list,result))

        return result

    @visitor.when(IfNode) #7.5 Conditional
    def visit(self,node,scope):
        ###############################
        #node.ifexp = ExpressionNode
        #node.elseexp = ExpressionNode
        #node.thenexp = ExpressionNode
        ###############################
        result = self.define_internal_local()
        condition = self.visit(node.ifexp,scope)
        then_label = self.create_label()
        end_label = self.create_label()

        self.register_instruction(cil.GotoIfCilNode(condition,then_label))
        else_result = self.visit(node.elseexp,scope)
        self.register_instruction(cil.AssignCilNode(result,else_result))
        self.register_instruction(cil.GotoCilNode(end_label))

        self.register_instruction(cil.LabelCilNode(then_label))
        then_result = self.visit(node.thenexp,scope)
        self.register_instruction(cil.AssignCilNode(result,then_result))
        self.register_instruction(cil.LabelCilNode(end_label))

        return result 

    @visitor.when(WhileNode) #7.6 Loop
    def visit(self,node,scope):
        ###############################
        # node.condition = ExpressionNode
        # node.body = ExpressionNode
        ###############################
        result_while = self.define_internal_local()
        label_start = self.create_label()
        label_end = self.create_label()
        self.register_instruction(cil.LabelCilNode(label_start))
        if_result = self.visit(node.condition,scope)
        self.register_instruction(cil.NotGotoIfCilNode(if_result,label_end))
        self.visit(node.body,scope)
        self.register_instruction(cil.GotoCilNode(label_start))
        self.register_instruction(cil.LabelCilNode(label_end))

        self.register_instruction(cil.GetDataCilNode('void_data',result_while))
        return result_while



    @visitor.when(ExpressionGroupNode) #7.7 Blocks
    def visit(self, node, scope):
        ###############################
        # node.body -> ExpressionNode
        ###############################
        for expression in node.body:
            value = self.visit(expression,scope)
        return value

    @visitor.when(LetNode) #7.8 Let Node 
    def visit(self, node, scope):
        ###############################
        # node.params = [DeclarationNode]
        # node.body = ExpresionNode
        ###############################
        child_scope = scope.create_child()
        for let_local in node.params:
            self.visit(let_local,child_scope)
        #In Expression
        result = self.visit(node.body,child_scope)
        return result

    @visitor.when(LetDeclarationNode) #7.8 Let Node 
    def visit(self, node, scope):
        ###############################
        # node.id = str
        # node.type = Type
        # node.expr = ExpresionNode
        ###############################
        if node.expr is not None:
            expr_result = self.visit(node.expr,scope)
            var_created = self.register_local(VariableInfo(node.id,node.type),scope)
            self.register_instruction(cil.AssignCilNode(var_created,expr_result))
        else:
            var_created = self.register_local(VariableInfo(node.id,node.type),scope)
            if node.type == 'Int':
                int_internal = self.define_internal_local()
                result_location = self.define_internal_local()
                self.register_instruction(cil.IntCilNode(0,int_internal))
                self.register_instruction(cil.AllocateCilNode('Int',result_location))
                self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result_location,int_internal],result_location))
            elif node.type == 'String':
                result_location = self.define_internal_local()
                data_location = self.define_internal_local()
                len_str = self.define_internal_local()
                self.register_instruction(cil.AllocateCilNode('String',result_location)) #Creo el espacio en memoria para guardar el String (Method_dir,String_value,Length)
                self.register_instruction(cil.GetDataCilNode('empty_str_data',data_location)) #Paso al sp en una local interna el data
                self.register_instruction(cil.IntCilNode(0,len_str))
                self.register_instruction(cil.StaticCallCilNode('String','INIT_String',[result_location,data_location,len_str],result_location)) #LLamo al init del string y lo relleno con los valores que se calcularon de: [Direccion de string val],  [Len del string] 
            elif node.type == 'Bool':
                bool_internal = self.define_internal_local()
                result_location = self.define_internal_local()
                self.register_instruction(cil.IntCilNode(0,bool_internal))
                self.register_instruction(cil.AllocateCilNode('Bool',result_location))
                self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result_location,bool_internal],result_location))
            else:
                result_location = self.define_internal_local()
                self.register_instruction(cil.GetDataCilNode('void_data',result_location))

            self.register_instruction(cil.AssignCilNode(var_created,result_location))
        return var_created



    @visitor.when(CaseNode) #7.9 Case Node 
    def visit(self, node, scope):
        ###############################
        # node.case = ExpresionNode
        # node.body = [Expression Node]
        ###############################
        expresionLabel_list = []

        result_expr_branch = self.define_internal_local() #Resultado del expr_k del branch que se va a ejecutar
        best_address = self.define_internal_local() #adress del INIT_method del menor type_k tal que type_k >= expr_0.Type()
        comparison_result = self.define_internal_local() #Booleano que representa si el type_i actual = al menor type_k
        actual_address = self.define_internal_local() #address actual que reviso
        label_end = self.create_label() 

        expr_result = self.visit(node.case,scope)
        self.register_instruction(cil.CaseCilNode(expr_result))


        #Revisar tipos primero y quedarme con el menor Tipe P tal que P >= C
        for (i,expr_node) in enumerate(node.body):
            expresionLabel_list.append(self.create_label())
            self.register_instruction(cil.BranchCilNode(f'{expr_node.type}_methods'))

        self.register_instruction(cil.CaseEndCilNode(best_address))




        for i,arg in enumerate(node.body):
            label_i = expresionLabel_list[i]
            self.register_instruction(cil.GetDataCilNode(f'{arg.type}_methods',actual_address))
            self.register_instruction(cil.EqualCilNode(comparison_result,best_address,actual_address))
            self.register_instruction(cil.GotoBoolIfCilNode(comparison_result,label_i))

        #Ejecutar a isntruccion correspondiente
        for (i,expr_node) in enumerate(node.body):
            child_scope = scope.create_child()
            self.register_instruction(cil.LabelCilNode(expresionLabel_list[i]))

            var_expresion = self.register_local(VariableInfo(expr_node.id,expr_node.type),child_scope)
            # self.register_instruction(cil.AllocateCilNode(expr_node.type,var_branch_location))
            # self.register_instruction(cil.InternalCopyCilNode(expr_result,var_branch_location))
            self.register_instruction(cil.AssignCilNode(var_expresion,expr_result))
            
            body_node_result = self.visit(expr_node.expr,child_scope)
            self.register_instruction(cil.AssignCilNode(result_expr_branch,body_node_result))
            self.register_instruction(cil.GotoCilNode(label_end))
        
        self.register_instruction(cil.LabelCilNode(label_end))
        return result_expr_branch

    @visitor.when(VarDeclarationNode) #Case Node
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        result = self.visit(node.expr,scope)
        return result 

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)

        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.PlusCilNode(dest,left,right))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,dest],result))
        return result

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()
        result_fun = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.MinusCilNode(dest,left,right))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,dest],result))
        return result

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)
        
        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.StarCilNode(dest,left,right))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,dest],result))
        return result

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)

        self.register_instruction(cil.DivCilNode(dest,left,right))
        self.register_instruction(cil.AllocateCilNode('Int',result))
        self.register_instruction(cil.StaticCallCilNode('Int','INIT_Int',[result,dest],result))
        return result


    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)

        if node.left.computed_type.name == 'String':
            self.register_instruction(cil.CompareStringCilNode(dest,left,right))
        elif node.left.computed_type.name in ['Int', 'Bool']:
            self.register_instruction(cil.EqualCilNode(dest,left,right))
        else:
            self.register_instruction(cil.EqualRefCilNode(dest,left,right))        
    
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))

        return result

    @visitor.when(LessEqual)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)

        self.register_instruction(cil.LessEqualCilNode(dest,left,right))
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))
        return result

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        left = self.visit(node.left,scope)
        right = self.visit(node.right,scope)

        self.register_instruction(cil.LessCilNode(dest,left,right))
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))
        return result

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        ###############################
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        right = self.visit(node.right,scope)

        self.register_instruction(cil.IsVoidCilNode(dest,right))
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))
        return result

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        right = self.visit(node.right,scope)

        self.register_instruction(cil.NotCilNode(dest,right))
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))
        return result

    @visitor.when(NegateNode)
    def visit(self, node, scope):
        ###############################
        # node.right -> ExpressionNode
        ###############################
        dest = self.define_internal_local()
        result = self.define_internal_local()

        right = self.visit(node.right,scope)

        self.register_instruction(cil.NegateCilNode(dest,right))
        self.register_instruction(cil.AllocateCilNode('Bool',result))
        self.register_instruction(cil.StaticCallCilNode('Bool','INIT_Bool',[result,dest],result))
        return result



    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        allocate_dir = self.define_internal_local()
        result = self.define_internal_local()
        self.register_instruction(cil.AllocateCilNode(node.lex,allocate_dir))
        self.register_instruction(cil.StaticCallCilNode(self.current_type.name,f'INIT_{node.lex}',[allocate_dir],result))
        return allocate_dir