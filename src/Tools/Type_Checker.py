from .Tools import visitor
from .Parser import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode,\
                   IfThenElseNode, WhileLoopNode, BlockNode, LetInNode, CaseOfNode,\
                   AssignNode, LessEqualNode, LessNode, EqualNode, ArithmeticNode,\
                   NotNode, IsVoidNode, ComplementNode, FunctionCallNode, MemberCallNode, NewNode,\
                   IntegerNode, IdNode, StringNode, BoolNode
from .Tools.Semantic import Context, Scope, SelfType, SemanticException, ErrorType
from .Tools.Errors import *

# Este es el visitor encargado de terminar el chequeo semantico.
# Revisa la compatibilidad de tipos, la compatibilidad en la herencia,
# que las variables hayan sido previamente definidas, asi como los
# metodos y atributos de clase, crea el scope para las variables, el
# cual sera rehusado para inferir las variables que se requieran.
# Observar que cada vez que el visitor llama recursivamente crea un scope
# hijo en el scope actual, esto se hace para que las variables previamente
# declaradas en ambitos hermanos no sean utiles en el ambito actual.

class Type_Checker:

    def __init__(self, Context : Context):
        self.Context = Context
        self.errors = []
        self.Current_Type = None
        self.Current_Method = None

        self.Object_Type = self.Context.get_type('Object')
        self.IO_Type = self.Context.get_type('IO')
        self.String_Type = self.Context.get_type('String')
        self.Int_Type = self.Context.get_type('Int')
        self.Bool_Type = self.Context.get_type('Bool')

        self.builtin_Types = [
            self.Object_Type,
            self.IO_Type,
            self.String_Type,
            self.Int_Type,
            self.Bool_Type
        ]

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode, scope : Scope = None):
        scope = Scope()
        for declaration in node.declarations:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(ClassDeclarationNode)
    def visit(self, node : ClassDeclarationNode, scope : Scope):
        self.Current_Type = self.Context.get_type(node.id.lex)

        # Incluyo cada uno de los atributos de los padres en su resoectivo orden
        current = self.Current_Type
        attributtes = []
        while current.parent:
            current = current.parent
            for att in reversed(current.attributes):
                attributtes.append(att)

        for att in reversed(attributtes):    
            scope.define_variable(att.name, att.type, att.line, att.column)

        for att in self.Current_Type.attributes:
            if scope.is_defined(att.name):
                self.errors.append(SemanticError(att.line, att.column,
                     f'Attribute {att.name} is an attribute of an inherited class'))
            scope.define_variable(att.name, att.type, att.line, att.column)

        for feature in node.features:
            self.visit(feature, scope.create_child())
        node.static_type = self.Current_Type

    @visitor.when(AttrDeclarationNode)
    def visit(self, node : AttrDeclarationNode, scope : Scope):
        expr = node.expression
        attr = self.Current_Type.get_attribute(node.id.lex)
        node_type = self.Current_Type if attr.type is SelfType else attr.type
        
        if expr:
            self.visit(expr, scope.create_child())
            expr_type = expr.static_type

            # Chequeo compatibilidad de tipos
            if not expr_type.conforms_to(node_type):
                self.errors.append(TypeError(node.expression.line, node.expression.column,
                     f'Inferred type {expr_type.name} of initialization of attribute {attr.name} '
                     f'does not conform to declared type {node_type.name}'))

        if attr.name.lower() == 'self':
            self.errors.append(SemanticError(node.line, node.column,
                         '\'self\' cannot be the name of an attribute'))

        node.static_type = node_type

    @visitor.when(FuncDeclarationNode)
    def visit(self, node : FuncDeclarationNode, scope : Scope):
        self.Current_Method = self.Current_Type.get_method(node.id.lex)
        
        if self.Current_Type.parent:
            try:
                inherited_method = self.Current_Type.parent.get_method(node.id.lex)
                
                if len(self.Current_Method.param_names) != len(inherited_method.param_names):
                    self.errors.append(SemanticError(node.line, node.column,
                         f'Incompatible number of formal parameters in redefined method {self.Current_Method.name}'))
                else:
                    for par1, par2, p in zip(self.Current_Method.param_types, inherited_method.param_types, node.params):
                        if par1.name != par2.name:
                            self.errors.append(SemanticError(p[0].line, p[0].column,
                                f'In redefined method {self.Current_Method.name}, parameter type {par1.name} '
                                f'is different from original type {par2.name}'))
                            
                if self.Current_Method.return_type.name != inherited_method.return_type.name:
                    self.errors.append(SemanticError(node.line, node.column,
                         f'In redefined method {self.Current_Method.name}, return type {self.Current_Method.return_type.name} '
                         f'is different from original return type {inherited_method.return_type.name}'))
                
            except SemanticException:
                pass

        scope.define_variable('self', self.Current_Type, node.line, node.column)

        # Defino cada uno de los parametros de metodo
        for pname, ptype in zip(self.Current_Method.param_names, self.Current_Method.param_types):
            scope.define_variable(pname, ptype, node.line, node.column)

            if pname.lower() == 'self':
                self.errors.append(SemanticError(node.line, node.column,
                         '\'self\' cannot be the name of a formal parameter'))

        # Chequeo consistencia en el cuerpo del metodo
        self.visit(node.body, scope.create_child())

        expr_type = node.body.static_type
        return_type = self.Current_Method.return_type

        # Chequeo consistencia entre el tipo de retorno definido y el tipo de retorno
        # del cuerpo del metodo
        if not expr_type.conforms_to(return_type):
            self.errors.append(TypeError(node.line, node.column,
                 f'Inferred return type {expr_type.name} of method {self.Current_Method.name} '
                 f'does not conform to declared return type {return_type.name}'))
        node.static_type = return_type

    @visitor.when(IfThenElseNode)
    def visit(self, node : IfThenElseNode, scope : Scope):
        # Chequeo consistencia en la condicion del if
        self.visit(node.condition, scope.create_child())

        condition_type = node.condition.static_type
        # Chequeo que el tipo de la condicion sea booleano
        if not condition_type.conforms_to(self.Bool_Type):
            self.errors.append(TypeError(node.condition.line, node.condition.column,
                 'Predicate of \'if\' does not have type Bool'))

        # Chequeo consistencia en las expresiones del then y el else
        self.visit(node.if_body, scope.create_child())
        self.visit(node.else_body, scope.create_child())

        if_type = node.if_body.static_type
        else_type = node.else_body.static_type

        node.static_type = if_type.type_union(else_type)

    @visitor.when(WhileLoopNode)
    def visit(self, node : WhileLoopNode, scope : Scope):
        self.visit(node.condition, scope.create_child())
        condition_type = node.condition.static_type

        # Chequeo que la condicion sea de tipo booleano
        if not condition_type.conforms_to(self.Bool_Type):
            self.errors.append(TypeError(node.condition.line, node.condition.column,
                     'Loop condition does not have type Bool'))

        # Chequeo consistencias en el cuerpo del while
        self.visit(node.body, scope.create_child())

        node.static_type = self.Object_Type

    @visitor.when(BlockNode)
    def visit(self, node : BlockNode, scope : Scope):

        # Chequeo consistencias en cada una de las instrucciones del cuerpo del bloque
        for expr in node.expressions:
            self.visit(expr, scope.create_child())

        node.static_type = node.expressions[-1].static_type

    @visitor.when(LetInNode)
    def visit(self, node : LetInNode, scope : Scope):
        for id, type, expr in node.let_body:

            if id.lex.lower() == 'self':
                self.errors.append(SemanticError(id.line, id.column,
                     '\'self\' cannot be bound in a \'let\' expression'))

            # Por cada una de las declaraciones del let
            try:
                type = self.Context.get_type(type.lex)
            except SemanticException as ex:
                # Chequeo que el tipo exista
                self.errors.append(TypeError(id.line, id.column, 
                     f'Class {type.lex} of let-bound identifier {id.lex} is undefined'))
                type = ErrorType()

            # Si es Self_Type tomo el tipo correspondiente
            type = self.Current_Type if isinstance(type, SelfType) else type

            child = scope.create_child()
            if expr:
                # Chequeo consistencias en la declaracion y la compatibilidad de tipos
                self.visit(expr, child)
                if not expr.static_type.conforms_to(type):
                    self.errors.append(TypeError(id.line, id.column,
                         f'Inferred type {expr.static_type.name} of initialization of '
                         f'{id.lex} does not conform to identifier\'s declared type {type.name}'))

            # Defino la variable
            scope.define_variable(id.lex, type, node.line, node.column)

        # Chequeo consistencias en el cuerpo del let in
        self.visit(node.in_body, scope.create_child())
        node.static_type = node.in_body.static_type

    @visitor.when(CaseOfNode)
    def visit(self, node : CaseOfNode, scope : Scope):
        # Chequeo consistencias en el case
        self.visit(node.expression, scope.create_child())

        branchs = []

        node.static_type = None
        for id, type, expr in node.branches:
            # Por cada instruccion en el cuerpo del case-of
            try:
                type = self.Context.get_type(type.lex)
            except SemanticException as ex:
                # Chequeo que el tipo exista
                self.errors.append(TypeError(type.line, type.column,
                    f'Class {type.lex} of case branch is undefined'))
                type = ErrorType()

            # Chequeo que no sea un tipo especial
            if isinstance(type, SelfType):
                self.errors.append(SemanticError(id.line, id.column,
                     f'SELF_TYPE cannot be used as a case branch'))

            child = scope.create_child()
            # Declaro la variable y chequeo consistencias en la expresion
            child.define_variable(id.lex, type, node.line, node.column)
            self.visit(expr, child)

            if type.name in branchs:
                self.errors.append(SemanticError(id.line, id.column,
                     f'Duplicate branch {type.name} in case statement'))
            branchs.append(type.name)

            node.static_type = node.static_type.type_union(expr.static_type) if node.static_type else expr.static_type


    @visitor.when(AssignNode)
    def visit(self, node : AssignNode, scope : Scope):
        # Chequeo consistencias en la expresion
        self.visit(node.expression, scope.create_child())
        expr_type = node.expression.static_type

        if node.id.lex.lower() == 'self':
            self.errors.append(SemanticError(node.line, node.column,
                     'Cannot assign to \'self\''))

        # Chequeo que la variable este declarada y que su tipo sea valido
        if scope.is_defined(node.id.lex):
            var_type = scope.find_variable(node.id.lex).type
            if isinstance(var_type, SelfType):
                var_type = self.Current_Type

            if not expr_type.conforms_to(var_type):
                self.errors.append(TypeError(node.expression.line, node.expression.column,
                     f'Inferred type {expr_type.name} of initialization of attribute {node.id.lex} '
                     f'does not conform to declared type {var_type.name}'))
        else:
            self.errors.append(NameError(node.line, node.column,
                 f'Undeclared identifier {node.id.lex}'))

        node.static_type = expr_type

    @visitor.when(NotNode)
    def visit(self, node : NotNode, scope : Scope):
        # Chequeo la consistencia de la expresion
        self.visit(node.expression, scope.create_child())

        # Chequeo que la expresion sea booleana
        if not node.expression.static_type.conforms_to(self.Bool_Type):
            self.errors.append(TypeError(node.expression.line, node.expression.column,
                 f'Argument of \'not\' has type {node.expression.static_type.name} instead of Bool'))

        node.static_type = self.Bool_Type

    @visitor.when(LessEqualNode)
    def visit(self, node : LessEqualNode, scope : Scope):
        # Chequeo la consistencia de ambos miembros
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())
        left_type = node.left.static_type
        right_type = node.right.static_type

        # Chequeo que ambos miembros posean tipo int
        if not left_type.conforms_to(self.Int_Type) or not right_type.conforms_to(self.Int_Type):
            self.errors.append(TypeError(node.line, node.column,
                 f'non-Int arguments: {left_type.name} <= {right_type.name}'))

        node.static_type = self.Bool_Type

    @visitor.when(LessNode)
    def visit(self, node: LessNode, scope: Scope):
        # Chequeo la consistencia de ambos miembros
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())
        left_type = node.left.static_type
        right_type = node.right.static_type

        # Chequeo que ambos miembros posean tipo int
        if not left_type.conforms_to(self.Int_Type) or not right_type.conforms_to(self.Int_Type):
            self.errors.append(TypeError(node.line, node.column,
                     f'non-Int arguments: {left_type.name} < {right_type.name}'))

        node.static_type = self.Bool_Type

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode, scope: Scope):
        # Chequeo la consistencia de ambos miembros
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())
        left_type = node.left.static_type
        right_type = node.right.static_type

        # Chequeo que ambos miembros posean tipos comparables
        if left_type.conforms_to(self.Int_Type) ^ right_type.conforms_to(self.Int_Type):
            self.errors.append(TypeError(node.line, node.column,
                 f'Illegal comparison with a basic type'))
        elif left_type.conforms_to(self.String_Type) ^ right_type.conforms_to(self.String_Type):
            self.errors.append(TypeError(node.line, node.column,
                 f'Illegal comparison with a basic type'))
        elif left_type.conforms_to(self.Bool_Type) ^ right_type.conforms_to(self.Bool_Type):
            self.errors.append(TypeError(node.line, node.column,
                 f'Illegal comparison with a basic type'))

        node.static_type = self.Bool_Type

    @visitor.when(ArithmeticNode)
    def visit(self, node : ArithmeticNode, scope : Scope):
        # Chequeo la consistencia de ambos miembros
        self.visit(node.left, scope.create_child())
        self.visit(node.right, scope.create_child())
        left_type = node.left.static_type
        right_type = node.right.static_type

        # Chequeo que ambos miembros posean tipo int
        if not left_type.conforms_to(self.Int_Type) or not right_type.conforms_to(self.Int_Type):
            self.errors.append(TypeError(node.line, node.column,
                 f'non-Int arguments: {left_type.name} and {right_type.name}'))

        node.static_type = self.Int_Type

    @visitor.when(IsVoidNode)
    def visit(self, node : IsVoidNode, scope : Scope):
        # Chequeo la consistencia de la expresion
        self.visit(node.expression, scope.create_child())
        node.static_type = self.Bool_Type

    @visitor.when(ComplementNode)
    def visit(self, node : ComplementNode, scope : Scope):
        # Chequeo la consistencia de la expresion
        self.visit(node.expression, scope.create_child())

        # Chequeo que la expresion sea de tipo booleana
        if not node.expression.static_type.conforms_to(self.Int_Type):
            self.errors.append(TypeError(node.expression.line, node.expression.column,
                 f'Argument of \'~\' has type {node.expression.static_type.name} instead of Int'))

        node.static_type = self.Int_Type

    @visitor.when(FunctionCallNode)
    def visit(self, node : FunctionCallNode, scope : Scope):
        # Chequeo la consistencia de la expresion a la cual se le pide la funcion
        self.visit(node.obj, scope.create_child())
        obj_type = node.obj.static_type

        try:
            if node.type:
                # Chequeo que el tipo exista
                try:
                    node_type = self.Context.get_type(node.type.lex)
                except SemanticException as ex:
                    self.errors.append(TypeError(node.line, node.column,
                         f'Class {node.type.lex} not defined'))
                    node_type = ErrorType()

                # Chequeo que el tipo no sea un tipo especial
                if isinstance(node_type, SelfType):
                    self.errors.append(TypeError(node.line, node.column,
                         'SELF_TYPE cannot be used in a dispatch'))

                # Chequeo que los tipos sean compatibles
                if not obj_type.conforms_to(node_type):
                    self.errors.append(TypeError(node.line, node.column,
                         f'Expression type {obj_type.name} does not conform '
                         f'to declared static dispatch type {node_type.name}'))

                obj_type = node_type


            obj_method = obj_type.get_method(node.id.lex)
            return_type = obj_type if isinstance(obj_method.return_type, SelfType) else obj_method.return_type

        except SemanticException as ex:
            self.errors.append(AttributeError(node.id.line, node.id.column,
                 f'Dispatch to undefined method {node.id.lex}'))
            return_type = ErrorType()
            obj_method = None

        # Chequeo consistencias en los argumentos con los que se llama al metodo
        for arg in node.args:
            self.visit(arg, scope.create_child())

        if obj_method and len(node.args) == len(obj_method.param_types):
            for arg, param_type, param_name in zip(node.args, obj_method.param_types, obj_method.param_names):
                if not arg.static_type.conforms_to(param_type):
                    # Chequeo compatibilidad de tipos entre los argumentos
                    self.errors.append(TypeError(arg.line, arg.column,
                        f'In call of method {obj_method.name}, type {arg.static_type.name} of '
                        f'parameter {param_name} does not conform to declared type {param_type.name}'))

        elif obj_method:
            # Chequeo que la cantidad de argumentos sea igual a las solicitadas por el metodo
            self.errors.append(SemanticError(node.id.line, node.id.column,
                      f'Method {obj_method.name} called with wrong number of arguments'))

        node.static_type = return_type


    @visitor.when(MemberCallNode)
    def visit(self, node : MemberCallNode, scope : Scope):
        # Chequeo que el metodo exista en el tipo actual
        try:
            obj_method = self.Current_Type.get_method(node.id.lex)
            return_type = self.Current_Type if isinstance(obj_method.return_type, SelfType) else obj_method.return_type
        except SemanticException as ex:
            self.errors.append(AttributeError(node.id.line, node.id.column,
                  f'Dispatch to undefined method {node.id.lex}'))
            obj_method = None
            return_type = ErrorType()

        # Chequeo la consistencia en los argumentos
        for arg in node.args:
            self.visit(arg, scope.create_child())

        if obj_method and len(node.args) == len(obj_method.param_types):
            # Chequeo la compatibiidad entre los tipos de los argumentos
            for arg, param_type, param_name in zip(node.args, obj_method.param_types, obj_method.param_names):
                if not arg.static_type.conforms_to(param_type):
                    self.errors.append(TypeError(arg.line, arg.column,
                         f'In call of method {obj_method.name}, type {arg.static_type.name} of '
                         f'parameter {param_name} does not conform to declared type {param_type.name}'))

        elif obj_method:
            # Chequeo que la cantidad de argumentos coincida con los que requiere el metodo
            self.errors.append(SemanticError(node.id.line, node.id.column,
                 f'Method {obj_method.name} called with wrong number of arguments'))

        node.static_type = return_type

    @visitor.when(NewNode)
    def visit(self, node : NewNode, scope : Scope):
        # Chequeo que el tipo exista
        try:
            type = self.Context.get_type(node.type.lex)
        except SemanticException as ex:
            self.errors.append(TypeError(node.type.line, node.type.column,
                f'\'new\' used with undeclared class {node.type.lex}'))
            type = ErrorType()

        node.static_type = type

    @visitor.when(IntegerNode)
    def visit(self, node : IntegerNode, scope : Scope):
        node.static_type = self.Int_Type

    @visitor.when(StringNode)
    def visit(self, node: StringNode, scope: Scope):
        node.static_type = self.String_Type

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode, scope: Scope):
        node.static_type = self.Bool_Type

    @visitor.when(IdNode)
    def visit(self, node: IntegerNode, scope: Scope):
        # Chequeo que la variable exista
        if scope.is_defined(node.token.lex):
            node.static_type = scope.find_variable(node.token.lex).type
        else:
            self.errors.append(NameError(node.line, node.column,
                 f'Undeclared identifier {node.token.lex}'))
            node.static_type = ErrorType()
