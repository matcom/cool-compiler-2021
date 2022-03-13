from utils import ast_nodes as ast
from utils import visitor
from .semantic import Type

class CollectDeclarationsDict(object):
    def __init__(self, dict_attr, dict_method, context):
        self.dict_attr = dict_attr
        self.dict_method = dict_method
        self.context = context
        self.initialize_types()
    
    def initialize_types(self):
        io = self.context.get_type('IO')
        self.dict_attr[io] = []
        
        self.dict_method[io] = [ 
            ('out_string'), 
            ('out_int'), 
            ('in_string'), 
            ('in_int')
        ]
        
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode):
        for item in node.class_list:
            self.visit(item)
 
    @visitor.when(ast.ClassDecNode)
    def visit(self, node: ast.ClassDecNode):
        class_type = self.context.get_type(node.name)
        self.dict_attr[class_type] = []
        self.dict_method[class_type] = []
        for dec in node.data:
            if isinstance(dec, ast.AttributeDecNode):
                self.dict_attr[class_type].append(dec)
            if isinstance(dec, ast.MethodDecNode):
                self.dict_method[class_type].append(dec)


def get_declarations_dict(t_dict_attr, t_dict_method):
    dict_attr, dict_method = {}, {}
    for item in t_dict_attr:
        dict_attr[item] = [i for i in t_dict_attr[item]]

    for item in t_dict_method:
        dict_method[item] = [i for i in t_dict_method[item]]
        
    for key in t_dict_attr.keys():
        _get_declarations_dict_(dict_attr, dict_method, t_dict_attr, t_dict_method,\
            key, key.parent)

    dict_attr_r, dict_method_r = {}, {}

    for item in t_dict_attr:
        dict_attr_r[item.name] = [i for i in t_dict_attr[item]]

    for item in t_dict_method:
        dict_method_r[item.name] = [i for i in t_dict_method[item]]

    return dict_attr_r, dict_method_r
    

def _get_declarations_dict_(dict_attr, dict_method, t_dict_attr, t_dict_method, current_type, parent_type):
    if parent_type.name in ['Object', None]:
        return
    t_dict_attr[current_type] += dict_attr[parent_type]
    t_dict_method[current_type] += dict_method[parent_type]
    next_parent = parent_type.parent
    return _get_declarations_dict_(dict_attr,  dict_method, t_dict_attr, t_dict_method, current_type, next_parent)
