from cool_ast.cool_ast import *
import visitors.visitor as visitor
from utils.semantic import *
from utils.digraph import *

class Inferencer:
    def __init__(self, context, errors):
        self.context = context
        self.errors = errors
        self.dGraph = DGraph()
        self.attributes = { }
        self.vars = { }
        self.methods = { }
        
        self.currentType = None
        self.currentMethod = None
        self.defaultType = self.context.get_type('Object')
        
        for t in context.types.values():
            for attr in t.attributes:
                self.attributes[t.name, attr.name] = AttrNode(t, attr)
            for m in t.methods:
            
                paramNodesList = [ ]
                for index, ptype in enumerate(m.param_types):
                    paramNodesList.append(ParamNode(ptype, m, index))
                self.methods[t.name,m.name] = (paramNodesList, RTypeNode(m.return_type,m))
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)#
    def visit(self, node):
        scope = Scope()
        for _classDeclaration in node.declarations:
            self.visit(_classDeclaration, scope.create_child())
            
        self.dGraph.Build(self.defaultType)
        backtracker = Backtracker(self.context, self.errors)
        backtracker.visit(node, scope)
        
    @visitor.when(ClassDeclarationNode)#
    def visit(self, node, scope):
        self.currentType = self.context.get_type(node.id)
        
        for feature in node.features:
            if isinstance(feature,AttrDeclarationNode):
                self.visit(feature, scope)
            else:
                self.visit(feature, scope.create_child())

    @visitor.when(AttrDeclarationNode)#
    def visit(self, node, scope):
        #crear un nodo del digrafo con la informacion del atributo encapsulada en un VarNode
        attrType = self.context.get_type(node.type)
        attr = scope.define_variable(node.id, attrType)
        self.vars[attr] = VarNode(attrType, attr)
        # self.vars[attr] = VarNode(self.context.get_type('AUTO_TYPE'), attr) ??
        varNode = self.vars[attr]
        
        attrValueNode = None
        if node.value is not None:
            attrValueNode = self.visit(node.value, scope.create_child())
            
        if node.type == 'AUTO_TYPE':
            attrNode = self.attributes[self.currentType.name, node.id]
            self.dGraph.AddEdge(attrNode, varNode)
            self.dGraph.AddEdge(varNode, attrNode)
            if attrValueNode is not None:
                self.dGraph.AddEdge(attrValueNode, varNode)
                self.dGraph.AddEdge(varNode, attrValueNode)
                
    @visitor.when(FuncDeclarationNode)#
    def visit(self, node, scope):
        #el scope se pasa como un scope hijo del anterior, asi que toca definir self como variable
        node.type = self.context.get_type(node.type)
        _self = scope.define_variable('self', self.currentType)
        self.vars[_self] = VarNode(self.currentType, _self)
        
        #ahora recorrer los parametros del metodo en busca de AUTO_TYPES para agregarlos al digrafo
        self.currentMethod = self.currentType.get_method(node.id, self.currentType, False)
        paramNodeList, _returnTypeNode = self.methods[self.currentType.name, self.currentMethod.name]
        
        
        # for i, (_paramName, _paramType) in enumerate(zip(self.currentMethod.param_names, self.currentMethod.param_types)):
        for i in range(len(self.currentMethod.param_names)): #param_names.Length = param_types.Length
            #i -> indice del parametro en la lista de parametros
            _ithParamName = self.currentMethod.param_names[i]
            _ithParamType = self.currentMethod.param_types[i]
            
            #definir los parametros como variables locales, sobrescribiendo cualquier referencia a una variable de mismo nombre en un scope padre
            ithParam = scope.define_variable(_ithParamName, _ithParamType)
            self.vars[ithParam] = VarNode(_ithParamType, ithParam)
            ithParamVarNode = self.vars[ithParam]
            
            if _ithParamType.name == 'AUTO_TYPE':
                paramNode = paramNodeList[i]
                self.dGraph.AddEdge(ithParamVarNode, paramNode)
                self.dGraph.AddEdge(paramNode, ithParamVarNode)
        
        
        
        methodBodyNode = self.visit(node.body, scope)
        if _returnTypeNode.type.name == 'AUTO_TYPE':
            self.dGraph.AddEdge(methodBodyNode, _returnTypeNode)
    
    @visitor.when(TrueNode)#
    def visit(self, node, scope):
        _type = self.context.get_type('Bool')
        return PrimeNode(_type)
    
    @visitor.when(FalseNode)#
    def visit(self, node, scope):
        _type = self.context.get_type('Bool')
        return PrimeNode(_type)
    
    @visitor.when(ConstantNumNode)#
    def visit(self, node, scope):
        _type = self.context.get_type('Int')
        return PrimeNode(_type)
    
    @visitor.when(StringNode)#
    def visit(self, node, scope):
        _type = self.context.get_type('String')
        return PrimeNode(_type)
    
    @visitor.when(NotNode)#
    def visit(self, node, scope):
        n = self.visit(node.expression, scope)
        _type = self.context.get_type('Bool')
        return PrimeNode(_type)
    
    @visitor.when(ComplementNode)#
    def visit(self, node, scope):
        n = self.visit(node.expr, scope)
        _type = self.context.get_type('Int')
        return PrimeNode(_type)
    
    @visitor.when(PlusNode)#
    def visit(self, node, scope):
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(intType)
        
    @visitor.when(MinusNode)#
    def visit(self, node, scope):
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(intType)
    
    @visitor.when(StarNode)#
    def visit(self, node, scope):
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(intType)
    
    @visitor.when(DivNode)#
    def visit(self, node, scope):
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(intType)
    
    @visitor.when(EqualNode)#
    def visit(self, node, scope):
        boolType = self.context.get_type('Bool')
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        return PrimeNode(boolType)
    
    @visitor.when(LessNode)#
    def visit(self, node, scope):
        boolType = self.context.get_type('Bool')
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(boolType)
    
    @visitor.when(LeqNode)#
    def visit(self, node, scope):
        boolType = self.context.get_type('Bool')
        intType = self.context.get_type('Int')
        
        left = self.visit(node.left, scope)
        right = self.visit(node.right, scope)
        
        intPrimeNode = PrimeNode(intType)
        
        if not isinstance(left, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, left)
            
        if not isinstance(right, PrimeNode):
            self.dGraph.AddEdge(intPrimeNode, right)
        
        return PrimeNode(boolType)
    
    @visitor.when(WhileNode)#
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        self.visit(node.loopChunk, scope.create_child())
        return PrimeNode(self.defaultType) #The predicate must have static type Bool. The body may have any static type. The static type of a loop expression is Object section 7.6
    
    @visitor.when(CallNode)#
    def visit(self, node, scope):
        node.obj = node.obj if node.obj is not None else VariableNode('self')
        _node = self.visit(node.obj, scope)
        if isinstance(_node, PrimeNode):
            # if _node.type.name == 'SELF_TYPE':
            #     _method_type = self.context.get_type(node.parent) if node.parent is not None else self.currentType
            #     _function, _obj = _method_type.get_method(node.method, _method_type, False, True)
            # else:
            #     _method_type = self.context.get_type(node.parent) if node.parent is not None else _node.type
            #     _function, _obj = _method_type.get_method(node.method, _method_type, False, True)
            _method_type = self.context.get_type(node.parent) if node.parent is not None else _node.type
            _function, _obj = _method_type.get_method(node.method, _method_type, False, True)
            paramNodeList, _returnTypeNode = self.methods[_obj.name, _function.name]
            for i in range(len(node.args)):
                _ithFuncParam = paramNodeList[i]
                _ithArg = node.args[i]
                _ithArgNode = self.visit(_ithArg, scope)
                if not isinstance(_ithArgNode, PrimeNode):
                    if _ithFuncParam.type.name == 'AUTO_TYPE':
                        self.dGraph.AddEdge(_ithFuncParam, _ithArgNode)
                    else:
                        self.dGraph.AddEdge(_ithFuncParam, _ithArgNode)
                        self.dGraph.AddEdge(_ithArgNode, _ithFuncParam)
                elif isinstance(_ithArgNode, PrimeNode) and _ithFuncParam.type.name == 'AUTO_TYPE':
                        self.dGraph.AddEdge(_ithArgNode, _ithFuncParam)
            if _returnTypeNode.type.name == 'AUTO_TYPE':
                return _returnTypeNode
            if _returnTypeNode.type.name == 'SELF_TYPE':
                return PrimeNode(_node.type)
            return PrimeNode(_returnTypeNode.type)
        
        
        
        for _arg in node.args:
            self.visit(_arg, scope)
        return PrimeNode(self.defaultType)
    
    @visitor.when(ConditionalNode)#
    def visit(self, node, scope):
        thenChunkNode = self.visit(node.thenChunk, scope.create_child())
        elseChunkNode = self.visit(node.elseChunk, scope.create_child())
        
        ifChunkNode = self.visit(node.ifChunk, scope)
        if not isinstance(ifChunkNode, PrimeNode):
            _boolType = self.context.get_type('Bool')
            _auxBoolNode = PrimeNode(_boolType)
            self.dGraph.AddEdge(_auxBoolNode,ifChunkNode)
        
        
        if isinstance(thenChunkNode, PrimeNode) and isinstance(elseChunkNode, PrimeNode):
            #sea x el tipo del trozo 'then', sea ademas y el tipo del trozo 'else'
            #el tipo de la expresion if completa es el "menor" tipo t, tal que x e y conformen a t
            #according to COOL Reference Manual page 10 section 7.5 
            
            tType = thenChunkNode.type
            eType = thenChunkNode.type
            
            while not isinstance(tType, Type):
                tType = tType.type
            while not isinstance(eType, Type):
                eType = eType.type
            
            ancestorType = tType.join(eType)
            return PrimeNode(ancestorType)
        
        else:
            #sad
            return PrimeNode(self.defaultType)
        
    @visitor.when(LetInNode)#
    def visit(self, node, scope):
        #definir cada una de las variables de node.decl_list en el scope y luego visitar la expresion
        for d in node.decl_list:
            # _varName = node.decl_list[i].id
            # _varTypeName = node.decl_list[i].type
            # _varValue = node.decl_list[i].expr
            try:
                _varType = self.context.get_type(d.type)
                _var = scope.define_variable(d.id, _varType)
            except: #si el type no existe.......
                _var = scope.define_variable(d.id, ErrorType()) #error type de semantic.py para modelar estos casos
            self.vars[_var] = VarNode(_var.type, _var)
            _varNode = self.vars[_var]
            
            _varValueNode = None
            if d.expr is not None:
                _varValueNode = self.visit(d.expr, scope.create_child())
            
            if d.type == 'AUTO_TYPE':
                if _varValueNode is None:
                    self.dGraph.CreateNode(_varNode)
                else:
                    self.dGraph.AddEdge(_varValueNode, _varNode)
        #no use la variable i del enumerate, asi que cuando deje de debuggear se puede quitar
        
        _inScope = scope.create_child()
        return self.visit(node.expression, _inScope)
        
    @visitor.when(SwitchCaseNode)#
    def visit(self, node, scope):
        _caseExpr0Node = self.visit(node.expr, scope)
        _cases = []
        for _ithVarName, _ithTypeName, _ithExpr in node.case_list:
            _ithVarType = self.context.get_type(_ithTypeName)
            _ithScope = scope.create_child()
            _ithVar = _ithScope.define_variable(_ithVarName, _ithVarType)
            self.vars[_ithVar] = VarNode(_ithVarType, _ithVar)
            _cases.append(self.visit(_ithExpr,_ithScope))
        
        #jachtagsad
        lca = _cases[0].type #todo switch case tiene al menos un case
        if lca.name == 'AUTO_TYPE': #ehhhhhhhhhhh
            return PrimeNode(self.defaultType)
        for other_case in _cases[1:]:
            if other_case.type.name == 'AUTO_TYPE': #ehhhhhhhhhhhh
                return PrimeNode(self.defaultType)
            lca.join(other_case.type)
        return PrimeNode(lca)
    
    @visitor.when(ChunkNode)#
    def visit(self, node, scope):
        innerScope = scope.create_child()
        #exprNode = [ ]
        #if
        exprNodes = [self.visit(i, innerScope) for i in node.chunk]
        return exprNodes[-1] if exprNodes else None
    
    @visitor.when(AssignNode)#
    def visit(self, node, scope):
        var = scope.find_variable(node.id)
        valueNode = self.visit(node.expr, scope.create_child())
        
        #THE PARCHE
        # if valueNode.type.name == 'SELF_TYPE' and isinstance(node.expr, CallNode) and node.expr.obj is not None:
        #     try:
        #         rType = scope.find_variable(node.expr.obj.lex).type if node.expr.parent is None else self.context.get_type(node.expr.parent)
        #     except:
        #         rType = self.context.get_type(node.expr.obj.lex) if node.expr.parent is None else self.context.get_type(node.expr.parent)
        #     if self.currentType.conforms_to(rType):
        #         pass
        #     else:
        #         valueNode = PrimeNode(rType)
        
        if var is not None: #cuando es None es xq esa variable no existe, y ese error no toca detectarlo ahora
            _var = self.vars[var]
            if var.type.name == "AUTO_TYPE" and valueNode.type.name == 'AUTO_TYPE':
                self.dGraph.AddEdge(_var, valueNode)
                self.dGraph.AddEdge(valueNode, _var)
            if var.type.name == "AUTO_TYPE" and valueNode.type.name != 'AUTO_TYPE':
                self.dGraph.AddEdge(valueNode, _var)
            if var.type.name != "AUTO_TYPE" and valueNode.type.name == 'AUTO_TYPE':
                self.dGraph.AddEdge(_var, valueNode)
        return valueNode
    
    @visitor.when(IsVoidNode)#
    def visit(self, node, scope):
        n = self.visit(node.method, scope)
        _type = self.context.get_type('Bool')
        return PrimeNode(_type)
    
    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        _type = self.context.get_type(node.lex)
        return PrimeNode(_type)
    
    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if node.lex == 'self' :
            _var = PrimeNode(self.currentType)
        else:
            _var = scope.find_variable(node.lex)
            if _var is None:
                _var = self.currentType.get_attribute(node.lex, self.currentType, False)
        
        if _var.type.name == 'AUTO_TYPE':
            return self.vars[_var]
        
        return PrimeNode(_var.type)
    
    
class Backtracker:
    def __init__(self, context, errors):
        self.errors = errors
        self.context = context
        self.defaultType = self.context.get_type('Object')
        self.currentType = self.defaultType
        self.autoType = self.context.get_type('AUTO_TYPE')
        
    @visitor.on('node')
    def visit(self, node, scope):
        pass
    
    @visitor.when(ProgramNode)#
    def visit(self, node, scope):
        for i in range(len(node.declarations)):
            _ithScope = scope.children[i]
            self.visit(node.declarations[i], _ithScope)
        
        return scope
    
    @visitor.when(ClassDeclarationNode)#
    def visit(self, node, scope):
        # attrIndex = 0
        index = 0
        
        self.currentType = self.context.get_type(node.id)
        
        for feature in node.features:
            if isinstance(feature, AttrDeclarationNode):
                if feature.value is not None:
                    feature._auxIndex = index
                    index += 1
                self.visit(feature, scope)
            
            else:   #funcDeclaration
                _ithMethodScope = scope.children[index]
                index += 1
                self.visit(feature,_ithMethodScope)
                
    @visitor.when(AttrDeclarationNode)#
    def visit(self, node, scope):
        _var = scope.find_variable(node.id)
        _type = self.context.get_type(node.type)
        if node.value is not None:
            self.visit(node.value, scope.children[node._auxIndex])
        if _type == self.autoType:
            if _var.type == self.autoType:
                self.errors.append(f'Unable to infer the type of {node.id}')
            node.type = _var.type.name

    @visitor.when(FuncDeclarationNode)#
    def visit(self, node, scope):
        _func = self.currentType.get_method(node.id, self.currentType, False)
        
        for i in range(len(node.params)):
            _ithParamName = node.params[i][0]
            _param = scope.find_variable(_ithParamName)
            if _param.type == self.autoType:
                self.errors.append(f'Unable to infer the type of {_param.name}')
            node.params[i] = (_ithParamName, _param.type.name)
        self.visit(node.body, scope)
        
        if self.context.get_type(node.type.name) == self.autoType:
            if _func.return_type == self.autoType:
                self.errors.append(f'Unable to infer the type of {_func.name}')
            node.type = _func.return_type.name # .name?
        elif isinstance(node.type, Type):
            node.type = node.type.name
        
    @visitor.when(ConditionalNode)#
    def visit(self, node, scope):
        _thenScope = scope.children[0]
        _elseScope = scope.children[1]
        
        
        self.visit(node.ifChunk, scope)
        self.visit(node.thenChunk, _thenScope)
        self.visit(node.elseChunk, _elseScope)
        
    @visitor.when(ChunkNode)#
    def visit(self, node, scope):
        for expr in node.chunk:
            self.visit(expr, scope.children[0])
            
    @visitor.when(CallNode)#
    def visit(self, node, scope):
        self.visit(node.obj, scope)
        for _arg in node.args:
            self.visit(_arg, scope)
            
    @visitor.when(LetInNode)#
    def visit(self, node, scope):
        count = 0
        for decl in node.decl_list:
            expr = decl.expr
            if expr is not None:
                self.visit(expr, scope.children[count])
                count += 1
                
        for d in node.decl_list:
            _var = scope.find_variable(d.id)
            if d.type == 'AUTO_TYPE':
                if _var.type == self.autoType:
                    self.errors.append(f'Unable to infer the type of {_var.name}')
                while not isinstance(_var.type, Type):
                    _var.type = _var.type.type
                d.type = _var.type.name
                

        # for i in range(len(node.decl_list)):
        #     _ithName, _ithTypeName, _value = node.decl_list[i]
        #     _ithVar = scope.find_variable(_ithName)
        #     if _ithTypeName == 'AUTO_TYPE':
        #         if _ithVar.type == self.autoType:
        #             self.errors.append(f'Unable to infer the type of {_ithVar.name}')
        #         node.decl_list[i] = (_ithName, _ithVar.type.name, _value)
    
    @visitor.when(SwitchCaseNode)#
    def visit(self, node, scope):
        self.visit(node.expr, scope)
        for i in range(len(node.case_list)):
            self.visit(node.case_list[i][2], scope.children[i])
            
    @visitor.when(WhileNode)#
    def visit(self, node, scope):
        self.visit(node.condition, scope)
        self.visit(node.loopChunk, scope.children[0])
        
    @visitor.when(BinaryNode)#
    def visit(self, node, scope):
        self.visit(node.left, scope)
        self.visit(node.right, scope)
        
    @visitor.when(AtomicNode)#
    def visit(self, node, scope):
        pass
        
    @visitor.when(AssignNode)#
    def visit(self, node, scope):
        self.visit(node.expr, scope.children[0])