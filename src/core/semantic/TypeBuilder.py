from core.tools import visitor
from core.tools.Semantic import *
from core.parser.Parser import ProgramNode, ClassDeclarationNode, AttrDeclarationNode, FuncDeclarationNode
from core.tools.Errors import *

# Visitor encargado de contruir los tipos. Una vez que se conocen los nombres
# de los tipos que intervienen en el codigo COOL, este visitor les annade sus
# metodos y atributos, asi como el tipo padre.

class Type_Builder:
    def __init__(self, Context : Context):
        self.Context = Context
        self.Current_Type = None

        self.errors = []

        # Construye los tipos builtin
        self.Object_Type = self.Context.get_type('Object')

        self.IO_Type = self.Context.get_type('IO')
        self.IO_Type.set_parent(self.Object_Type)
        self.IO_Type.depth = 1

        self.Int_Type = self.Context.get_type('Int')
        self.Int_Type.set_parent(self.Object_Type)
        self.Int_Type.depth = 1
        self.Int_Type.sealed = True

        self.String_Type = self.Context.get_type('String')
        self.String_Type.set_parent(self.Object_Type)
        self.String_Type.depth = 1
        self.String_Type.sealed = True

        self.Bool_Type = self.Context.get_type('Bool')
        self.Bool_Type.set_parent(self.Object_Type)
        self.Bool_Type.depth = 1
        self.Bool_Type.sealed = True

        self.IO_Type.define_method('out_string', ['x'], [self.String_Type], SelfType(), 0, 0)
        self.IO_Type.define_method('out_int', ['x'], [self.Int_Type], SelfType(), 0, 0)
        self.IO_Type.define_method('in_int', [], [], self.Int_Type, 0, 0)
        self.IO_Type.define_method('in_string', [], [], self.String_Type, 0, 0)

        self.Object_Type.define_method('abort', [], [], self.Object_Type, 0, 0)
        self.Object_Type.define_method('type_name', [], [], self.String_Type, 0, 0)
        self.Object_Type.define_method('copy', [], [], SelfType(), 0, 0)

        self.String_Type.define_method('length', [], [], self.Int_Type, 0, 0)
        self.String_Type.define_method('concat', ['x'], [self.String_Type], self.String_Type, 0, 0)
        self.String_Type.define_method('substr', ['l', 'r'], [self.Int_Type, self.Int_Type], self.String_Type, 0, 0)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node : ProgramNode):
        for type in node.declarations:
            self.visit(type)

        try:
            self.Context.get_type('Main').get_method('main')
        except SemanticException:
            # Cada programa COOL debe tener una clase MAIN
            self.errors.append(SemanticError(0, 0,
                             f'Class Main and its method main must be defined'))

    @visitor.when(ClassDeclarationNode)
    def visit(self, node : ClassDeclarationNode):
        self.Current_Type = self.Context.get_type(node.id.lex)

        if node.parent:
            try:
                parent_type = self.Context.get_type(node.parent.lex)
            except SemanticException as ex:
                self.errors.append(TypeError(node.parent.line, node.parent.column,
                         f'Class {node.id} inherits from an undefined class {node.parent.lex}'))
                parent_type = self.Object_Type

            try:
                self.Current_Type.set_parent(parent_type)
            except SemanticException as ex:
                self.errors.append(SemanticError(node.parent.line, node.parent.column,
                     f'Class {node.id.lex} cannot inherit class {parent_type.name}'))

            parent = self.Current_Type.parent
            # Revisa que no haya herencia ciclica
            while parent:
                if parent == self.Current_Type:
                    self.errors.append(SemanticError(node.line, node.column,
                         f'Class {node.id.lex}, or an ancestor of {node.id.lex}, '
                         f'is involved in an inheritance cycle'))
                    self.Current_Type.parent = self.Object_Type
                    break
                parent = parent.parent

        else:
            self.Current_Type.set_parent(self.Object_Type)


        for feat in node.features:
            self.visit(feat)

    @visitor.when(AttrDeclarationNode)
    def visit(self, node : AttrDeclarationNode):
        try:
            attr_type = self.Context.get_type(node.type.lex)
        except SemanticException as ex:
            # Existio un error al tratar de obtener el tipo del atributo
            self.errors.append(TypeError(node.type.line, node.type.column, ex.text))
            attr_type = ErrorType()

        try:
            self.Current_Type.define_attribute(node.id.lex, attr_type, node.line, node.column)
        except SemanticException as ex:
            # Existio un error al tratar de definir el atributo
            self.errors.append(SemanticError(node.line, node.column, ex.text))

    @visitor.when(FuncDeclarationNode)
    def visit(self, node : FuncDeclarationNode):
        param_names, param_types = [], []

        for name, type in node.params:
            try:
                type = self.Context.get_type(type.lex)
            except SemanticException as ex:
                # Existio un error al tratar de obtener el tipo del parametro
                self.errors.append(TypeError(type.line, type.column,
                         f'Class {type.lex} of formal parameter {name.lex} is undefined'))
                type = ErrorType()
            else:
                if isinstance(type, SelfType):
                    self.errors.append(SemanticError(name.line, name.column,
                        f'\'self\' cannot be the name of a formal parameter'))
                    arg_type = ErrorType()

            if name.lex in param_names:
                self.errors.append(SemanticError(name.line, name.column,
                         f'Formal parameter {name.lex} is multiply defined'))

            param_names.append(name.lex)
            param_types.append(type)



        try:
            return_type = self.Context.get_type(node.type.lex)
        except SemanticException as ex:
            # Existio un error al tratar de obtener el tipo del parametro de retorno
            self.errors.append(TypeError(node.type.line, node.type.column,
                     f'Undefined return type {node.type.lex} in method {node.id.lex}'))
            return_type = ErrorType()

        if return_type is SelfType:
            return_type = self.Current_Type

        try:
            self.Current_Type.define_method(node.id.lex, param_names, param_types, return_type, node.line, node.column)
        except SemanticException as ex:
            # Existio un error al tratar de definir el metodo
            self.errors.append(SemanticError(node.line, node.column, ex.text))
