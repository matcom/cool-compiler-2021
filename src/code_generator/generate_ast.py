from parsing.ast import *
from .ast_CIL import *
from .utils import *
from cmp.semantic import IntType, StringType, BoolType, ObjectType
import cmp.visitor as visitor
        
    
class CIL:
    def __init__(self, context):
        self.scope = CILScope(context)

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        types_ts = get_ts(self.scope.context)
        infos = self.scope.infos = {}
        for type in types_ts:
            t = TypeInfo() 
            infos[type.name] = t  
            if type.parent is not None:
                p = type.parent.name
                t.attrs = infos[p].attrs.copy()
                t.methods = infos[p].methods.copy()
            
            t.attrs.extend(type.attributes)
            for m in type.methods:
                t.methods[m.name] = f'{m.name}_{type.name}'
            
        types = []
        for d in node.declarations:
            type = self.visit(d)
            types.append(type)
        
        # Add built-in types and functions
        types.extend(self.scope.create_builtin_types())
        
        # Brings main function to the first position
        main_idx = [idx for idx, element in enumerate(self.scope.functions) if element.id == 'main_Main'][0]
        main = self.scope.functions[main_idx]
        self.scope.functions.pop(main_idx)
        self.scope.functions.insert(0, main)
        
        return CILProgramNode(types, self.scope.data, self.scope.functions)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.scope.current_class = node.id
        att_aux = []
        attributes = []
        expressions = []
        methods = []
        
        type_info = self.scope.infos[node.id]
        for a in type_info.attrs:   
            attributes.append(CILAttributeNode(a.name, a.type))
        for m in type_info.methods.keys():        
            methods.append(CILMethodNode(m, type_info.methods[m])) 
        methods.append(CILMethodNode('init', f'init_{node.id}'))         
                
        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                if feature.expr is not None:
                    expr = self.visit(feature.expr)
                    expressions.append(expr)
                    att_aux.append(feature.id)
                    
            else:
                function = self.visit(feature)
                self.scope.functions.append(function) 

        init_class = self.scope.create_init_class(att_aux , expressions)    
        self.scope.functions.append(init_class)  
        
        return CILTypeNode(node.id, attributes, methods)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        pass
    
    @visitor.when(FuncDeclarationNode) 
    def visit(self, node):
        self.scope.all_locals = []
        self.scope.locals = [{}]
        self.scope.instructions = []
        
        params = []
        param_node = CILParamNode(f'self_{self.scope.current_class}', self.scope.current_class)
        params.append(param_node)
        
        for param in node.params:
            name = self.scope.add_local(param.id, param.type, True)
            param_node = CILParamNode(name, param.type)
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
            name = self.scope.add_new_local(node.expr.computed_type.name) 
            instruction = CILAssignNode(CILVariableNode(name), expr)
            self.scope.instructions.append(instruction)  
        else: 
            name = f'self_{self.scope.current_class}' 
        
        args = []
        args.append(CILArgNode(CILVariableNode(name)))
        for arg in node.arg:
            expr = self.visit(arg)
            name_arg = self.scope.add_new_local(arg.computed_type.name)
            if not isinstance(expr, VariableNode):
                instruction = CILAssignNode(CILVariableNode(name_arg), expr)
                self.scope.instructions.append(instruction)
                args.append(CILArgNode(CILVariableNode(name_arg)))
            else: 
                args.append(CILArgNode(CILVariableNode(expr.lex)))   
        self.scope.instructions.extend(args)        
        
        if node.type is not None:
            expression = CILVCallNode(node.type.name, node.id)
        else:         
            expression = CILCallNode(node.id)
        type = self.scope.ret_type_of_method(node.id, self.scope.current_class)
        new_var = self.scope.add_new_local(type) 
        node_var = CILVariableNode(new_var)
        self.scope.instructions.append(CILAssignNode(node_var, expression))     
        return node_var

    @visitor.when(ConditionalNode)
    def visit(self, node):
        exp = self.visit(node.predicate)
        name_expr = self.scope.add_new_local("Int")
        name_return = self.scope.add_new_local(node.computed_type.name)
        var_condition = CILVariableNode(name_expr) 
        var_return = CILVariableNode(name_return) 
        self.scope.instructions.append(CILAssignNode(var_condition, exp))
        self.scope.instructions.append(CILIfGotoNode(var_condition,CILLabelNode(f'then_{self.scope.if_count}')))
        count = self.scope.if_count
        self.scope.if_count += 1
        exp_else = self.visit(node.elsex)
        self.scope.instructions.append(CILAssignNode(var_return, exp_else))
        self.scope.instructions.append(CILGotoNode(CILLabelNode(f'ifend{count}')))
        self.scope.instructions.append(CILLabelNode( f'then{count}'))
        exp_then = self.visit(node.then)
        self.scope.instructions.append(CILAssignNode(var_return, exp_then))
        self.scope.instructions.append(CILLabelNode(f'ifend{count}'))
        return var_return
            
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
        elif isinstance(node.computed_type, IntType): 
            self.scope.instructions.append(CILArgNode(CILNumberNode(0)))
            self.scope.instructions.append(CILVCallNode('Int', 'init'))
        elif isinstance(node.computed_type, BoolType): 
            self.scope.instructions.append(CILArgNode(CILNumberNode(0)))
            self.scope.instructions.append(CILVCallNode('Bool', 'init'))
        elif isinstance(node.computed_type, StringType):
            self.scope.instructions.append(CILArgNode(CILNumberNode(0)))
            self.scope.instructions.append(CILVCallNode('String', 'init'))
            
    @visitor.when(LoopNode)
    def visit(self, node):
        count = self.scope.loop_count
        self.scope.loop_count += 1
        self.scope.instructions.append(CILLabelNode(f'while_{count}'))
        pred = self.visit(node.predicate)
        name_pred = self.scope.add_new_local("Bool")
        name_return = self.scope.add_new_local(node.computed_type.name)
        
        var_condition = CILVariableNode(name_pred) 
        var_return = CILVariableNode(name_return) 
        self.scope.instructions.append(CILAssignNode(var_condition, pred))
        self.scope.instructions.append(CILIfGotoNode(var_condition,CILLabelNode(f'body_{count}')))
        self.scope.instructions.append(CILGotoNode(CILLabelNode(f'pool_{count}')))
        self.scope.instructions.append(CILLabelNode(f'body_{count}'))
        body = self.visit(node.body)
        self.scope.instructions.append(CILAssignNode(var_return, body))
        self.scope.instructions.append(CILGotoNode(CILLabelNode(f'while_{count}')))
        self.scope.instructions.append(CILLabelNode(f'pool_{count}'))

        return var_return
          
    @visitor.when(CaseNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        self.expression_var_case = expr
        name = self.scope.add_new_local(node.expr.computed_type.name)
        var = CILVariableNode(name)
        self.scope.instructions.append(CILAssignNode(var, expr))
        
        expr_type_of = CILTypeOfNode(var)
        name_type_expr = self.scope.add_new_local(node.expr.computed_type.name)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name_type_expr), expr_type_of))     
        name_return =  self.scope.add_new_local(node.computed_type.name)
        return_ = CILVariableNode(name_return)
        
        for case, index in zip(node.cases,range(0,len(node.cases))):
            if index != 0:
                self.scope.instructions.append(CILLabelNode(f'branch_{self.scope.case_count}_{index-1}')) 
            
            case_expr_type_of = CILTypeConstantNode(case.type)
            name_var_condition = self.scope.add_new_local(None)
            var_condition = CILVariableNode(name_var_condition)
            self.scope.instructions.append(CILAssignNode(var_condition, CILNotEqualsNode(CILVariableNode(name_type_expr),case_expr_type_of)))
            self.scope.instructions.append(CILIfGotoNode(var_condition,CILLabelNode(f'branch_{self.scope.case_count}_{index}')))
            
            expr_attr = self.visit(case)
            
            self.scope.instructions.append(CILAssignNode(return_, expr_attr))    
       
            self.scope.instructions.append(CILGotoNode(CILLabelNode(f'case_end{self.scope.case_count}')))
        self.scope.instructions.append(CILLabelNode(f'case_end{ self.scope.case_count}'))
        self.scope.case_count += 1 
        return return_
            
    @visitor.when(CaseAttrNode)
    def visit(self, node):  
        self.scope.locals.append({})
        local = self.scope.add_local(node.id, node.type)
        self.scope.instructions.append(CILAssignNode( CILVariableNode(local), self.expression_var_case))

        expression_branch = self.visit(node.expr)
        self.scope.locals.pop()
        return expression_branch
         
    @visitor.when(AssignNode)
    def visit(self, node):
        var = self.visit(node.expr)
        local = self.scope.find_local(node.id.lex)

        if local is not None:
            self.scope.instructions.append(CILAssignNode(CILVariableNode(local.id), var))
            return CILVariableNode(local.id)
        else:
            self.scope.instructions.append(CILSetAttributeNode(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.id.lex), var))
            return var
                                     
    @visitor.when(BinaryNode)
    def visit(self, node):
        expr_left = self.visit(node.left)
        expr_right = self.visit(node.right)
        if not isinstance(expr_left, CILAtomicNode):
            name = self.scope.add_new_local(node.left.computed_type.name)
            expr = self.visit(node.left)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))
            left = CILVariableNode(name)
            
        else:
            left = expr_left 

        if not isinstance(expr_right, CILAtomicNode):
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
        expr = self.visit(node.expr)
        return CILStarNode(expr , CILNumberNode(-1))
   
    @visitor.when(NotNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        return  CILNotEqualsNode( expr, CILNumberNode(0))
    
    @visitor.when(StringNode)
    def visit(self, node):
        data = CILDataNode(f'str_{self.scope.str_count}', node.lex)
        self.scope.data.append(data)
        return CILLoadNode(data.id) 

    @visitor.when(IsVoidNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        if isinstance(node.expr.computed_type, IntType) or isinstance(node.expr.computed_type, StringType) or isinstance(node.expr.computed_type, BoolType):
            return CILNumberNode(0)
        else: 
            name = self.scope.add_new_local(node.computed_type)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))
            return CILEqualsNode(CILVariableNode(name), CILNumberNode(0)) 
    
    @visitor.when(ConstantNumNode)
    def visit(self, node):
        return CILNumberNode(node.lex)

    @visitor.when(VariableNode)
    def visit(self, node):
        local = self.scope.find_local(node.lex)
        if local is not None:
            return CILVariableNode(local.id)
        else:
            return CILGetAttribute(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.lex))
        
    @visitor.when(TrueNode)
    def visit(self, node):
       return CILNumberNode(1)

    @visitor.when(FalseNode)
    def visit(self, node):
       return CILNumberNode(0)
    
    @visitor.when(InstantiateNode)
    def visit(self, node):
        return CILAllocateNode(CILTypeConstantNode(node.lex)) 
