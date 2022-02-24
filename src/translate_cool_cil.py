import utils.visitor as visitor
import ast_cool_hierarchy as ast_cool
import ast_cil_hierarchy as ast_cil
from utils.semantic import Context, Type


FUNCTION_NAME = 'f_%s_%s'
LOCAL_NAME = 'local_%s_%s'


class TranslateCool2Cil:
    def __init__(self, cool_tree, context):
        self.context: Context = context
        self.cil_program = ast_cil.Program()
        self.current_function: ast_cil.Function = None
        self.current_class: ast_cool.ClassDeclarationNode = None

    def create_cil_type(self, type_name):
        _type = ast_cil.Type(type_name)
        self.cil_program.type_section.append(_type)
        return _type

    def create_cil_function(self, func_name):
        function = ast_cil.Function(func_name)
        self.cil_program.code_section.append(function)
        return function

    @staticmethod
    def create_local(function: ast_cil.Function):
        local = LOCAL_NAME % (function.fun_name, len(function.local_vars))
        function.local_vars.append(local)
        return local

    @visitor.on('cool_node')
    def visit(self, cool_node):
        pass

    @visitor.when(ast_cool.ProgramNode)
    def visit(self, cool_node: ast_cool.ProgramNode):
        # Create Function to start program
        start_function = self.create_cil_function(FUNCTION_NAME % ('start', ''))
        local1 = self.create_local(start_function)
        local2 = self.create_local(start_function)
        start_function.instructions.extend([
            ast_cil.Call(local1, FUNCTION_NAME % ('Main', '_init_')),
            ast_cil.Arg(local1),
            ast_cil.Call(local2, FUNCTION_NAME % ('Main', 'main')),
            ast_cil.Return(0)])

        # Visit all classes
        for declaration in cool_node.declarations:
            self.visit(declaration)

    @visitor.when(ast_cool.ClassDeclarationNode)
    def visit(self, cool_node: ast_cool.ClassDeclarationNode):
        cil_type = self.create_cil_type(cool_node.id)

        # Create Type Section
        class_type: Type = self.context.get_type(cool_node.id)
        while class_type is not None:
            attr_names = []
            for attr in class_type.attributes:
                attr_names.append(attr.name)
            func_names = []
            for func in class_type.methods:
                func_names.append(FUNCTION_NAME % (class_type.name, func.name))
            cil_type.attributes = attr_names + cil_type.attributes
            cil_type.methods = func_names + cil_type.methods
            class_type = class_type.parent

        # Create Init Function
        init_funct = self.create_cil_function(FUNCTION_NAME % (cool_node.id, '_init_'))
        self.current_function = init_funct
        self_instance = self.create_local(init_funct)
        init_funct.instructions.append(
            ast_cil.Allocate(self_instance, cool_node.id))
        index = 0
        for attribute in [f for f in cool_node.features if isinstance(f, ast_cool.AttrDeclarationNode)]:
            attribute_instance = self.visit(attribute)
            init_funct.instructions.append(
                ast_cil.SetAttr(attribute_instance, self_instance, index))
            index += 1
        init_funct.instructions.append(
            ast_cil.Return(self_instance))
        self.current_function = None

        # Create rest of Functions
        for method in [f for f in cool_node.features if isinstance(f, ast_cool.FuncDeclarationNode)]:
            self.visit(method)

    @visitor.when(ast_cool.AttrDeclarationNode)
    def visit(self, cool_node: ast_cool.AttrDeclarationNode):
        if cool_node.val is None:
            if cool_node.type == 'Int':
                local1 = self.create_local(self.current_function)
                self.current_function.instructions.extend([
                    ast_cil.Assign(local1, 0)
                ])
            # TODO add rest of default values
        else:
            return self.visit(cool_node.val)

    @visitor.when(ast_cool.FuncDeclarationNode)
    def visit(self, cool_node: ast_cool.FuncDeclarationNode):
        function = self.create_cil_function(FUNCTION_NAME % (self.current_class.id, cool_node.id))
        function.params.append('self')
        for param in cool_node.params:
            function.params.append(param)

        result = self.visit(cool_node.body)

        function.instructions.append(
            ast_cil.Return(result))
