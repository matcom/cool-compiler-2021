from distutils.log import error
from semantic.semantic import AutoType, ErrorType, MethodError
from utils.errors import AttributexError, SemanticError, TypexError
from utils import visitor
from utils.utils import get_type, get_common_basetype
from utils.ast import *


class TypeChecker:
    def __init__(self, context, errors):
        self.context = context
        self.currentType = None
        self.currentMethod = None
        self.errors = errors
        self.currentIndex = None

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
            if not typex.conform_to(varType):
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

        return get_type(method.return_type, typex)

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

        return get_type(method.return_type, objType)

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

        return get_type(method.return_type, typex)

    def _get_type(self, ntype, pos):
        try:
            return self.context.get_type(ntype, pos)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    def _get_method(self, typex, name, pos):
        try:
            return typex.get_method(name, pos)
        except SemanticError:
            if type(typex) != ErrorType and type(typex) != AutoType:
                errorText = f'Dispatch to undefined method {name}.'
                self.errors.append(AttributexError(errorText, *pos))
            return MethodError(name, [], [], ErrorType())

    def _check_args(self, method, scope, args, pos):
        argTypes = [self.visit(arg, scope) for arg in args]

        if len(argTypes) > len(method.param_types):
            errorText = f'Method {method.name} called with wrong number of arguments.'
            self.errors.append(SemanticError(errorText, *pos))
        elif len(argTypes) < len(method.param_types):
            for arg, argInfo in zip(method.param_names[len(argTypes):], args[len(argTypes):]):
                errorText = f'Method {method.name} called with wrong number of arguments.'
                self.errors.append(SemanticError(errorText, *argInfo.pos))

        for argType, paramType, paramName in zip(argTypes, method.param_types, method.param_names):
            if not argType.conforms_to(paramType):
                errorText = f'In call of method {method.name}, type {argType.name} of parameter {paramName} does not conform to declared type {paramType.name}.'
                self.errors.append(TypexError(errorText, *pos))
