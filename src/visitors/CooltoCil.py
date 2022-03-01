from cool_ast.cool_ast import *
import cil_ast.cil_ast as cil
from utils.semantic import VariableInfo
import visitors.visitor as visitor

class BaseCOOLToCILVisitor:
    def __init__(self, context):
        self.dottypes = []
        self.dotdata = []
        self.dotcode = []
        self.current_type = None
        self.current_function = None

        self.context = context
        self._self = VariableInfo('self', None)

        self.dvars = {}
        self.ctrs = {}
        self.dtypes = {}

        self.breakline_data = self.register_data('\n')
        self.emptystring_data = self.register_data('')

        self.locals = {}


    def transform_to_keys(self, xtype, keys):
        for i, key in enumerate(keys):
            xtype.attrs[key] = i
        return xtype.attrs
    
    # def build_type(self, node):
    #     type = self.register_type(node.id)
    #     self.dtypes[node.id.lex] = type
    #     ctype = self.context.get_type(node.id.lex)

    #     queue = []
    #     while ctype is not None:
    #         queue.append(ctype)
    #         ctype = ctype.parent

    #     rqueue = [ queue[i] for i in range(len(queue)-1, -1, -1)] #.reverse()
    #     for i in rqueue:
    #         _ = 0
    #         mm = sorted(i.methods)
    #         attribs = sorted(i.attributes)
    #         for attr in attribs:
    #             type.attributes[attr.name] = cil.AttributeNode(attr.name, i.name)
    #         for meth in mm:
    #             type.methods[meth] = self.to_function_name(meth, i.name)


    @property
    def params(self):
        return self.current_function.params
    
    @property
    def localvars(self):
        return self.current_function.localvars
    
    @property
    def instructions(self):
        return self.current_function.instructions
    

    def register_param(self, p):
        # try:
        #     p.lex
        # except:
        #     _ = 0
        name = f'param_at_{self.current_function.name}_{p.name}_{len(self.params)}'
        pnode = cil.ParamNode(name)
        self.dvars[p.name] = cil.VarNode(name)
        self.params.append(pnode)
        return self.dvars[p.name]

    def register_local(self, v):
        name = v.name
        try:
            v.lex
        except:
            _ = 0
        v.name = f'local_{self.current_function.name[9:]}_{v.name}_{len(self.localvars)}'
        local_node = cil.LocalNode(v.name)
        self.dvars[name] = cil.VarNode(v.name)
        self.localvars.append(local_node)
        return self.dvars[name]

    def register_attribute(self, name, type):
        name =  f'attr_{type}_{name}'
        return cil.AttributeNode(name, type)

    def define_internal_local(self):
        vinfo = VariableInfo('internal', None)
        return self.register_local(vinfo)

    def register_instruction(self, instruction):
        self.instructions.append(instruction)
        return instruction
    
    def to_function_name(self, method_name, type_name):
        return f'function_{method_name}_at_{type_name}'
    
    def register_function(self, function_name):
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node
    
    def register_type(self, name):
        type_node = cil.TypeNode(name)
        self.dtypes[name] = type_node
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = cil.DataNode(vname, value)
        self.dotdata.append(data_node)
        return data_node

    def register_label(self, label):
        lname = f'{label}_{self.current_function.labels_count}'
        self.current_function.labels_count += 1
        return cil.LabelNode(lname)

    def ctor(self, name):
        return '__ctor_{}'.format(name)

    def attrib_ctor_name(self, name):
        return '__attributes_ctor_{}'.format(name)


    def create_ctr(self, class_node, scope):
        attrs = [att for att in class_node.features if isinstance(att, AttrDeclarationNode)]
        while True:
            break
        self.current_function = self.register_function(self.to_function_name('ctor', self.current_type.name))
        self.register_instruction(cil.ParamNode('self'))

        for i, attr in enumerate(attrs):
            set_attr_node = self.visit(attr, scope)
            set_attr_node.index = i
            self.register_instruction(set_attr_node)
        self.register_instruction(cil.ReturnNode(VariableInfo('self', self.current_type)))
        

    def add_runtime_exception(self, cond, msg):
        error_node = self.register_label('error_label')
        continue_node = self.register_label('continue_label')
        self.register_instruction(cil.GotoIfNode(error_node.label, cond))
        self.register_instruction(cil.GotoNode(continue_node.label))
        self.register_instruction(error_node)
        data_node = self.register_data(msg)
        self.register_instruction(cil.ErrorNode(data_node))
        self.register_instruction(continue_node)

    def register_builtin(self):
        # Object
        line, column = 0, 0
        type_node = self.register_type('Object')

        self.current_function = self.register_function(self.ctor('Object'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Object', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('abort', 'Object'))
        self_ref = self.register_param(self._self)
        vname = self.define_internal_local()
        abort_data = self.register_data('Abort called from class ')
        self.register_instruction(cil.LoadNode(vname, abort_data))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.TypeOfNode(vname, self_ref))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.LoadNode(vname, self.breakline_data))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.ExitNode())

        self.current_function = self.register_function(self.to_function_name('type_name', 'Object'))
        self_ref = self.register_param(self._self)
        result = self.define_internal_local()
        self.register_instruction(cil.TypeOfNode(result, self_ref))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('copy', 'Object'))
        self_ref = self.register_param(self._self)
        result = self.define_internal_local()
        self.register_instruction(cil.CopyNode(result, self_ref))
        self.register_instruction(cil.ReturnNode(result))

        type_node.methods = {name: self.to_function_name(name, 'Object') for name in ['abort', 'type_name', 'copy']}
        type_node.methods['init'] = self.ctor('Object')
        obj_methods = ['abort', 'type_name', 'copy']

        # IO
        type_node = self.register_type('IO')

        self.current_function = self.register_function(self.ctor('IO'))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('IO', instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('out_string', 'IO'))
        self_ref = self.register_param(self._self)
        x = self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, x, '__prop', 'String'))
        self.register_instruction(cil.PrintStringNode(vname))
        self.register_instruction(cil.ReturnNode(self_ref))

        self.current_function = self.register_function(self.to_function_name('out_int', 'IO'))
        self_ref = self.register_param(self._self)
        x = self.register_param(VariableInfo('x', None))
        vname = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(vname, x, '__prop', 'Int'))
        self.register_instruction(cil.PrintIntNode(vname))
        self.register_instruction(cil.ReturnNode(self_ref))

        self.current_function = self.register_function(self.to_function_name('in_string', 'IO'))
        self_ref = self.register_param(self._self)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadStringNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('in_int', 'IO'))
        self_ref = self.register_param(self._self)
        result = self.define_internal_local()
        self.register_instruction(cil.ReadIntNode(result))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'IO') for name in
                              ['out_string', 'out_int', 'in_string', 'in_int']})
        type_node.methods['init'] = self.ctor('IO')

        # String
        type_node = self.register_type('String')
        type_node.attributes = {name:self.register_attribute(name, 'String') for name in ['__prop', 'length']}

        self.current_function = self.register_function(self.ctor('String'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('String', instance))
        self.register_instruction(cil.SetAttribNode(instance, '__prop', val, 'String'))
        result = self.define_internal_local()
        self.register_instruction(cil.LengthNode(result, val))
        attr = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), attr))
        self.register_instruction(cil.SetAttribNode(instance, 'length', attr, 'String'))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('length', 'String'))
        self_ref = self.register_param(self._self)
        result = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(result, self_ref, 'length', 'String'))
        self.register_instruction(cil.ReturnNode(result))

        self.current_function = self.register_function(self.to_function_name('concat', 'String'))
        self_ref = self.register_param(self._self)
        s = self.register_param(VariableInfo('s', None))
        str_1 = self.define_internal_local()
        str_2 = self.define_internal_local()
        length_1 = self.define_internal_local()
        length_2 = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_1, self_ref, '__prop', 'String'))
        self.register_instruction(cil.GetAttribNode(str_2, s, '__prop', 'String'))
        self.register_instruction(cil.GetAttribNode(length_1, self_ref, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(length_2, s, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(length_1, length_1, '__prop', 'Int'))
        self.register_instruction(cil.GetAttribNode(length_2, length_2, '__prop', 'Int'))
        self.register_instruction(cil.PlusNode(length_1, length_1, length_2))

        result = self.define_internal_local()
        self.register_instruction(cil.ConcatNode(result, str_1, str_2, length_1))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        self.current_function = self.register_function(self.to_function_name('substr', 'String'))
        self_ref = self.register_param(self._self)
        i = self.register_param(VariableInfo('i', None))
        l = self.register_param(VariableInfo('l', None))
        result = self.define_internal_local()
        index_value = self.define_internal_local()
        length_value = self.define_internal_local()
        length_wrapper = self.define_internal_local()
        length_attr = self.define_internal_local()
        length_substr = self.define_internal_local()
        less_value = self.define_internal_local()
        str_value = self.define_internal_local()
        self.register_instruction(cil.GetAttribNode(str_value, self_ref, '__prop', 'String'))
        self.register_instruction(cil.GetAttribNode(index_value, i, '__prop', 'Int'))
        self.register_instruction(cil.GetAttribNode(length_value, l, '__prop', 'Int'))
        # Check Out of range error
        self.register_instruction(cil.GetAttribNode(length_wrapper, self_ref, 'length', 'String'))
        self.register_instruction(cil.GetAttribNode(length_attr, length_wrapper, '__prop', 'Int'))
        self.register_instruction(cil.PlusNode(length_substr, length_value, index_value))
        self.register_instruction(cil.LessNode(less_value, length_attr, length_substr))
        self.add_runtime_exception(less_value, 'Index out of range exception')
        self.register_instruction(cil.SubstringNode(result, str_value, index_value, length_value))
        instance = self.define_internal_local()
        self.register_instruction(cil.ArgNode(result))
        self.register_instruction(cil.StaticCallNode(self.ctor('String'), instance))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods.update({name: self.to_function_name(name, 'String') for name in ['length', 'concat', 'substr']})
        type_node.methods['init'] = self.ctor('String')

        # Int
        type_node = self.register_type('Int')
        type_node.attributes = {name:self.register_attribute(name, 'Int') for name in ['__prop']}

        self.current_function = self.register_function(self.ctor('Int'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Int', instance))
        self.register_instruction(cil.SetAttribNode(instance, '__prop', val, 'Int'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method:self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.ctor('Int')

        # Bool
        type_node = self.register_type('Bool')
        type_node.attributes = {name:self.register_attribute(name, 'Bool') for name in ['__prop']}

        self.current_function = self.register_function(self.ctor('Bool'))
        val = self.register_param(VariableInfo('val', None))
        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode('Bool', instance))
        self.register_instruction(cil.SetAttribNode(instance, '__prop', val, 'Bool'))
        self.register_instruction(cil.ReturnNode(instance))

        type_node.methods = {method: self.to_function_name(method, 'Object') for method in obj_methods}
        type_node.methods['init'] = self.ctor('Bool')




class COOLToCILVisitor(BaseCOOLToCILVisitor):
    @visitor.on('node')
    def visit(self, node):
        pass
    
    def class_node_from_context(self, type):
        idx = type.name
        features = self.features_from_context(type)
        parent = 'Object' if idx not in ['Object', 'Void'] else None
        return ClassDeclarationNode(idx, features, parent)

    def features_from_context(self, type):
        feats = [AttrDeclarationNode(feat.name, feat.type) for feat in type.attributes]
        for func in type.methods:
            feats.append(FuncDeclarationNode(func.name, func.param_names, func.return_type, None))
        
        return feats


    def build_types(self, node):
        type = self.register_type(node.id)
        self.dtypes[node.id] = type
        ctype = self.context.get_type(node.id)

        queue = []
        while ctype is not None:
            queue.append(ctype)
            ctype = ctype.parent

        # queue.reverse()
        rqueue = [ queue[i] for i in range(len(queue)-1, -1, -1)] #.reverse()
        for i in rqueue:
            _ = 0
            methods = [m.name for m in i.methods]
            _attributes = i.attributes
            attributes = [x.name for x in _attributes]
            methods.sort()
            attributes.sort()
            for attr in attributes:
                type.attributes[attr] = cil.AttributeNode(attr, i.name)
            for meth in methods:
                type.methods[meth] = self.to_function_name(meth, i.name)


    # def build_type(self, node):
    #     type = self.register_type(node.id)
    #     self.dtypes[node.id.lex] = type
    #     ctype = self.context.get_type(node.id.lex)

    #     queue = []
    #     while ctype is not None:
    #         queue.append(ctype)
    #         ctype = ctype.parent

    #     rqueue = [ queue[i] for i in range(len(queue)-1, -1, -1)] #.reverse()
    #     for i in rqueue:
    #         _ = 0
    #         mm = sorted(i.methods)
    #         attribs = sorted(i.attributes)
    #         for attr in attribs:
    #             type.attributes[attr.name] = cil.AttributeNode(attr.name, i.name)
    #         for meth in mm:
    #             type.methods[meth] = self.to_function_name(meth, i.name)



    @visitor.when(ProgramNode)
    def visit(self, node, scope):
        ######################################################
        # node.declarations -> [ ClassDeclarationNode ... ]
        ######################################################
        self.register_builtin()
        self.current_function = None
        
        self.current_function = self.register_function('entry')
        inst = self.define_internal_local()


        self.register_instruction(cil.StaticCallNode(self.ctor('Main'), inst))
        self.register_instruction(cil.ArgNode(inst))
        self.register_instruction(cil.StaticCallNode(self.to_function_name('main', 'Main'),inst))
        self.register_instruction(cil.ReturnNode(0))

        for typ in node.declarations:
            self.build_types(typ)

        for i, typ in enumerate(node.declarations):
            self.visit(typ, scope.children[i])

        return cil.ProgramNode(self.dottypes, self.dotdata, self.dotcode)

    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        ####################################################################
        # node.id -> str
        # node.parent -> str
        # node.features -> [ FuncDeclarationNode/AttrDeclarationNode ... ]
        ####################################################################
        self.current_type = self.context.get_type(node.id)
        type = self.dtypes[node.id]

        self.current_function = self.register_function(self.attrib_ctor_name(node.id))
        type.methods['__attributes_ctor'] = self.current_function.name
        self_ref = self.register_param(self._self)

        # for at in type.attributes:
        #     # try:
        #     #     type[attributes][at]
        #     # except:
        #     #     _ = 0
        #     self.localvars.append(type.attributes[at])

        self.dvars.update({i:cil.AttributeNode(j.name, type.name)
                               for i,j in type.attributes.items()})

        self._self.name = self_ref
        if self.current_type.parent.name not in ('Object', 'IO'):
            dst = self.define_internal_local()
            self.register_instruction(cil.ArgNode(self_ref))
            self.register_instruction(cil.StaticCallNode(
                self.attrib_ctor_name(self.current_type.parent.name), dst))

        for i, feat in enumerate(node.features):
            if isinstance(feat, AttrDeclarationNode):
                # try:
                self.visit(feat, scope.children[i])
                self.register_instruction(cil.SetAttribNode(self_ref, feat.id, feat.noted_value, node.id,))
                # except Exception as e:
                    # _ = 0
        self.register_instruction(cil.ReturnNode(self_ref))

        # for feat, child in zip(node.features, scope.children):
        for i, feat in enumerate(node.features):
            if isinstance(feat, FuncDeclarationNode):
                # try:
                self.visit(feat, scope.children[i])
                # except Exception as e:
                #     _ = 0
        self._self.name = 'self'

        self.current_function = self.register_function(self.ctor(node.id))
        type.methods['__ctor'] = self.current_function.name
        # for at in type.attributes:
        #     self.localvars.append(type.attributes[at])

        instance = self.define_internal_local()
        self.register_instruction(cil.AllocateNode(node.id, instance))

        dst = self.define_internal_local()
        self.register_instruction(cil.ArgNode(instance))
        self.register_instruction(cil.StaticCallNode(self.attrib_ctor_name(node.id), dst))

        self.register_instruction(cil.ReturnNode(dst))

        self.current_function = None
        self.current_type = None

    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.value = ExpressionNode
        ###############################
        # local function to determine the default value of an attribute given its type
        def default_value_init(type):
            if type == 'Int':
                return ConstantNumNode(0)
            elif type == 'Bool':
                return FalseNode()
            elif type == 'String':
                return StringNode("")
            else:
                return VoidNode('void')

        dst = self.define_internal_local()
        if node.value:
            a = 0
            self.visit(node.value, scope.children[0])
            self.register_instruction(cil.AssignNode(dst, node.value.noted_value))


        elif node.type.name in ['SELF_TYPE', 'Int', 'Bool', 'String']:
            if node.type.name == 'SELF_TYPE':
                checked_t = self.current_type.name
            else:
                checked_t = node.type.name

            if checked_t == 'String':
                data = self.emptystring_data
                self.register_instruction(cil.LoadNode(dst, data))
                self.register_instruction(cil.ArgNode(dst))
            elif checked_t in ['Int', 'Bool']:
                self.register_instruction(cil.ArgNode(0))
            else:
                raise Exception('...builtin type not found? or bad registered type')
            self.register_instruction(cil.StaticCallNode(self.ctor(checked_t), dst))
        node.noted_value = dst

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.params -> [ (str, str) ... ]
        # node.type -> str
        # node.body -> [ ExpressionNode ... ]
        ###############################
        m = self.current_type.get_method(node.id, self.current_type, False)
        type = self.dtypes[self.current_type.name]
        self.current_function = self.register_function(self.to_function_name(m.name, self.current_type.name))
        # for at in type.attributes:
        #     self.localvars.append(type.attributes[at])

        self_ref = self.register_param(self._self)
        self._self.name = self_ref
        for param, type in node.params:
            self.register_param(VariableInfo(param, type))

        self.visit(node.body, scope)
        self.register_instruction(cil.ReturnNode(node.body.noted_value))
        self._self.name = 'self'

    @visitor.when(VarDeclarationNode) # AssignNode
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.type -> str
        # node.expr -> ExpressionNode
        ###############################
        var = scope.find_variable(node.id)
        dest = self.locals[var.name] = self.register_local(var)
        
        if node.expr is not None:
            source = self.visit(node.expr, scope)
        else:
            if node.type.name.lower() == 'int':
                source = 0
            elif node.type.name.lower() == 'string':
                source = ''
            elif node.type.name.lower() == 'bool':
                source = False
            else:
                source = None 
        self.register_instruction(cil.AssignNode(dest, source))
        return dest
            
    @visitor.when(AssignNode) # 
    def visit(self, node, scope):
        ###############################
        # node.id -> str
        # node.expr -> ExpressionNode
        ###############################
        dst = self.dvars[node.id]
        self.visit(node.expr, scope.children[0])
        self.register_instruction(cil.AssignNode(dst, node.expr.noted_value))
        node.noted_value = dst

    @visitor.when(CallNode)
    def visit(self, node, scope):
        ###############################
        # node.obj -> AtomicNode
        # node.method -> str
        # node.args -> [ ExpressionNode ... ]
        ###############################
        if isinstance(node.obj, CallNode) :
            _ = 0
        try:
            if node.method == 'type_name':
                _ = 0
        except:
            pass
        if node.obj:
            args = []
            for arg in node.args:
                self.visit(arg, scope)
                args.append(cil.ArgNode(arg.noted_value))

            self.visit(node.obj, scope)


            void = cil.VoidNode()
            isvoid = self.define_internal_local()
            self.register_instruction(cil.EqualNode(isvoid, node.obj.noted_value, void))
            self.add_runtime_exception(isvoid, 'Function call in a void instance')

            self.register_instruction(cil.ArgNode(node.obj.noted_value))
            for arg in args: self.register_instruction(arg)
            nval1 = self.define_internal_local()

            checked_t = node.obj.type.name
            # if isinstance(node.obj, InstantiateNode):
            #     checked_t = node.obj.lex
            # elif isinstance(node.obj, CallNode):
            #     checked_t = node.type.name
            # else:
            #     checked_t = scope.find_variable(node.obj.lex)
            #     if checked_t is None:
            #         if isinstance(node.obj, StringNode):
            #             checked_t = 'String'
            #         else:
            #             raise Exception("calling a function in a dst not found that is not a string wtf :D")
            #     else:
            #         checked_t = checked_t.type.name

            if node.parent is not None:
                # checked_t = node.type.lex
                nodefunc = self.dtypes[node.parent].methods[node.method]
                if nodefunc == '__ctor_type Object {\n\t[method] abort(): Object;\n\t[method] type_name(): String;\n\t[method] copy(): SELF_TYPE;\n}\n':
                    _ = 0
                self.register_instruction(cil.StaticCallNode(self.dtypes[node.parent].methods[node.method], nval1))
            else:
                # checked_t = node.obj.static_type.name
                self.register_instruction(cil.ArgNode(node.obj.noted_value))
                self.register_instruction(cil.DynamicCallNode(checked_t, self.dtypes[checked_t].methods[node.method], nval1))


            node.noted_value = nval1
        
        else:
            nval2 = self.define_internal_local()

            args = []
            for arg in node.args:
                self.visit(arg, scope)
                args.append(cil.ArgNode(arg.noted_value))

            self.register_instruction(cil.ArgNode(self._self.name))
            for arg in args: self.register_instruction(arg)
            self.register_instruction(cil.ArgNode(self._self.name))

            checked_t = self.current_type.name
            self.register_instruction(cil.DynamicCallNode(checked_t, self.dtypes[checked_t].methods[node.method], nval2))
            node.noted_value = nval2


    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        nval = self.define_internal_local()

        self.register_instruction(cil.ArgNode(node.lex))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval))
        node.noted_value = nval

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        if node.lex == 'self':
            node.noted_value = self._self.name
        else:
            node.noted_value = self.dvars[node.lex]

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        ###############################
        # node.lex -> str
        ###############################
        instval = self.define_internal_local()

        if node.type.name == 'SELF_TYPE':
            checked_t = self.current_type.name
        else:
            checked_t = node.type.name

        if checked_t in ['Int', 'Bool']:
            self.register_instruction(cil.ArgNode(0))
        elif checked_t == 'String':
            data = self.emptystring_data
            dst = self.define_internal_local()
            self.register_instruction(cil.LoadNode(dst, data))
            self.register_instruction(cil.ArgNode(dst))
        self.register_instruction(cil.StaticCallNode(self.ctor(checked_t), instval))
        node.noted_value = instval

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.PlusNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval,))

        node.noted_value = nval

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.MinusNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval))

        node.noted_value = nval

    @visitor.when(StarNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.StarNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval))
        node.noted_value = nval

    @visitor.when(DivNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()
        zero = self.define_internal_local()

        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)

        self.register_instruction(cil.ArgNode(0))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), zero))
        self.register_instruction(cil.GetAttribNode(zero, zero, '__prop', 'Int'))
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.EqualNode(zero, zero, right,
                                                ))
        self.add_runtime_exception(zero, 'Division by zero exception')

        self.register_instruction(cil.DivNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval))
        node.noted_value = nval

    @visitor.when(ChunkNode)
    def visit(self, node, scope):
        ###############################
        # node.chunk -> [ ExpressionNode... ]
        ###############################

        for i, expr in enumerate(node.chunk):
            self.visit(expr, scope.children[i])
        node.noted_value = node.chunk[-1].noted_value


    @visitor.when(ConditionalNode)
    def visit(self, node, scope):
        ###############################
        # node.ifChunk -> ExpressionNode
        # node.thenChunk -> ExpressionNode
        # node.elseChunk -> ExpressionNode
        ###############################

        nval = self.define_internal_local()
        cval = self.define_internal_local()

        then_label = self.register_label('then_label')
        continue_label = self.register_label('continue_label')

        self.visit(node.ifChunk, scope.children[0])
        self.register_instruction(cil.GetAttribNode(cval, node.ifChunk.noted_value, '__prop', 'Bool'))
        self.register_instruction(cil.GotoIfNode(then_label.label, cval))

        self.visit(node.elseChunk, scope.children[2])
        self.register_instruction(cil.AssignNode(nval, node.elseChunk.noted_value))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(then_label)
        self.visit(node.thenChunk, scope.children[1])
        self.register_instruction(cil.AssignNode(nval, node.thenChunk.noted_value))

        self.register_instruction(continue_label)
        node.noted_value = nval

    @visitor.when(LetInNode)
    def visit(self, node, scope):
        ###############################
        # node.decl_list -> [ DeclarationNode... ]
        # node.expression -> ExpressionNode
        ###############################

        i = 0
        for decl in node.decl_list:
            id = decl.id
            type = decl.type
            dst = self.register_local(VariableInfo(id, type))
            if decl.expr:
                self.visit(decl.expr, scope.children[i])
                self.register_instruction(cil.AssignNode(dst, decl.expr.noted_value))
                i += 1
            elif type in ['SELF_TYPE', 'Int', 'Bool', 'String']:
                if type == 'SELF_TYPE':
                    checked_t = self.current_type.name
                else:
                    checked_t = type
                if checked_t == 'Int':
                    self.register_instruction(cil.ArgNode(0))
                elif checked_t == 'Bool':
                    self.register_instruction(cil.ArgNode(0))
                elif checked_t == 'String':
                    data = self.emptystring_data
                    self.register_instruction(cil.LoadNode(dst, data))
                    self.register_instruction(cil.ArgNode(dst))
                self.register_instruction(cil.StaticCallNode(self.ctor(checked_t), dst))

        self.visit(node.expression, scope.children[-1])
        node.noted_value = node.expression.noted_value

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        while_label = self.register_label('while_label')
        loop_label = self.register_label('loop_label')
        pool_label = self.register_label('pool_label')
        cval = self.define_internal_local()

        self.register_instruction(while_label)
        self.visit(node.condition, scope.children[0])
        self.register_instruction(cil.GetAttribNode(cval, node.condition.noted_value, '__prop', 'Bool'))
        self.register_instruction(cil.GotoIfNode(loop_label.label, cval))
        self.register_instruction(cil.GotoNode(pool_label.label))

        self.register_instruction(loop_label)
        self.visit(node.loopChunk, scope.children[1])
        self.register_instruction(
            cil.GotoNode(while_label.label))

        self.register_instruction(pool_label)
        node.noted_value = cil.VoidNode()

    @visitor.when(NotNode)
    def visit(self, node, scope):
        ###############################
        # node.expression -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        value = self.define_internal_local()
        neg_value = self.define_internal_local()

        self.visit(node.expression, scope.children[0])
        self.register_instruction(cil.GetAttribNode(value, node.expression.noted_value, '__prop', 'Bool'))
        self.register_instruction(cil.NotNode(neg_value, value))
        self.register_instruction(cil.ArgNode(neg_value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))

        node.noted_value = nval

    @visitor.when(IsVoidNode)
    def visit(self, node, scope):
        ###############################
        # node.method -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        ret = self.define_internal_local()

        void = cil.VoidNode()
        self.visit(node.method, scope.children[0])
        self.register_instruction(cil.EqualNode(ret, node.method.noted_value, void))

        self.register_instruction(cil.ArgNode(ret))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))
        node.noted_value = nval

    @visitor.when(ComplementNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        value = self.define_internal_local()
        ret = self.define_internal_local()

        self.visit(node.expr, scope)
        self.register_instruction(cil.GetAttribNode(value, node.expr.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.ComplementNode(ret, value))
        self.register_instruction(cil.ArgNode(ret))
        self.register_instruction(cil.StaticCallNode(self.ctor('Int'), nval))
        node.noted_value = nval

    @visitor.when(SwitchCaseNode)
    def visit(self, node, scope):
        ###############################
        # node.expr -> ExpressionNode
        # node.case_list = [ (id, type, expr)... ]
        ###############################
        nval = self.define_internal_local()
        vtype = self.define_internal_local()
        cond = self.define_internal_local()

        self.visit(node.expr, scope)
        self.register_instruction(cil.TypeOfNode(vtype, node.expr.noted_value))

        isvoid = self.define_internal_local()
        self.register_instruction(cil.EqualNode(isvoid, node.expr.noted_value, cil.VoidNode()))
        self.add_runtime_exception(isvoid, 'Void isntance found in switch case')

        end_label = self.register_label('case_end_label')

        branch_type = self.define_internal_local()
        visited = []
        labels = []
        branches = sorted(node.case_list, key=lambda x: self.context.get_type(x[1]).depth, reverse=True)
        # for p, (id, type, expr) in enumerate(branches):
        for p, case in enumerate(branches):
            id   = case[0]
            type = case[1]
            expr = case[2]
            labels.append(self.register_label(f'case_label_{p}'))

            st = self.context.type_offsprings(type)
            for t in st:
                if t not in visited:
                    self.register_instruction(cil.NameNode(branch_type, t.name))
                    self.register_instruction(cil.EqualNode(cond, branch_type, vtype))
                    self.register_instruction(cil.GotoIfNode(labels[-1].label, cond))
                    visited.append(t)

        # not a runtime exception, but the data section to throw it
        data = self.register_data('Switch Case without valid branches')
        self.register_instruction(cil.ErrorNode(data))

        for p, label in enumerate(labels):
            id   = branches[p][0]
            type = branches[p][1]
            expr = branches[p][2]
            # id, type, expr = branches[p]
            sc = scope.children[p]

            self.register_instruction(label)
            var = self.register_local(VariableInfo(id, vtype))
            self.register_instruction(cil.AssignNode(var, node.expr.noted_value))
            self.visit(expr, sc)
            self.register_instruction(cil.AssignNode(nval, expr.noted_value))
            self.register_instruction(cil.GotoNode(end_label.label))

        self.register_instruction(end_label)
        node.noted_value = nval
        

    @visitor.when(TrueNode)
    def visit(self, node, scope):
        nval = self.define_internal_local()
        self.register_instruction(cil.ArgNode(1))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))
        node.noted_value = nval

    @visitor.when(FalseNode)
    def visit(self, node, scope):
        nval = self.define_internal_local()
        self.register_instruction(cil.ArgNode(0))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))
        node.noted_value = nval

    @visitor.when(StringNode)
    def visit(self, node, scope):
        try:
            data = [i for i in self.dotdata if i.value == node.lex][0]
        except IndexError:
            data = self.register_data(node.lex[1:-1])

        dst = self.define_internal_local()
        nval = self.define_internal_local()
        self.register_instruction(cil.LoadNode(dst, data))
        self.register_instruction(cil.ArgNode(dst))
        self.register_instruction(cil.StaticCallNode(self.ctor('String'), nval))
        node.noted_value = nval


    @visitor.when(EqualNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        type_left = self.define_internal_local()
        
        right = self.define_internal_local()
        int_t = self.define_internal_local()
        bool_t = self.define_internal_local()
        string_t = self.define_internal_local()
        equal = self.define_internal_local()
        value = self.define_internal_local()
        int_comparisson = self.register_label('comparing_ints')
        bool_comparisson = self.register_label('comparing_bools')
        string_comparisson = self.register_label('comparing_strings')
        continue_label = self.register_label('comparing_notbuiltin')

        self.visit(node.left, scope)
        self.visit(node.right, scope)
        self.register_instruction(cil.TypeOfNode(type_left, node.left.noted_value))
        self.register_instruction(cil.NameNode(int_t, 'Int'))
        self.register_instruction(cil.NameNode(string_t, 'String'))
        self.register_instruction(cil.NameNode(bool_t, 'Bool'))
        self.register_instruction(cil.EqualNode(equal, type_left, int_t))
        self.register_instruction(cil.GotoIfNode(int_comparisson.label, equal))
        self.register_instruction(cil.EqualNode(equal, type_left, string_t))
        self.register_instruction(cil.GotoIfNode(string_comparisson.label, equal))
        self.register_instruction(cil.EqualNode(equal, type_left, bool_t))
        self.register_instruction(cil.GotoIfNode(bool_comparisson.label, equal))

        # for i in self.dtypes:
            # try:
        #     self.visit()
            # except:
        #     __ = 0

        self.register_instruction(cil.EqualNode(value, node.left.noted_value, node.right.noted_value))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(int_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.EqualNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(string_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'String'))
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'String'))
        self.register_instruction(cil.EqualStringNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(bool_comparisson)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Bool'))
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Bool'))
        self.register_instruction(cil.EqualNode(value, left, right))
        self.register_instruction(cil.GotoNode(continue_label.label))

        self.register_instruction(continue_label)

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))
        node.noted_value = nval

    @visitor.when(LessNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()
        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.LessNode(value, left, right))
        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))

        node.noted_value = nval
    

    @visitor.when(LeqNode)
    def visit(self, node, scope):
        ###############################
        # node.left -> ExpressionNode
        # node.right -> ExpressionNode
        ###############################
        nval = self.define_internal_local()
        left = self.define_internal_local()
        right = self.define_internal_local()
        value = self.define_internal_local()

        self.visit(node.left, scope)
        self.register_instruction(cil.GetAttribNode(left, node.left.noted_value, '__prop', 'Int'))
        self.visit(node.right, scope)
        self.register_instruction(cil.GetAttribNode(right, node.right.noted_value, '__prop', 'Int'))
        self.register_instruction(cil.LessEqualNode(value, left, right))

        self.register_instruction(cil.ArgNode(value))
        self.register_instruction(cil.StaticCallNode(self.ctor('Bool'), nval))

        node.noted_value = nval
