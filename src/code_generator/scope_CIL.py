from .ast_CIL import *


class CILScope:
    def __init__(self, context):
        self.context = context
        
        self.if_count = 0
        self.case_count = 0
        self.variables_count = 0
        self.str_count = 0
        self.loop_count = 0
        
        self.locals = []
        self.all_locals = []
        self.instructions = []
        self.data = []
        self.functions = []
        self.current_class = ""
         
    def add_local(self, id, type, is_param = False):
        local_dict = self.locals[-1] 
        if id in local_dict.keys():
            nickname = local_dict[id].id
            local_dict[id] = CILLocalNode(nickname, type) 
        else:
            nickname = f'{id}_{self.variables_count}'
            self.variables_count += 1
            node = CILLocalNode(nickname, type)
            local_dict[id] = node
            
            if not is_param:
                self.all_locals.append(node)
                
        return nickname
                
    def add_new_local(self, type):
        local_dict = self.locals[-1] 
        name = f't_{self.variables_count}'
        self.variables_count += 1
        node = CILLocalNode(name, type)
        local_dict[name] = node
        self.all_locals.append(node)
        return name
    
    def find_local(self, id):
        for i in range (len(self.locals) - 1 , -1, -1):
            d = self.locals[i]
            try:
                return d[id]
            except:
                pass
        return None

    def find_data(self, id):
        for d in self.data:
            if d.id == id:
                return d
        return None

    def ret_type_of_method(self, name_meth, name_class):
        type_class = self.context.get_type(name_class)
        method = type_class.get_method(name_meth)
        return method.return_type.name

    def create_builtin_types(self):
        types = []
        
        int_methods = [
            CILMethodNode('init', 'init_Int'),
        ]
        types.append(CILTypeNode('Int', [CILAttributeNode('value', None)], int_methods))
        init_int = CILFuncNode(
            'init_Int', 
            [CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Int', CILVariableNode('value'), CILVariableNode('v'))])               
        self.functions.append(init_int)
        
        str_methods = [
            CILMethodNode('init', 'init_String'), 
            CILMethodNode('length', 'length'), 
            CILMethodNode('concat', 'concat'),
            CILMethodNode('substr', 'substr'),
        ]
        types.append(CILTypeNode('String', [CILAttributeNode('value', None)], str_methods))
        init_string = CILFuncNode(
            'init_String', 
            [CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'String', CILVariableNode('value'), CILVariableNode('v'))])               
        self.functions.append(init_string)
        
        bool_methods = [
            CILMethodNode('init', 'init_Bool'),
        ]
        types.append(CILTypeNode('Bool', [CILAttributeNode('value', None)], bool_methods))
        bool_string = CILFuncNode(
            'init_Bool', 
            [CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Bool', CILVariableNode('value'), CILVariableNode('v'))])               
        self.functions.append(bool_string)
               
        obj_methods = [
            CILMethodNode('abort', 'abort'), 
            CILMethodNode('type_name', 'type_name'),
            CILMethodNode('copy', 'copy'),
        ]
        types.append(CILTypeNode('Object', [], obj_methods))
        
        io_methods = [
            CILMethodNode('out_string', 'out_string'), 
            CILMethodNode('out_int', 'out_int'),
            CILMethodNode('in_string', 'in_string'),
            CILMethodNode('in_int', 'in_int'),
        ]
        types.append(CILTypeNode('IO', [], io_methods))
        
        return types
        
    #pending 
    def create_init_class(attributes, expresions):
        for attr,expr in zip(attributes,expresions):
            assig = CILAssignNode (attr.id,expr)