from cmp.semantic import IntType, ObjectType, StringType, BoolType
from .ast_CIL import *
from collections import deque
from itertools import chain
from collections import OrderedDict

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
            CILMethodNode('Init_Object', 'Init_Object'),
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
        ]
        types.append(CILTypeNode('Object', [], obj_methods))
        init_Object = CILFuncNode(
            'Init_Object', 
            [CILParamNode('self', None)], 
            [], 
            [CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_Object)
        
        int_methods = [
            CILMethodNode('Init_Int', 'Init_Int'),
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
        ]
        types.append(CILTypeNode('Int', [CILAttributeNode('value', None)], int_methods))
        init_int = CILFuncNode(
            'Init_Int', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Int', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_int)
        
        str_methods = [
            CILMethodNode('Init_String', 'Init_String'), 
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
            CILMethodNode('length', 'length_String'), 
            CILMethodNode('concat', 'concat_String'),
            CILMethodNode('substr', 'substr_String'),
        ]
        types.append(CILTypeNode('String', [CILAttributeNode('value', None)], str_methods))
        init_string = CILFuncNode(
            'Init_String', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'String', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_string)
        
        bool_methods = [
            CILMethodNode('Init_Bool', 'Init_Bool'),
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
        ]
        types.append(CILTypeNode('Bool', [CILAttributeNode('value', None)], bool_methods))
        init_bool = CILFuncNode(
            'Init_Bool', 
            [CILParamNode('self', None), CILParamNode('v', None)], 
            [], 
            [CILSetAttributeNode(CILVariableNode('self'), 'Bool', CILVariableNode('value'), CILVariableNode('v')), CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_bool)
        
        io_methods = [
            CILMethodNode('Init_IO', 'Init_IO'),
            CILMethodNode('abort', 'abort_Object'), 
            CILMethodNode('type_name', 'type_name_Object'),
            CILMethodNode('copy', 'copy_Object'),
            CILMethodNode('out_string', 'out_string_IO'), 
            CILMethodNode('out_int', 'out_int_IO'),
            CILMethodNode('in_string', 'in_string_IO'),
            CILMethodNode('in_int', 'in_int_IO'),
        ]
        types.append(CILTypeNode('IO', [], io_methods))
        init_IO = CILFuncNode(
            'Init_IO', 
            [CILParamNode('self', None)], 
            [], 
            [CILReturnNode(CILVariableNode('self'))])               
        self.functions.append(init_IO)
        
        return types
        
    def create_init_class(self, attributes, locals):
        type = self.context.get_type(self.current_class)
        instructions = []
        if not isinstance(type.parent, ObjectType):
            instructions.append(CILArgNode(CILVariableNode(f'self_{self.current_class}')))
            call = CILCallNode(f'Init_{type.parent.name}')  
            instructions.append(CILAssignNode(CILVariableNode(f'self_{self.current_class}'), call))   

        for id, type, expr, inst in attributes:
            if expr is not None:
                instructions.extend(inst)
                if not isinstance(expr, CILAtomicNode):
                    variable = CILVariableNode(self.add_new_local(type))
                    instructions.append(CILAssignNode(variable, expr))
                else:   
                    variable = expr
            elif type == 'Int':
                variable = CILNumberNode(0)
            elif type == 'String':
                variable = CILVariableNode(self.add_new_local(type))
                instructions.append(CILAssignNode(variable, CILLoadNode('str_empty')))
            elif type == 'Bool':
                variable = CILVariableNode(self.add_new_local(type))
                instructions.append(CILAssignNode(variable, CILEqualsNode(CILNumberNode(0), CILNumberNode(1))))
            else:
                variable = None
            
            if variable is not None:
                instructions.append(CILSetAttributeNode(CILVariableNode(f'self_{self.current_class}'), self.current_class, CILVariableNode(id), variable)) 
        
        instructions.append(CILReturnNode(CILVariableNode(f'self_{self.current_class}')))
        locals.extend(self.all_locals.copy())
        return CILFuncNode(f'Init_{self.current_class}', [CILParamNode(f'self_{self.current_class}', None)], locals, instructions)


        
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
    heirs = {}
    visited = []
    for c in context.types.values():
        if c not in visited:
            dfs_visit_ts(context, c, list,heirs, visited)
    return list, heirs


def dfs_visit_ts(context, u, list, heirs, visited):
    visited.append(u)
    if u.parent is not None:
        try:
            heirs[u.parent.name].append(u.name)
        except KeyError:
            heirs[u.parent.name] = [u.name]

        if u.parent not in visited:
            dfs_visit_ts(context, u.parent, list, heirs, visited)
    
    list.append(u)


def bfs_init (context)  :
    table = {}
    d = {}
    d = init(context, d)
    for c in context.types.values():
        list = deque()
        list.append(c)
        visit = []        
        m = bfs( list, d.copy() , c,{})
        
        table [c.name] = m    
    return table

def bfs ( list, d ,s , m ):
    d[s.name] = 0
    while (len(list) > 0):
        u  =  list.pop()
        if u.parent is not None:
            v = u.parent
        else :
            v = None    
        while v is not None:
            if d[v.name] == -1:
                d[v.name] = d[s.name] + 1
                s = v
                list.append(v) 
                
            v = v.parent
    return d           

def init (context,d):
    for c in context.types.values():
        d [c.name] = -1
    return d     

def table (table):
    d = {}
    for k in (table.keys()):
        value = table[k]
        for c in value.keys(): 
            if  table[k][c] != -1 and table[k][c] != 0:
        
                try:
                    d [c].append((k,table[k][c])) 
                except:
                   d [c] =  [(k,table[k][c])]    
    return d 

 
def order_case_branc_to(branchs, to):
    d = {}
    string = [] 
    list = [branch.type for branch in branchs]
    for s in to :
        string.append(s.name)
    for s in string:
        try:
            d[s] =  list.index(s)
        except:
            pass    
    return d     
        
        
def valid_case (table, branchs):
    valid = {}
    for key in branchs.keys():
        try:
            s =  table[key]
        except:
            continue     
        order = sorted(s, key=lambda tu : tu[1])
        for m in order:
            try:
               valid[key].append(m)
            except:
                valid[key] = [m]
    return valid  


def return_list_valid_case(node, to, table ):
        order = order_case_branc_to(node.cases,to)
        valid = valid_case(table,order)
        s = list(valid.values())
        iterator = chain(*s)
        l = list(iterator)
        m = list(OrderedDict.fromkeys(l))
        new_cases = sorted(m, key=lambda tu : tu[1])
        return new_cases, valid         
  
            
                     
         
        
    
