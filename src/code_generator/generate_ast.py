from math import exp
from parsing.ast import *
from .ast_CIL import *
import cmp.visitor as visitor


class CILScope:
    def __init__(self):
        self.let_count = 0
        self.if_count = 0
        self.case_count = 0
        self.variables_count = 0
        
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
            local_dict[id] = CILLocalNode(nickname, CILTypeConstantNode(type)) 
        else:
            nickname = f'{id}_{self.variables_count}'
            self.variables_count += 1
            node = CILLocalNode(nickname, CILTypeConstantNode(type))
            local_dict[id] = node
            
            if not is_param:
                self.all_locals.append(node)
                
        return nickname
                
    def add_new_local(self, type):
        local_dict = self.locals[-1] 
        name = f't_{self.variables_count}'
        self.variables_count += 1
        node = CILLocalNode(name, CILTypeConstantNode(type))
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

#pending 
def create_init_class(attributes, expresions):
    for attr,expr in zip(attributes,expresions):
        assig = CILAssignNode (attr.id,expr)


class CIL:
    def __init__(self):
        self.scope = CILScope()

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        types = []
        for d in node.declarations:  # TODO organizar de modo q quede el main de primero
            type = self.visit(d)
            types.append(type)
          
        return CILProgramNode(types, self.scope.data, self.scope.functions)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.scope.current_class = node.id
        
        attributes = []
        expressions = []
        methods = []
        for feature in node.features:
            if isinstance (feature, AttrDeclarationNode):
                attr = self.visit(feature)
                attributes.append(attr)
                if feature.expr is not None:
                    expr = self.visit(feature.expr)
                    expressions.append(expr)
            else:
                function = self.visit(feature)
                self.scope.functions.append(function) 
                methods.append(CILMethodNode(feature.id, function.id))   
                
        methods.append(CILMethodNode('init', f'init_{node.id}'))         
        # use expressions here
        #init_class = create_init_class (type.attributes,expressions)    
        #self.scope.functions.append (init_class)  
        
        # herencia          
              
        return CILTypeNode(node.id, attributes, methods)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        return CILAttributeNode(node.id, CILTypeConstantNode(node.type))
    
    @visitor.when(FuncDeclarationNode) 
    def visit(self, node):
        self.scope.all_locals = []
        self.scope.locals = [{}]
        self.scope.instructions = []
        
        params = []
        param_node = CILParamNode(CILVariableNode(f'self_{self.scope.current_class}'), CILTypeConstantNode(self.scope.current_class))
        params.append(param_node)
        
        for param in node.params:
            name = self.scope.add_local(param.id, param.type, True)
            param_node = CILParamNode(name, CILTypeConstantNode(param.type))
            params.append(param_node)
            
        expr = self.visit(node.expr)  
        new_var = self.scope.add_new_local(node.type)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(new_var), expr))
        self.scope.instructions.append(CILReturnNode(CILVariableNode(new_var)))
        return CILFuncNode(f'{node.id}_{self.scope.current_class}', params, self.scope.all_locals, self.scope.instructions)
                   
    @visitor.when(BlockNode)
    def visit(self, node): 
        for i in range(0, len(node.expr_lis) - 1):
            self.visit(node.expr_lis[i]) # Necesary instructions are added, but there is not sense to keep the expression
        expr = node.expr_lis[len(node.expr_lis) - 1]
        return self.visit(expr)
            
    @visitor.when(DispatchNode)
    def visit(self, node):
        if not isinstance(node.expr, VariableNode) or node.expr.lex != 'self':
            expr = self.visit(node.expr)
            name = self.scope.add_new_local(None)  # TODO revisar el tipo de retorno (idea, a;adir una instruccio typeof)
            instruction = CILAssignNode(CILVariableNode(name), expr)
            self.scope.instructions.append(instruction)  
        else: 
            name = f'self_{self.scope.current_class}' 
        
        args = []
        args.append(CILArgNode(CILVariableNode(name)))
        for arg in node.arg:
            expr = self.visit(arg)
            name_arg = self.scope.add_new_local(None) # TODO lo mismo de arriba
            if not isinstance(expr, VariableNode):
                instruction = CILAssignNode(CILVariableNode(name_arg), expr)
                self.scope.instructions.append(instruction)
                args.append(CILArgNode(CILVariableNode(name_arg)))
            else: 
                args.append(CILArgNode(CILVariableNode(expr.lex)))   
        self.scope.instructions.extend(args)        
        
        if node.type is not None:
            expression = CILVCallNode(CILTypeConstantNode(node.type.name), node.id)
        else:         
            expression = CILCallNode(node.id)
        new_var = self.scope.add_new_local(None) # TODO
        node_var = CILVariableNode(new_var)
        self.scope.instructions.append(CILAssignNode(node_var, expression))     
        return node_var

    @visitor.when(ConditionalNode)
    def visit(self, node):
       pass
            
    @visitor.when(LetNode)
    def visit(self, node):
        self.scope.locals.append({})
        for variable in node.variables:
            self.visit(variable)
        expr = self.visit(node.expr)
        self.scope.locals.pop()
        return expr
        
    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        name = self.scope.add_local(node.id, node.type)
        if node.expr is not None:
            expr = self.visit(node.expr)
            instruction = CILAssignNode(CILVariableNode(name), expr)
            self.scope.instructions.append(instruction)
            
    @visitor.when(LoopNode)
    def visit(self, node):
        pass
          
    @visitor.when(CaseNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        var_name = f't{self.scope.variables_count}'
        self.scope.variables_count += 1
        
        self.scope.locals.append(CILLocalNode(var_name, None))
        self.scope.instructions.append(CILAssignNode(var_name, expr))
        typeof = CILTypeOfNode(var_name)
        self.scope.instructions.append(CILAssignNode(var_name, typeof))
        
        for case in node.cases:
            self.visit(case)

    @visitor.when(CaseAttrNode)
    def visit(self, node):  
        #local = mself.scope.add_new_local(node.id)
        self.scope.instructions.append(CILLabelNode(""))
        expresion_branch = self.visit(node.expr)
         
    @visitor.when(AssignNode)
    def visit(self, node):
        var = self.visit(node.expr)
        local = self.scope.find_local(node.id.lex)

        if local is not None:
            self.scope.instructions.append(CILAssignNode(CILVariableNode(local.id), var))
            return CILVariableNode(local.id)
        else:
            self.scope.instructions.append(CILSetAttributeNode(CILVariableNode(f'self_{self.scope.current_class}'), CILTypeConstantNode(self.scope.current_class), CILVariableNode(node.id.lex), var))
            return var
                                     
    @visitor.when(BinaryNode)
    def visit(self, node):
        if not isinstance(node.left, AtomicNode):
            name = self.scope.add_new_local(node.left.computed_type.name)
            expr = self.visit(node.left)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))
            left = CILVariableNode(name)
            
        else:
            left = self.visit(node.left)  

        if not isinstance(node.right, AtomicNode):
            name = self.scope.add_new_local(node.right.computed_type.name)
            expr = self.visit(node.right)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))
            right = CILVariableNode(name)
        else:
            right = self.visit(node.right)
        
        if isinstance(node, PlusNode):
            return CILPlusNode(left, right)
        elif isinstance(node, MinusNode):
            return CILMinusNode(left, right)
        elif isinstance(node, DivNode):
            return CILDivNode(left, right)
        elif isinstance(node, StarNode):
            return CILStarNode(left, right)
        elif isinstance(node, ElessNode):
            return CILElessNode(left, right)
        elif isinstance(node, LessNode):
            return CILLessNode(left, right)
        else:
            return CILEqualsNode(left, right)
                
    @visitor.when(PrimeNode)
    def visit(self, node):
        pass
   
    @visitor.when(NotNode)
    def visit(self, node):
       pass
    @visitor.when(StringNode)
    def visit(self, node):
        pass

    @visitor.when(IsVoidNode)
    def visit(self, node):
        pass
    
    @visitor.when(ConstantNumNode)
    def visit(self, node):
        return CILNumberNode(node.lex)

    @visitor.when(VariableNode)
    def visit(self, node):
        local = self.scope.find_local(node.lex)
        if local is not None:
            return CILVariableNode(local.id)
        else:
            return CILGetAttribute(CILVariableNode(f'self_{self.scope.current_class}'), CILTypeConstantNode(self.scope.current_class), CILVariableNode(node.lex))
        
    @visitor.when(TrueNode)
    def visit(self, node):
       pass

    @visitor.when(FalseNode)
    def visit(self, node):
        pass   
    
    @visitor.when(InstantiateNode)
    def visit(self, node):
        pass 
