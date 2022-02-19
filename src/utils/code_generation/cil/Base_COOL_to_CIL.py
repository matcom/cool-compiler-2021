from utils.code_generation.cil.AST_CIL import cil_ast as nodes
from cmp.semantic import VariableInfo


class BaseCOOLToCIL:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []

        self.current_type = None
        self.current_method = None
        self.current_function = None

        self.context = context
        self.vself = VariableInfo('self', None)
    
    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars

    @property
    def ids(self):
        return self.current_function.ids
    
    @property
    def instructions(self):
        return self.current_function.instructions
    
    def register_param(self, vinfo):
        param_node = nodes.ParamNode(vinfo.name)
        self.params.append(param_node)
        return vinfo.name
    
    def register_local(self, vinfo, id=False):
        if len(self.current_function.name) >= 8 and self.current_function.name[:8] == 'function':
            name = f'local_{self.current_function.name[9:]}_{vinfo.name}_{len(self.localvars)}'
        else:
            name = f'local_{self.current_function.name[5:]}_{vinfo.name}_{len(self.localvars)}'
        
        new_vinfo = VariableInfo(name, None)
        local_node = nodes.LocalNode(new_vinfo.name)

        if id:
            self.ids[vinfo.name] = new_vinfo.name

        self.localvars.append(local_node)
        return new_vinfo.name

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'

    def init_name(self, type_name, attr=False):
        if attr:
            return f'init_attr_at_{type_name}'
        return f'init_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = nodes.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = nodes.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = nodes.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return nodes.LabelNode(lname)
    
    def register_runtime_error(self, condition, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(nodes.IfGotoNode(condition, error_node.label))
        self.register_instruction(nodes.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(nodes.ErrorNode(data_node))
        self.register_instruction(continue_node)