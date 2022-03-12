
from weakref import ref
from parsing.ast import *
from .ast_CIL import *
from .utils import *
from semantics.semantic import IOType, IntType, StringType, BoolType, ObjectType
import utils.visitor as visitor


    
class CIL:
    def __init__(self, context):
        self.scope = CILScope(context)       

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        # Creates the first function to execute
        locals = []
        locals.append(CILLocalNode("m0", "Main"))
        locals.append(CILLocalNode("m1", "Main"))
        locals.append(CILLocalNode("m2", "Main")) 
        
        instructions = []
        instructions.append(CILAssignNode(CILVariableNode("m0"), CILAllocateNode(CILTypeConstantNode("Main"))))
        instructions.append(CILArgNode(CILVariableNode("m0")))
        instructions.append(CILAssignNode(CILVariableNode("m1"), CILVCallNode("Main", "Init_Main")))
        instructions.append(CILArgNode(CILVariableNode("m1")))
        instructions.append(CILAssignNode(CILVariableNode("m2"), CILVCallNode("Main", "main")))
        instructions.append(CILReturnNode(CILVariableNode("m2")))
        self.scope.functions.append(CILFuncNode('main', [], locals, instructions))
        
        self.scope.data.append(CILDataNode(f'str_empty', "\"\""))
        table_ = bfs_init(self.scope.context)
        self.table = table(table_)
        types_ts, types_heirs = get_ts(self.scope.context)
        self.types_ts = types_ts
        self.types_heirs = types_heirs
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
        
        return CILProgramNode(types, self.scope.data, self.scope.functions)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.scope.current_class = node.id
        self.scope.attributes = {}
        features = []
        methods = []
        locals  = []
        type_info = self.scope.infos[node.id]
        
        for a in type_info.attrs:   
            self.scope.attributes[a.name] = CILAttributeNode(a.name, a.type)
        methods.append(CILMethodNode(f'Init_{node.id}', f'Init_{node.id}'))         
        
        for m in type_info.methods.keys():        
            methods.append(CILMethodNode(m, type_info.methods[m])) 
                
        for feature in node.features:
            self.scope.instructions = []
            self.scope.locals = [{}]
            self.scope.all_locals = []
            if isinstance(feature, AttrDeclarationNode):
                if feature.expr is not None:    
                    expr = self.visit(feature.expr), feature.expr.computed_type
                    features.append((feature.id, feature.type, expr, self.scope.instructions.copy()))
                    self.scope.instructions =  []
                else:
                    expr = None
                    features.append((feature.id, feature.type, None, None))
                
                locals.extend(self.scope.all_locals.copy())
                   
            else:
                function = self.visit(feature)
                self.scope.functions.append(function) 

        self.scope.locals = [{}]
        self.scope.all_locals = []
        init_class = self.scope.create_init_class(features, locals)    
        self.scope.functions.append(init_class)  
        
        return CILTypeNode(node.id, self.scope.attributes.values(), methods)
            
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
            type = node.expr.computed_type.name
        elif node.expr.lex == 'self':
            name = f'self_{self.scope.current_class}' 
            type = self.scope.current_class   
        else:
            name = self.scope.find_local(node.expr.lex)
            type = node.expr.computed_type.name
        if node.type is not None:
            type = node.type         
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
            expression = CILVCallNode(node.type, node.id, True)
        else:         
            expression = CILVCallNode(type, node.id)
        type = self.scope.ret_type_of_method(node.id, type)
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
        self.scope.instructions.append(CILGotoNode(CILLabelNode(f'ifend_{count}')))
        self.scope.instructions.append(CILLabelNode( f'then_{count}'))
        exp_then = self.visit(node.then)
        self.scope.instructions.append(CILAssignNode(var_return, exp_then))
        self.scope.instructions.append(CILLabelNode(f'ifend_{count}'))
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
        elif isinstance(node.computed_type, IntType): 
            expr = CILNumberNode(0)
        elif isinstance(node.computed_type, BoolType): 
            expr = CILEqualsNode(CILNumberNode(0), CILNumberNode(1), False)
        elif isinstance(node.computed_type, StringType):
            expr = CILLoadNode('str_empty')
        else:
            expr = None

        if expr is not None:
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))

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
        expr = self.visit(node.expr) # the code for computing the expression is generated
        self.expression_var_case = expr

        expr_type = node.expr.computed_type
        expr_var_name = self.scope.add_new_local(expr_type.name)
        expr_var = CILVariableNode(expr_var_name)
        self.scope.instructions.append(CILAssignNode(expr_var, expr)) # save the expression result in a local

        types_ts_pos = { type.name : i for i, type in enumerate(self.types_ts) }

        if (expr_type.ref): # when the expression is a reference type we need to compute least ancestor for all valid dynamic types of the expression
            expr_type_of = CILTypeOfNode(expr_var)
            name_type_expr = self.scope.add_new_local(expr_type.name)
            type_expr_var = CILVariableNode(name_type_expr)
            self.scope.instructions.append(CILAssignNode(type_expr_var,expr_type_of))
            # until here we have 
            # t0 = expr
            # t1 = TYPEOF t0
            name_type_comp = self.scope.add_new_local('Bool')
            type_comp_var = CILVariableNode(name_type_comp)


            # use the topological sort computed in the ProgramNode to sort the types of the branches of the case         
            case_types = [case.type for case in node.cases]
            case_types = sorted(case_types, key=lambda t: types_ts_pos[t], reverse=True)
            least_ancestor = {}
            case_labels = {}
            for type in case_types:
                least_ancestor[type] = type
                case_labels[type] = CILLabelNode(f'case_{self.scope.case_count}_{type}')
                try:
                    queue = self.types_heirs[type].copy() # place the children class
                except KeyError: # last type in a branch of the Type Tree
                    queue = None
                while queue: # travel to all descendants
                    descendant = queue.pop()
                    try:
                        # this type was visited by a type that is later in 
                        # the topological order so is more close to the type in the class hierarchy
                        least_ancestor[descendant]
                        continue
                    except KeyError:
                        least_ancestor[descendant] = type
                        try:
                            queue = self.types_heirs[descendant] + queue
                        except KeyError:
                            pass
            for type, lancestor in least_ancestor.items():
                self.scope.instructions.append(CILAssignNode(type_comp_var, CILEqualsNode(type_expr_var, CILTypeConstantNode(type), ref)))
                self.scope.instructions.append(CILIfGotoNode(type_comp_var, case_labels[lancestor]))
        
        result_name = self.scope.add_new_local(node.computed_type.name)
        var_result = CILVariableNode(result_name)
        # first generate the instructions of the labels to get the CILLabelNodes to use

        for case in sorted(node.cases, key=lambda c: types_ts_pos[c.type], reverse=True):
            case_type_ref = case.type not in ["Bool", "Int"]
            if (not expr_type.ref and case_type_ref and case.type != 'Object'):
                continue
            self.scope.instructions.append(CILLabelNode(f'case_{self.scope.case_count}_{case.type}'))
            if (expr_type.ref and not case_type_ref):
                self.scope.instructions.append(CILAssignNode(expr, CILUnboxNode(expr, case.type)))
            if (not expr_type.ref and case_type_ref):
                self.scope.instructions.append(CILAssignNode(expr, CILBoxNode(expr, expr_type.name)))
            branch_expr = self.visit(case)
            self.scope.instructions.append(CILAssignNode(var_result, branch_expr))
            if (node.computed_type.ref and not case_type_ref):
                self.scope.instructions.append(CILAssignNode(var_result, CILBoxNode(var_result, case.type)))
            self.scope.instructions.append(CILGotoNode(CILLabelNode(f'case_{self.scope.case_count}_end')))
            if (not expr_type.ref):
                break
        self.scope.instructions.append(CILLabelNode(f'case_{self.scope.case_count}_end'))
        self.scope.case_count += 1
        return var_result
            
    @visitor.when(CaseAttrNode)
    def visit(self, node):  
        self.scope.locals.append({})
        local = self.scope.add_local(node.id, node.type)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(local), self.expression_var_case))

        expression_branch = self.visit(node.expr)
        self.scope.locals.pop()
        return expression_branch
         
    @visitor.when(AssignNode)
    def visit(self, node):
        var = self.visit(node.expr)
        
        if not isinstance(var, CILAtomicNode):
            variable = CILVariableNode(self.scope.add_new_local(node.expr.computed_type.name))
            self.scope.instructions.append(CILAssignNode(variable, var))
        else:
            variable = var
      
        local = self.scope.find_local(node.id.lex)

        if local is not None:
            if local.type == 'Object' and node.expr.computed_type.name in ['Int', 'Bool']:
                self.scope.instructions.append(CILAssignNode(CILVariableNode(local.id), CILBoxNode(variable, node.expr.computed_type.name)))
            else:
                self.scope.instructions.append(CILAssignNode(CILVariableNode(local.id), variable))
            return CILVariableNode(local.id)
        else:
            if self.scope.attributes[node.id.lex].type.name == 'Object' and node.expr.computed_type.name in ['Int', 'Bool']:
                var1 = CILVariableNode(self.scope.add_new_local('Object'))
                self.scope.instructions.append(CILAssignNode(var1, CILBoxNode(variable, node.expr.computed_type.name)))
                self.scope.instructions.append(CILSetAttributeNode(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.id.lex), var1))
            else:
                self.scope.instructions.append(CILSetAttributeNode(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.id.lex), variable))
            return CILGetAttribute(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.id.lex))
                                     
    @visitor.when(BinaryNode)
    def visit(self, node):
        expr_left = self.visit(node.left)
        expr_right = self.visit(node.right)
        if not isinstance(expr_left, CILAtomicNode):
            name = self.scope.add_new_local(node.left.computed_type.name)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr_left))
            left = CILVariableNode(name)
        else:
            left = expr_left 

        if not isinstance(expr_right, CILAtomicNode):
            name = self.scope.add_new_local(node.right.computed_type.name)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr_right))
            right = CILVariableNode(name)
        else:
            right = expr_right
        
        if isinstance(node, PlusNode):
            oper = CILPlusNode(left, right)
        elif isinstance(node, MinusNode):
            oper = CILMinusNode(left, right)
        elif isinstance(node, DivNode):
            oper = CILDivNode(left, right)
        elif isinstance(node, StarNode):
            oper = CILStarNode(left, right)
        elif isinstance(node, ElessNode):
            oper = CILElessNode(left, right)
        elif isinstance(node, LessNode):
            oper = CILLessNode(left, right)
        else:
            oper = CILEqualsNode(left, right, node.left.computed_type.ref)
        name = self.scope.add_new_local(node.computed_type.name)       
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name),oper))
        return CILVariableNode(name)

    @visitor.when(PrimeNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        name_exp = self.scope.add_new_local(node.expr.computed_type.name)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name_exp), expr))  
        name = self.scope.add_new_local(node.computed_type.name)   
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILMinusNode(CILNumberNode(0), CILVariableNode(name_exp))))
        return CILVariableNode(name)
   
    @visitor.when(NotNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        name_exp = self.scope.add_new_local(node.expr.computed_type.name)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name_exp), expr))  
        name = self.scope.add_new_local(node.computed_type.name)   
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILNotNode(CILVariableNode(name_exp))))
        return CILVariableNode(name)

    @visitor.when(StringNode)
    def visit(self, node):
        data = CILDataNode(f'str_{self.scope.str_count}', node.lex)
        self.scope.str_count += 1
        self.scope.data.append(data)
        name = self.scope.add_new_local('String')
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILLoadNode(data.id)))
        return CILVariableNode(name) 

    @visitor.when(IsVoidNode)
    def visit(self, node):
        expr = self.visit(node.expr)
        name = self.scope.add_new_local(node.computed_type.name)
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), expr))
        self.scope.instructions.append(CILArgNode(CILVariableNode(name)))
        name = self.scope.add_new_local("Bool")
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILCallNode("isvoid") ))
        return CILVariableNode(name)
    
    @visitor.when(ConstantNumNode)
    def visit(self, node):
        return CILNumberNode(node.lex)

    @visitor.when(VariableNode)
    def visit(self, node):
        local = self.scope.find_local(node.lex)
        if local is not None:
            return CILVariableNode(local.id)
        else:
            if node.lex == 'self':
                return CILVariableNode(f'self_{self.scope.current_class}')
            else:
                name = self.scope.add_new_local(node.computed_type.name)
                self.scope.instructions.append(CILAssignNode(CILVariableNode(name),CILGetAttribute(CILVariableNode(f'self_{self.scope.current_class}'), self.scope.current_class, CILVariableNode(node.lex))))
                return  CILVariableNode(name)
        
    @visitor.when(TrueNode)
    def visit(self, node):
        oper = CILEqualsNode(CILNumberNode(0), CILNumberNode(0), False)
        name = self.scope.add_new_local('Bool')       
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), oper))
        return CILVariableNode(name)

    @visitor.when(FalseNode)
    def visit(self, node):
        oper = CILEqualsNode(CILNumberNode(0), CILNumberNode(1), False)
        name = self.scope.add_new_local('Bool')       
        self.scope.instructions.append(CILAssignNode(CILVariableNode(name), oper))
        return CILVariableNode(name)
    
    @visitor.when(InstantiateNode)
    def visit(self, node):
        name = self.scope.add_new_local(node.lex)
        if node.lex in ["Bool", "Int"]:
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILNumberNode(0)))
        else:
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name),CILAllocateNode(CILTypeConstantNode(node.lex))))
            self.scope.instructions.append(CILArgNode(CILVariableNode(name)))
            name = self.scope.add_new_local(node.lex)
            self.scope.instructions.append(CILAssignNode(CILVariableNode(name), CILVCallNode(node.lex, f"Init_{node.lex}")))
        return  CILVariableNode(name) 