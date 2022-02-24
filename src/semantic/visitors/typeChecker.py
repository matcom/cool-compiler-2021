from cgi import print_directory
from semantic.semantic import AutoType, BoolType, ErrorType, IntType, MethodError, ObjectType, StringType, VariableInfo, VoidType
from utils.errors import AttributexError, SemanticError, TypexError
from utils import visitor
from utils.utils import get_type, get_common_basetype
from utils.ast import *


class TypeChecker:
    def __init__(self, context, errors):
        self.context = context
        self.currentType = None
        self.currentMethod = None
        self.currentIndex = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, programNode, scope):
        for i in range(0, len(programNode.declarations)):
            self.visit(programNode.declarations[i], scope.children[i])

    @visitor.when(ClassDeclarationNode)
    def visit(self, classDeclarationNode, scope):
        self.currentType = self.context.get_type(
            classDeclarationNode.id, (classDeclarationNode.line, classDeclarationNode.col))

        funcDeclarations = []
        for feature in classDeclarationNode.features:
            if isinstance(feature, AttrDeclarationNode):
                self.visit(feature, scope)
            else:
                funcDeclarations.append(feature)

        for funcDeclaration in funcDeclarations:
            self.visit(funcDeclaration, scope.functions[funcDeclaration.id])

    @visitor.when(FuncDeclarationNode)
    def visit(self, funcDeclarationNode, scope):
        parent = self.currentType.parent
        self.currentMethod = self.currentType.get_method(
            funcDeclarationNode.id, (funcDeclarationNode.line, funcDeclarationNode.col))

        method = self.currentMethod
        if parent is not None:
            try:
                oldMethod = parent.get_method(
                    funcDeclarationNode.id, (funcDeclarationNode.line, funcDeclarationNode.col))
                if oldMethod.return_type.name != method.return_type.name:
                    errorText = f'In redefined method {funcDeclarationNode.id}, return type {method.return_type.name} is different from original return type {oldMethod.return_type.name}.'
                    self.errors.append(SemanticError(
                        errorText, funcDeclarationNode.typeLine, funcDeclarationNode.typeCol))
                if len(method.param_names) != len(oldMethod.param_names):
                    errorText = f'Incompatible number of formal parameters in redefined method {funcDeclarationNode.id}.'
                    self.errors.append(SemanticError(
                        errorText, funcDeclarationNode.line, funcDeclarationNode.col))
                for (name, ptype, pline, pcol), type1, type2 in zip(funcDeclarationNode.params, method.param_types, oldMethod.param_types):
                    if type1.name != type2.name:
                        errorText = f'In redefined method {name}, parameter type {type1.name} is different from original type {type2.name}.'
                        self.errors.append(
                            SemanticError(errorText, pline, pcol))
            except:
                pass

        result = self.visit(funcDeclarationNode.body, scope)
        returnType = get_type(method.return_type, self.currentType)

        if not result.conforms_to(returnType):
            errorText = f'Inferred return type {result.name} of method test does not conform to declared return type {returnType.name}.'
            self.errors.append(TypexError(
                errorText, funcDeclarationNode.typeLine, funcDeclarationNode.typeCol))

    @visitor.when(AttrDeclarationNode)
    def visit(self, attrDeclarationNode, scope):
        attr = self.currentType.get_attribute(
            attrDeclarationNode.id, (attrDeclarationNode.line, attrDeclarationNode.col))
        attrType = get_type(attr.type, self.currentType)
        self.currentIndex = attr.index
        typex = self.visit(attrDeclarationNode.expr, scope)
        self.currentIndex = None

        if not typex.conforms_to(attrType):
            errorText = f'Inferred type {typex.name} of initialization of attribute {attr.name} does not conform to declared type {attrType.name}.'
            self.errors.append(TypexError(
                errorText, attrDeclarationNode.line, attrDeclarationNode.col))
            return ErrorType()

        return typex

    @visitor.when(VarDeclarationNode)
    def visit(self, varDeclarationNode, scope):
        varType = self._get_type(
            varDeclarationNode.type, (varDeclarationNode.line, varDeclarationNode.col))
        varType = get_type(varType, self.currentType)

        if varDeclarationNode.expr == None:
            return varType
        else:
            typex = self.visit(varDeclarationNode.expr, scope)
            if not typex.conforms_to(varType):
                errorText = f'Inferred type {typex.name} of initialization of {varDeclarationNode.id} does not conform to identifier\'s declared type {varType.name}.'
                self.errors.append(TypexError(
                    errorText, varDeclarationNode.typeLine, varDeclarationNode.typeCol))
            return typex

    @visitor.when(AssignNode)
    def visit(self, assignNode, scope):
        varInfo = self.find_variable(scope, assignNode.id)
        varType = get_type(varInfo.type, self.currentType)
        typex = self.visit(assignNode.expr, scope)

        if not typex.conforms_to(varType):
            errorText = f'Inferred type {typex.name} of initialization of {assignNode.id} does not conform to identifier\'s declared type {varType.name}.'
            self.errors.append(TypexError(
                errorText, assignNode.line, assignNode.col))

        assignNode.computed_type = typex
        return typex

    @visitor.when(ArrobaCallNode)
    def visit(self, arrobaCallNode, scope):
        objType = self.visit(arrobaCallNode.obj, scope)
        typex = self._get_type(
            arrobaCallNode.type, (arrobaCallNode.typeLine, arrobaCallNode.typeCol))

        if not objType.conforms_to(typex):
            errorText = f'Expression type {typex.name} does not conform to declared static dispatch type {objType.name}.'
            self.errors.append(TypexError(
                errorText, arrobaCallNode.typeLine, arrobaCallNode.typeCol))
            return ErrorType()

        method = self._get_method(
            typex, arrobaCallNode.id, (arrobaCallNode.line, arrobaCallNode.col))
        if not isinstance(method, MethodError):
            # check the args
            argTypes = [self.visit(arg, scope) for arg in arrobaCallNode.args]

            if len(argTypes) > len(method.param_types):
                errorText = f'Method {method.name} called with wrong number of arguments.'
                self.errors.append(SemanticError(
                    errorText, arrobaCallNode.line, arrobaCallNode.col))
            elif len(argTypes) < len(method.param_types):
                for arg, argInfo in zip(method.param_names[len(argTypes):], arrobaCallNode.args[len(argTypes):]):
                    errorText = f'Method {method.name} called with wrong number of arguments.'
                    self.errors.append(SemanticError(errorText, *argInfo.pos))

            for argType, paramType, paramName in zip(argTypes, method.param_types, method.param_names):
                if not argType.conforms_to(paramType):
                    errorText = f'In call of method {method.name}, type {argType.name} of parameter {paramName} does not conform to declared type {paramType.name}.'
                    self.errors.append(TypexError(
                        errorText, arrobaCallNode.line, arrobaCallNode.col))

        arrobaCallNode.computed_type = get_type(method.return_type, TypexError)
        return arrobaCallNode.computed_type

    @visitor.when(DotCallNode)
    def visit(self, dotCallNode, scope):
        objType = self.visit(dotCallNode.obj, scope)
        method = self._get_method(
            objType, dotCallNode.id, (dotCallNode.line, dotCallNode.col))
        if not isinstance(method, MethodError):
            # check the args
            argTypes = [self.visit(arg, scope) for arg in dotCallNode.args]

            if len(argTypes) > len(method.param_types):
                errorText = f'Method {method.name} called with wrong number of arguments.'
                self.errors.append(SemanticError(
                    errorText, dotCallNode.line, dotCallNode.col))
            elif len(argTypes) < len(method.param_types):
                for arg, argInfo in zip(method.param_names[len(argTypes):], dotCallNode.args[len(argTypes):]):
                    errorText = f'Method {method.name} called with wrong number of arguments.'
                    self.errors.append(SemanticError(errorText, *argInfo.pos))

            for argType, paramType, paramName in zip(argTypes, method.param_types, method.param_names):
                if not argType.conforms_to(paramType):
                    errorText = f'In call of method {method.name}, type {argType.name} of parameter {paramName} does not conform to declared type {paramType.name}.'
                    self.errors.append(TypexError(
                        errorText, dotCallNode.line, dotCallNode.col))

        dotCallNode.computed_type = get_type(method.return_type, objType)
        return dotCallNode.computed_type

    @visitor.when(MemberCallNode)
    def visit(self, memberCallNode, scope):
        typex = self.currentType
        method = self._get_method(
            typex, memberCallNode.id, (memberCallNode.line, memberCallNode.col))
        if not isinstance(method, MethodError):
            # check the args
            argTypes = [self.visit(arg, scope) for arg in memberCallNode.args]

            if len(argTypes) > len(method.param_types):
                errorText = f'Method {method.name} called with wrong number of arguments.'
                self.errors.append(SemanticError(
                    errorText, memberCallNode.line, memberCallNode.col))
            elif len(argTypes) < len(method.param_types):
                for arg, argInfo in zip(method.param_names[len(argTypes):], memberCallNode.args[len(argTypes):]):
                    errorText = f'Method {method.name} called with wrong number of arguments.'
                    self.errors.append(SemanticError(errorText, *argInfo.pos))

            for argType, paramType, paramName in zip(argTypes, method.param_types, method.param_names):
                if not argType.conforms_to(paramType):
                    errorText = f'In call of method {method.name}, type {argType.name} of parameter {paramName} does not conform to declared type {paramType.name}.'
                    self.errors.append(TypexError(
                        errorText, memberCallNode.line, memberCallNode.col))

        memberCallNode.static_type = typex
        memberCallNode.computed_type = get_type(method.return_type, typex)
        return memberCallNode.computed_type

    @visitor.when(IfThenElseNode)
    def visit(self, ifThenElseNode, scope):
        conditionType = self.visit(ifThenElseNode.condition, scope)
        if conditionType.name != 'Bool':
            errorText = f'Predicate of \'if\' does not have type Bool.'
            self.errors.append(TypexError(
                errorText, ifThenElseNode.line, ifThenElseNode.col))

        ifBodyType = self.visit(ifThenElseNode.ifBody, scope)
        elseBodyType = self.visit(ifThenElseNode.elseBody, scope)

        ifThenElseNode.computed_type = get_common_basetype(
            [ifBodyType, elseBodyType])
        return ifThenElseNode.computed_type

    @visitor.when(WhileNode)
    def visit(self, whileNode, scope):
        conditionType = self.visit(whileNode.condition, scope)
        if conditionType.name != 'Bool':
            errorText = 'Loop condition does not have type Bool.'
            self.errors.append(TypexError(
                errorText, whileNode.line, whileNode.col))
        self.visit(whileNode.body, scope)

        whileNode.computed_type = ObjectType()
        return ObjectType()

    @visitor.when(BlockNode)
    def visit(self, blockNode, scope):
        typex = None
        for expr in blockNode.exprs:
            typex = self.visit(expr, scope)

        blockNode.computed_type = typex
        return typex

    @visitor.when(LetInNode)
    def visit(self, letInNode, scope):
        childScope = scope.expr_dict[letInNode]
        for letDeclaration in letInNode.letBody:
            self.visit(letDeclaration, childScope)

        typex = self.visit(letInNode.inBody, childScope)
        letInNode.computed_type = typex
        return typex

    @visitor.when(CaseNode)
    def visit(self, caseNode, scope):
        exprType = self.visit(caseNode.expr, scope)
        newScope = scope.expr_dict[caseNode]
        types = []
        checkDuplicate = []
        for option, optionScope in zip(caseNode.optionList, newScope.children):
            optionType = self.visit(option, optionScope)
            types.append(optionType)
            if option.type in checkDuplicate:
                errorText = f'Duplicate branch {option.type} in case statement.'
                self.errors.append(SemanticError(
                    errorText, option.typeLine, option.typeCol))
            checkDuplicate.append(option.type)

        caseNode.computed_type = get_common_basetype(types)
        return caseNode.computed_type

    @visitor.when(CaseOptionNode)
    def visit(self, caseOptionNode, scope):
        optionType = self.visit(caseOptionNode.expr, scope)
        caseOptionNode.computed_type = optionType
        return optionType

    @visitor.when(PlusNode)
    def visit(self, plusNode, scope):
        leftType = self.visit(plusNode.lvalue, scope)
        rightType = self.visit(plusNode.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} + {rightType.name} .'
            self.errors.append(TypexError(
                errorText, plusNode.line, plusNode.col))
            return ErrorType()

        plusNode.computed_type = IntType()
        return IntType()

    @visitor.when(MinusNode)
    def visit(self, minusNode, scope):
        leftType = self.visit(minusNode.lvalue, scope)
        rightType = self.visit(minusNode.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} - {rightType.name} .'
            self.errors.append(TypexError(
                errorText, minusNode.line, minusNode.col))
            return ErrorType()

        minusNode.computed_type = IntType()
        return IntType()

    @visitor.when(StarNode)
    def visit(self, starNode, scope):
        leftType = self.visit(starNode.lvalue, scope)
        rightType = self.visit(starNode.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} * {rightType.name} .'
            self.errors.append(TypexError(
                errorText, starNode.line, starNode.col))
            return ErrorType()

        starNode.computed_type = IntType()
        return IntType()

    @visitor.when(DivNode)
    def visit(self, divNode, scope):
        leftType = self.visit(divNode.lvalue, scope)
        rightType = self.visit(divNode.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} / {rightType.name} .'
            self.errors.append(TypexError(
                errorText, divNode.line, divNode.col))
            return ErrorType()

        divNode.computed_type = IntType()
        return IntType()

    @visitor.when(LessNode)
    def visit(self, lessNode, scope):
        leftType = self.visit(lessNode.lvalue, scope)
        rightType = self.visit(lessNode.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} < {rightType.name} .'
            self.errors.append(TypexError(
                errorText, lessNode.line, lessNode.col))
            return ErrorType()

        lessNode.computed_type = BoolType()
        return BoolType()

    @visitor.when(LessEqNode)
    def visit(self, lessEq, scope):
        leftType = self.visit(lessEq.lvalue, scope)
        rightType = self.visit(lessEq.rvalue, scope)
        if leftType != IntType() or rightType != IntType():
            errorText = f'non-Int arguments: {leftType.name} <= {rightType.name} .'
            self.errors.append(TypexError(
                errorText, lessEq.line, lessEq.col))
            return ErrorType()

        lessEq.computed_type = BoolType()
        return BoolType()

    @visitor.when(EqualNode)
    def visit(self, equalNode, scope):
        leftType = self.visit(equalNode.lvalue, scope)
        rightType = self.visit(equalNode.rvalue, scope)
        if (leftType != rightType) and (leftType in [IntType(), StringType(), BoolType()] or rightType in [IntType(), StringType(), BoolType()]):
            errorText = 'Illegal comparison with a basic type.'
            self.errors.append(TypexError(
                errorText, equalNode.line, equalNode.col))
            return ErrorType()

        equalNode.computed_type = BoolType()
        return BoolType()

    @visitor.when(NegationNode)
    def visit(self, negationNode, scope):
        exprType = self.visit(negationNode.expr, scope)
        if exprType != IntType():
            errorText = f'Argument of \'~\' has type {exprType.name} instead of {IntType().name}.'
            self.errors.append(TypexError(
                errorText, negationNode.line, negationNode.col))
            return ErrorType()

        negationNode.computed_type = IntType()
        return IntType()

    @visitor.when(LogicNegationNode)
    def visit(self, logicNegationNode, scope):
        exprType = self.visit(logicNegationNode.expr, scope)
        if exprType != BoolType():
            errorText = f'Argument of \'not\' has type {exprType.name} instead of {BoolType().name}.'
            self.errors.append(TypexError(
                errorText, logicNegationNode.line, logicNegationNode.col))
            return ErrorType()

        logicNegationNode.computed_type = BoolType()
        return BoolType()

    @visitor.when(IsVoidNode)
    def visit(self, isVoidNode, scope):
        self.visit(isVoidNode.expr, scope)
        isVoidNode.computed_type = BoolType()
        return BoolType()

    @visitor.when(NewNode)
    def visit(self, newNode, scope):
        try:
            typex = self.context.get_type(
                newNode.id, (newNode.line, newNode.col))
        except:
            typex = ErrorType()
            errorText = f'\'new\' used with undefined class {newNode.id}.'
            self.errors.append(TypexError(
                errorText, newNode.line, newNode.col))

        typex = get_type(typex, self.currentType)
        newNode.computed_type = typex
        return typex

    @visitor.when(IdNode)
    def visit(self, idNode, scope):
        varType = self.find_variable(scope, idNode.id).type
        typex = get_type(varType, self.currentType)
        idNode.computed_type = typex
        return typex

    @visitor.when(IntNode)
    def visit(self, intNode, scope):
        intNode.computed_type = IntType((intNode.line, intNode.col))
        return intNode.computed_type

    @visitor.when(BoolNode)
    def visit(self, boolNode, scope):
        boolNode.computed_type = BoolType((boolNode.line, boolNode.col))
        return boolNode.computed_type

    @visitor.when(StringNode)
    def visit(self, stringNode, scope):
        stringNode.computed_type = StringType(
            (stringNode.line, stringNode.col))
        return stringNode.computed_type

    @visitor.when(VoidNode)
    def visit(self, voidNode, scope):
        voidNode.computed_type = VoidType((voidNode.line, voidNode.col))
        return voidNode.computed_type

    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    def _get_method(self, typex, name, pos):
        typex = self.context.get_type(typex.name)
        try:
            return typex.get_method(name, pos)
        except SemanticError:
            if type(typex) != ErrorType and type(typex) != AutoType:
                errorText = f'Dispatch to undefined method {name}.'
                self.errors.append(AttributexError(errorText, *pos))
            return MethodError(name, [], [], ErrorType())

    def find_variable(self, scope, lex):
        var_info = scope.find_local(lex)
        if var_info is None:
            var_info = scope.find_attribute(lex)
        if lex in self.currentType.attributes and var_info is None:
            return VariableInfo(lex, VoidType())
        return var_info
