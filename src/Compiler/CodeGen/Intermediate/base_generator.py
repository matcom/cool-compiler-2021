from CodeGen.Intermediate import cil
from Semantic.scope import *

class BaseCOOLToCILVisitor:
    def __init__(self):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_method = None
        self.current_function = None
        self.context = None
        self.labels = 0
        self.types_names = dict()
        self.init_attr_functions = dict()
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_local(self, vinfo):
        vinfo.name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(vinfo.name)
        self.localvars.append(local_node)
        return vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)
    
    def define_label(self):
        new_label = f'Label_{self.labels}'
        self.labels += 1
        return new_label
    
    def define_init_attr_function(self):
        function_name = f'function_initialize_{self.current_type}_attributes'
        function_node = cil.FunctionNode(function_name, [cil.ParamNode('self')], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_instruction(self, instruction):
        if self.current_function is None:
            self.instr_without_context.append(instruction)
            return instruction
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name, parent):
        data = self.register_data(name)
        self.types_names[name] = data
        type_node = cil.TypeNode(data, parent)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def fill_cil_types(self, context):
        for p in [t for t in self.dottypes]:
            p_type = context.get_type(p.name.value)
            parents = p_type.get_all_parents()
            for p_type in parents:
                for name in list(p_type.func.keys()):
                    p.methods.append((name, self.to_function_name(name, p_type.name)))
    
    
    def define_entry_function(self):
        self.current_function = self.register_function('main')        
        instance0 = self.define_internal_local()
        instance1 = self.define_internal_local()
        result = self.define_internal_local()
        ret = self.define_internal_local()
        main_method_name = self.to_function_name('main', 'Main')
        self.register_instruction(cil.AllocateNode('type_Main', instance0))
        self.register_instruction(cil.ArgNode(instance0))
        self.register_instruction(cil.StaticCallNode('function_initialize_Main_attributes', instance1))
        self.register_instruction(cil.ArgNode(instance1))
        self.register_instruction(cil.StaticCallNode(main_method_name, result))
        self.register_instruction(cil.EndProgramNode())
        self.current_function = None
        
    ##################################################################################################################
    #  PREDEFINED     TYPES
    ##################################################################################################################
    
    def predefined_types(self):
        self.register_io_type()
        self.register_object_type()
        self.register_string_type()
        self.register_int_type()
        self.register_bool_type()
        self.register_void_type()
        # ... add more
    
    #=================================================================================================================
    
    def register_io_type(self):
        self.current_type = self.context.ctype.IO
        _type = self.register_type(self.current_type.name, 'Object')
        _type.attributes = [v for v in self.current_type.get_all_attr()]
        _type.methods = [(f, self.to_function_name(f, 'IO')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    
    def register_object_type(self):
        self.current_type = self.context.ctype.OBJECT
        _type = self.register_type(self.current_type.name, None)
        _type.attributes = [v for v in self.current_type.get_all_attr()]
        _type.methods = [(f, self.to_function_name(f, 'Object')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    
    def register_string_type(self):
        self.current_type = self.context.ctype.STRING
        _type = self.register_type(self.current_type.name, 'Object')
        _type.attributes = [v for v in self.current_type.get_all_attr()] + ["value"]
        _type.methods = [(f, self.to_function_name(f, 'String')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    
    def register_int_type(self):
        self.current_type = self.context.ctype.INT
        _type = self.register_type(self.current_type.name, 'Object')
        _type.attributes = [v for v in self.current_type.get_all_attr()] + ["value"]
        _type.methods = [(f, self.to_function_name(f, 'Int')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    
    def register_bool_type(self):
        self.current_type = self.context.ctype.BOOL
        _type = self.register_type(self.current_type.name, 'Object')
        _type.attributes = [v for v in self.current_type.get_all_attr()] + ["value"]
        _type.methods = [(f, self.to_function_name(f, 'Bool')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    
    def register_void_type(self):
        self.current_type = self.context.ctype.VOID
        _type = self.register_type(self.current_type.name, 'Object')
        _type.attributes = [v for v in self.current_type.get_all_attr()]
        _type.methods = [(f, self.to_function_name(f, 'Void')) for f in self.current_type.get_all_func()]
        self.current_function = self.define_init_attr_function()
        self.register_instruction(cil.ReturnNode('self'))
        self.current_function = None
        self.current_type = None
    