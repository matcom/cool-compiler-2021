from cmp.semantic import ObjectType
from .ast_CIL import *


class CILScope:
    def __init__(self, context):
        self.context = context
        
        self.if_count = 0
        self.case_count = 0
        self.variables_count = 0
        self.str_count = 0
        self.loop_count = 0
        
        self.locals = [{}]
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
        
        obj_methods = [
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
            CILMethodNode('init', 'init_Object'),
        ]
        types.append(CILTypeNode('Object', [], obj_methods))
        init_Object = CILFuncNode(
            'init_Object', 
            [CILParamNode('self', None)], 
            [], 
            [CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_Object)
        
        int_methods = obj_methods.copy()
        int_methods.extend([CILMethodNode('init', 'init_Int')])
        types.append(CILTypeNode('Int', [CILAttributeNode('value', None)], int_methods))
        init_int = CILFuncNode(
            'init_Int', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Int', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_int)
        
        str_methods = obj_methods.copy()
        str_methods.extend([
            CILMethodNode('init', 'init_String'), 
            CILMethodNode('length', 'length_String'), 
            CILMethodNode('concat', 'concat_String'),
            CILMethodNode('substr', 'substr_String'),
        ])
        types.append(CILTypeNode('String', [CILAttributeNode('value', None)], str_methods))
        init_string = CILFuncNode(
            'init_String', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'String', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_string)
        
        bool_methods = obj_methods.copy()
        bool_methods.extend([CILMethodNode('init', 'init_Bool')])
        types.append(CILTypeNode('Bool', [CILAttributeNode('value', None)], bool_methods))
        init_bool = CILFuncNode(
            'init_Bool', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Bool', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_bool)
        
        io_methods = obj_methods.copy()
        io_methods.extend([
            CILMethodNode('out_string', 'out_string_IO'), 
            CILMethodNode('out_int', 'out_int_IO'),
            CILMethodNode('in_string', 'in_string_IO'),
            CILMethodNode('in_int', 'in_int_IO'),
        ])
        types.append(CILTypeNode('IO', [], io_methods))
        init_IO = CILFuncNode(
            'init_IO', 
            [CILParamNode('self', None)], 
            [], 
            [CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_IO)
        
        return types
        
    def create_init_class(self, attributes, expresions):
        type = self.context.get_type(self.current_class)
        instructions = []
        
        if not isinstance(type.parent,ObjectType):
            instructions.append(CILArgNode(CILVariableNode(f'self')))
            call = CILVCallNode(type.parent.name, f'init')  
            instructions.append(CILAssignNode(CILVariableNode('self'), call))   
                     
        for attr, (expr, type) in zip(attributes, expresions):
            if not isinstance(expr, CILAtomicNode):
                variable = CILVariableNode(self.add_new_local(type))
                self.instructions.append(CILAssignNode(variable, expr))
            else:   
                variable = CILVariableNode(expr.lex)
                
            instructions.append(CILSetAttributeNode(CILVariableNode('self'), self.current_class, CILVariableNode(attr), variable)) 
        
        instructions.append(CILReturnNode(CILVariableNode('self')))
        
        return CILFuncNode(f'init_{self.current_class}', [CILParamNode('self', None)], [], instructions)
        
        
class TypeInfo:
    def __init__(self):
        self.attrs = []
        self.methods = {}
        
    def __repr__(self):
        text = str(self.attrs) + '\n'
        text += str(self.methods) + '\n'
        return text
        
            
def get_ts(context):
    list = []
    visited = []
    for c in context.types.values():
        if c not in visited:
            dfs_visit_ts(context, c, list, visited)
    return list


def dfs_visit_ts(context, u, list, visited):
    visited.append(u)
    if u.parent is not None and u.parent not in visited:
        dfs_visit_ts(context, u.parent, list, visited)
    
    list.append(u)