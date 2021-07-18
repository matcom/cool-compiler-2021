import cmp.visitor as visitor
from cool.ast.ast import *
from cool.semantic.type import Type,ErrorType,StringType,IntType,IOType,BoolType,ObjectType,SelfType,VoidType,AutoType
from cool.semantic.context import Context
from cool.semantic.atomic import ClassInstance
from cool.error.errors import *
import cool.visitors.utils as ut
from cool.semantic.operations import Operator

class ReconstructVisitor:
    def __init__(self, context, operator):
        self.context = context
        self.operator = operator
        self.tab = "    "
    
    def add_line(self, line, depth):
        return self.tab*depth + line + "\n"
    
    def preappend_depth_if_needed(self, text, depth):
        if text[-1] != "\n":
            return self.tab*depth + text + "\n"
        return text
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node, depth=0):
        program = ""
        for decl in node.declarations:
            program += self.visit(decl, depth)
            program += self.add_line("\n", depth)
        
        return program

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, depth=0):
        father = f" inherits {node.parent}" if node.parent != "Object" else ""
        class_decl = self.add_line(f"class {node.id}" + father, depth)
        class_decl += self.add_line("{", depth)
        for feature in node.features:
            class_decl += self.visit(feature, depth + 1)
        class_decl += self.add_line("}", depth)
        return class_decl
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, depth=0):
        attr_decl = f"{node.id}:{node.type.name}"
        if node.expr and node.expr.type.name != "Void" and node.expr.column != None:
            attr_decl += " <- "
            attr_decl += self.visit(node.expr, depth + 1)
        attr_decl += ";"
        return self.add_line(attr_decl, depth)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, depth=0):
        func_decl = f"{node.id}("
        func_decl += ", ".join([self.visit(x, depth + 1) for x in node.params])
        func_decl += f"): {node.type.name}"
        func_decl = self.add_line(func_decl, depth)
        func_decl += self.add_line("{", depth)
        func_decl += self.preappend_depth_if_needed(self.visit(node.body, depth+1), depth + 1)
        func_decl += self.add_line("};", depth)
        return func_decl
    
    @visitor.when(ParamNode)
    def visit(self, node, depth=0):
        return f"{node.id}:{node.type.name}"
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, depth=0):
        decl = self.add_line(f"{node.id}:{node.type.name} <- ", depth)
        decl += self.preappend_depth_if_needed(self.visit(node.expr, depth + 1), depth + 1)
        return decl
    
    @visitor.when(AssignNode)
    def visit(self, node, depth=0):
        assign = self.add_line(f"{node.id} <- ", depth)
        assign += self.preappend_depth_if_needed(self.visit(node.expr, depth + 1), depth + 1)
        return assign
    
    @visitor.when(CallNode)
    def visit(self, node, depth=0):
        obj = self.visit(node.obj, depth)
        obj = self.preappend_depth_if_needed(obj, depth)
        if node.at:
            obj += self.add_line(f"@{node.at.name}.{node.id}(", depth)  # remove the \n
        else:
            obj += self.add_line(f".{node.id}(", depth)  # remove the \n
        
        for arg in [self.visit(x, depth + 1) for x in node.args]:
            if arg[-1] == "\n":
                arg = arg[:len(arg)-1] + ",\n"
            else:
                arg = self.add_line(arg + ",", depth + 1)
            obj += arg 
        if node.args:
            obj = obj[:len(obj)-2] + "\n"
        obj += self.add_line(")", depth)
        return obj
    
    @visitor.when(BlockNode)
    def visit(self, node, depth=0):
        block = self.add_line("{", depth)
        
        for expr in node.expr_list:
            expr = self.visit(expr, depth + 1)
            if expr[-1] == "\n":
                expr = expr[:len(expr)-1] + ";\n"
            else:
                expr = self.add_line(expr + ";", depth + 1)
            block += expr
        
        block += self.add_line("}", depth)
        return block
    
    @visitor.when(ConditionalNode)
    def visit(self, node, depth=0):
        condition = self.add_line("if", depth)
        condition += self.preappend_depth_if_needed(self.visit(node.condition,depth + 1), depth + 1)
        condition += self.add_line("then", depth)
        condition += self.preappend_depth_if_needed(self.visit(node.then_expr, depth + 1), depth + 1)
        condition += self.add_line("else", depth)
        condition += self.preappend_depth_if_needed(self.visit(node.else_expr, depth + 1), depth + 1)
        condition += self.add_line("fi", depth)
        return condition
    
    @visitor.when(LetNode)
    def visit(self, node, depth=0):
        let = self.add_line("let", depth)
        for arg in [self.visit(arg, depth + 1) for arg in node.params]:
            if arg[-1] == "\n":
                arg = arg[:len(arg)-1] + ",\n"
            else:
                arg = self.preappend_depth_if_needed(arg + ",", depth + 1)
            let += arg 
        if node.params:
            let = let[:len(let)-2] + "\n"
        
        
        let += self.add_line("in", depth)
        expr = self.preappend_depth_if_needed(self.visit(node.expr, depth + 1), depth + 1)
        return let + expr
    
    @visitor.when(CaseNode)
    def visit(self, node, depth=0):
        case = self.add_line("case", depth)
        case += self.preappend_depth_if_needed(self.visit(node.expr, depth + 1), depth + 1)
        case += self.add_line("of", depth)
        for check in [self.visit(x, depth + 1) for x in node.params]:
            check = self.preappend_depth_if_needed(check, depth + 1)
            case += check
        case += self.add_line("esac", depth)
        return case
    
    @visitor.when(CheckNode)
    def visit(self, node, depth=0):
        check = self.add_line(f"{node.id}:{node.type.name} =>", depth)
        expr = self.visit(node.expr, depth + 1)
        expr = self.preappend_depth_if_needed(expr, depth + 1)
        check += expr[:len(expr)-1] + ";\n"
        return check
    
    @visitor.when(WhileNode)
    def visit(self, node, depth=0):
        code = self.add_line("while", depth)
        code += self.preappend_depth_if_needed(self.visit(node.condition, depth + 1), depth + 1)
        code += self.add_line("loop", depth)
        code += self.preappend_depth_if_needed(self.visit(node.expr, depth + 1), depth + 1)
        code += self.add_line("pool", depth)
        return code
        
    @visitor.when(UnaryNode)
    def visit(self, node, depth=0):
        operator = self.operator.get_operator(node) + " "
        operator += self.visit(node.member, depth + 1)
        return operator
    
    @visitor.when(BinaryNode)
    def visit(self, node, depth=0):
        operator = "("
        operator += self.visit(node.left, depth + 1)
        operator += " " + self.operator.get_operator(node) + " "
        operator += self.visit(node.right, depth + 1)
        operator += ")"
        return operator
    
    @visitor.when(VariableNode)
    def visit(self, node, depth=0):
        return node.lex
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, depth=0):
        return node.lex

    @visitor.when(BoolNode)
    def visit(self, node, depth=0):
        return node.lex

    @visitor.when(StringNode)
    def visit(self, node, depth=0):
        return node.lex
    
    @visitor.when(VoidNode)
    def visit(self, node, depth=0):
        return "void"
    
    @visitor.when(InstantiateNode)
    def visit(self, node, depth=0):
        return "new " + node.lex

class FormatVisitor(object):
    
    @visitor.on('node')
    def visit(self, node, tabs):
        pass
    
    def get_type_name(self, node):
        try:
            return node.type.name
        except AttributeError:
            return node.type
    
    @visitor.when(ProgramNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__ProgramNode [<class> ... <class>]'
        statements = '\n'.join(self.visit(child, tabs + 1) for child in node.declarations)
        return f'{ans}\n{statements}'
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node, tabs=0):
        parent = '' if node.parent is None else f": {node.parent}"
        ans = '\t' * tabs + f'\\__ClassDeclarationNode: class {node.id} {parent} {{ <feature> ... <feature> }}'
        features = '\n'.join(self.visit(child, tabs + 1) for child in node.features)
        return f'{ans}\n{features}'
    
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AttrDeclarationNode: {node.id} : {self.get_type_name(node)}'
        return f'{ans}'
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__VarDeclarationNode: let {node.id} : {self.get_type_name(node)} = <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(AssignNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__AssignNode: let {node.id} <- <expr>'
        expr = self.visit(node.expr, tabs + 1)
        return f'{ans}\n{expr}'
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node, tabs=0):
        params = ', '.join([self.visit(x) for x in node.params])
        ans = '\t' * tabs + f'\\__FuncDeclarationNode: {node.id}({params}) : {self.get_type_name(node)} {{ <expr> }};'
        body = self.visit(node.body, tabs + 1)
        return f'{ans}\n{body}'

    @visitor.when(BinaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__<expr> {node.__class__.__name__} <expr>'
        left = self.visit(node.left, tabs + 1)
        right = self.visit(node.right, tabs + 1)
        return f'{ans}\n{left}\n{right}'

    @visitor.when(UnaryNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f'\\__{node.__class__.__name__} <expr>'
        member = self.visit(node.member, tabs + 1)
        return f'{ans}\n{member}'

    @visitor.when(AtomicNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__{node.__class__.__name__}: {node.lex}'
    
    @visitor.when(BlockNode)
    def visit(self,node,tabs=0):
        ans = '\t' * tabs + f'\\__ BlockNode: {{ <expr_list> }}'
        expr_list = [ self.visit(x,tabs+1) for x in node.expr_list ]
        return ans + "\n" + '\n'.join(expr_list)
        
    @visitor.when(CallNode)
    def visit(self, node, tabs=0):
        obj = self.visit(node.obj, tabs + 1)
        ans = '\t' * tabs + f'\\__CallNode: <obj>.{node.id}(<expr>, ..., <expr>)'
        args = '\n'.join(self.visit(arg, tabs + 1) for arg in node.args)
        return f'{ans}\n{obj}\n{args}'
    
    @visitor.when(InstantiateNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f'\\__ InstantiateNode: new {node.lex}'
    
    @visitor.when(ParamNode)
    def visit(self, node, tabs=0):
        return '\t' * tabs + f"{node.id} : {self.get_type_name(node)}"
    
    @visitor.when(CaseNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f"\\__CaseNode: case <expr> of <check_list> esac"
        expr = self.visit(node.expr, tabs + 1)
        checks = "\n".join(self.visit(check, tabs + 1) for check in node.params)
        return f"{ans}\n{expr}\n{checks}"
    
    @visitor.when(CheckNode)
    def visit(self, node, tabs=0):
        ans = "\t" * tabs + f"\\__CheckNode: {node.id}:{self.get_type_name(node)} => <expr>"
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{expr}"
    
    @visitor.when(LetNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f"\\__LetNode: let <decl_list> in <expr>"
        decls = "\n".join(self.visit(decl, tabs + 1) for decl in node.params)
        expr = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{decls}\n{expr}"
    
    @visitor.when(ConditionalNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f"\\__ConditionalNode: if <expr> then <expr> else <expr> fi"
        cond = self.visit(node.condition, tabs + 1)
        then = self.visit(node.then_expr, tabs + 1)
        elsex = self.visit(node.else_expr, tabs + 1)
        return f"{ans}\n{cond}\n{then}\n{elsex}"
    
    @visitor.when(WhileNode)
    def visit(self, node, tabs=0):
        ans = '\t' * tabs + f"\\__WhileNode: while <expr> loop <expr> pool"
        cond = self.visit(node.condition, tabs + 1)
        body = self.visit(node.expr, tabs + 1)
        return f"{ans}\n{cond}\n{body}"
    
    
class TypeCollector(object):
    def __init__(self, errors=[], context=None):
        self.context = context
        self.errors = errors
    
    def add_semantic_error(self, error:SemanticError, row:int, column:int):
        error.set_position(row, column)
        self.errors.append(error)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        if not self.context:
            self.context = Context({
                'Object':ObjectType,
                'String':StringType,
                'Bool':BoolType,
                'Int':IntType,
                'IO':IOType,
                'Void':VoidType,
                'Error':ErrorType,
                })
        
        for class_decl in node.declarations:
            if class_decl.id in self.context.special_types:
                typex = self.context.get_type(class_decl.id)
                typex.class_node = class_decl
                self.add_semantic_error(SemanticError(REDEFINITION_BASIC_CLASS, class_decl.id), class_decl.row, class_decl.column)
            else:
                try:
                    typex = self.context.create_type(class_decl.id)
                    typex.class_node = class_decl
                except SemanticError as er:
                    self.add_semantic_error(er, class_decl.row, class_decl.column)
        
        for class_decl in node.declarations:
            if not class_decl.id in self.context.special_types:
                try:
                    curr_type = self.context.get_type(class_decl.id)
                except SemanticError as er:
                    self.add_semantic_error(er, class_decl.row, class_decl.column)
                if class_decl.parent:
                    try:
                        parent_type = self.context.get_type(class_decl.parent)
                    except SemanticError as er:
                        er = SemanticError(UNDEFINED_INHERITED_TYPE, class_decl.id, class_decl.parent)
                        self.add_semantic_error(er, class_decl.row, class_decl.column)
                    try:
                        if not curr_type.parent:
                            curr_type.set_parent(parent_type)
                    except SemanticError as er:
                        self.add_semantic_error(er, class_decl.row, class_decl.column)
        
        cycles = ut.any_cycles(ut.build_graph_dict(self.context.types))
        
        for type1,type2 in cycles:
            error = SemanticError(CIRCULAR_DEPENDENCY, type1.name)
            self.add_semantic_error(error, type1.class_node.row, type1.class_node.column)
            
class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    def add_semantic_error(self, error:SemanticError, row:int, column:int):
        error.set_position(row, column)
        self.errors.append(error)
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        for decl in node.declarations:
            self.visit(decl)
    
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        for child in node.features:
            self.visit(child)
            
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        if node.id == 'self':
            er = SemanticError(ATTRIBUTE_NAME_SELF)
            node.type = ErrorType()
            self.add_semantic_error(er, node.row, node.column)
            return
        try:
            node.type = self.context.get_type(node.type)
        except SemanticError as er:
            er = TypeCoolError(ATTRIBUTE_TYPE_UNDEFINED, node.type, node.id)
            node.type = ErrorType()
            self.add_semantic_error(er, node.row, node.column)
        try:
            attribute = self.current_type.define_attribute(node.id,node.type)
            attribute.node = node
        except SemanticError as er:
            self.add_semantic_error(er, node.row, node.column)
    
    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        for i,x in enumerate(node.params):
            if x.id == 'self':
                er = SemanticError(PARAM_NAME_SELF)
                self.add_semantic_error(er, x.row, x.column)
            try:
                x.type = self.context.get_type(x.type)
            except SemanticError as er:
                er = TypeCoolError(UNDEFINED_PARAM_TYPE, x.type, x.id)
                x.type = ErrorType()
                self.add_semantic_error(er, x.row, x.column)
            if x.id in [n.id for n in node.params[:i]]:
                er = SemanticError(METHOD_REPEATED_ARGS_NAME, x.id)
                self.add_semantic_error(er, x.row, x.column)
        try:
            node.type = self.context.get_type(node.type)
        except SemanticError as er:
            er = TypeCoolError(UNDEFINED_RETURN_TYPE, node.type, node.id)
            node.type = ErrorType()
            self.add_semantic_error(er, node.type_row, node.type_column)
        try:
            method = self.current_type.define_method(node.id,[x.id for x in node.params],[x.type for x in node.params],node.type)
            method.node = node
        except SemanticError as er:
            self.add_semantic_error(er, node.row, node.column)

class TypeChecker:
    """
    Checks if the operations between types are correct.
    Build the program scope.
    Nodes are tagged with their type.
    """
    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors
        self.operator = Operator(context,errors)

    def complete_initial_types(self):
        complete_types = ['Object','String','IO']
        for cmp_type in complete_types:
            self.context.get_type(cmp_type).complete()

    def add_semantic_error(self, error:SemanticError, row:int, column:int):
        error.set_position(row, column)
        self.errors.append(error)

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node, scope=None):
        scope = scope
        
        for declaration in node.declarations:
            self.visit(declaration, scope)
        
        if 'Main' in self.context.types:
            MainType = self.context.get_type('Main')
            try:
                main_method = MainType.get_method('main',0, only_local = True)
            except SemanticError as er:
                self.errors.append(SemanticError(NO_ENTRY_POINT))
        else:            
            self.errors.append(SemanticError(NO_MAIN_TYPE))
        
        self.complete_initial_types()
        
        return scope,self.operator

    @visitor.when(ClassDeclarationNode)
    def visit(self, node, scope):
        self.current_type = self.context.get_type(node.id)
        node.scope = scope.create_child(self.current_type)
        node.scope.define_variable('self',self.current_type)
        node.features.sort(key=lambda x: x.__class__.__name__) # Attributes first, Stable sort
        for feature in node.features:
            self.visit(feature,node.scope)
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node, scope):
        if not node.expr:
            if node.type.name != "AUTO_TYPE":
                node.expr = node.type.default
                node.expr.type = node.type # if type is void then is not assigned in the visit else the type is overridden
            else:
                return # No default expr can be assing at this moment
        self.visit(node.expr,scope)
        
        if not node.expr.type.conforms_to(node.type,self.current_type):
            self.add_semantic_error(TypeCoolError(ATTRIBUTE_INCOMPATIBLE_TYPES, node.id, node.type.name, node.expr.type.name),node.row,node.column)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node, scope):
        methods = []
        current_method = self.current_type.get_method(node.id,len(node.params))
        if self.current_type.parent:
            methods = self.current_type.parent.all_methods()
            methods = [x for x,typex in methods if x.name == node.id]
            methods = [x for x in methods if x != current_method]
        if methods:
            for method in methods:
                if len(method.param_names) == len(node.params):
                    for i,(x,y) in [(i,(x,y)) for i,(x,y) in enumerate(zip(method.param_types, current_method.param_types)) if x != y]:
                        err = SemanticError(METHOD_REDEFINED_WRONG_SIGNATURE_PARAM,method.name, y.name, x.name)
                        self.add_semantic_error(err, node.params[i].row, node.params[i].column)
                else:
                    err = SemanticError(METHOD_REDEFINED_WRONG_PARAM_AMOUNT, node.id)
                    self.add_semantic_error(err, node.row, node.column)
                if method.return_type != current_method.return_type:
                    err = SemanticError(METHOD_REDEFINED_WRONG_SIGNATURE_RETURN, method.name, current_method.return_type.name, method.return_type.name)
                    self.add_semantic_error(err, node.type_row, node.type_column)
                    
                        
        f_scope = scope.create_child()
        node.scope = f_scope
        
        for param in node.params:
            self.visit(param,f_scope)
        
        self.current_method = self.current_type.get_method(node.id,len(node.params))
        self.visit(node.body,f_scope)
        
        if not isinstance(node.type,VoidType) and not node.body.type.conforms_to(node.type,self.current_type):
            err = TypeCoolError(METHOD_INCOMPATIBLE_RETURN_TYPE, node.id, node.type.name, node.body.type.name)
            self.add_semantic_error(err, node.row, node.column)

    @visitor.when(ParamNode)
    def visit(self, node, scope):
        scope.define_variable(node.id,node.type)

    @visitor.when(VarDeclarationNode)
    def visit(self, node, scope, let_variable=False):
        if node.id == 'self':
            if let_variable:
                err = SemanticError(LET_BOUND_SELF)
            else:
                err = SemanticError(SELF_IS_READONLY)
            self.add_semantic_error(err, node.row, node.column)
        
        try:
            node.type = self.context.get_type(node.type)
        except SemanticError as er:
            if let_variable:
                er = TypeCoolError(LET_BOUND_TYPE_NOT_DEFINED, node.type, node.id)
            node.type = ErrorType()
            self.add_semantic_error(er, node.row, node.column)
        if not node.expr:
            if node.type.name != "AUTO_TYPE":
                node.expr = node.type.default
                node.expr.type = node.type # if type is void then is not assigned in the visit else the type is overridden
            else:
                if scope.is_local(node.id):
                    er = SemanticError(LOCAL_ALREADY_DEFINED, node.id, self.current_method.name)
                    self.add_semantic_error(er, node.row, node.column)
                else:
                    scope.define_variable(node.id,node.type)
                return # No default expr can be assing at this moment

        self.visit(node.expr,scope)
        
        if scope.is_local(node.id):
            er = SemanticError(LOCAL_ALREADY_DEFINED, node.id, self.current_method.name)
            self.add_semantic_error(er, node.row, node.column)
        else:
            scope.define_variable(node.id,node.type)
        
        if not node.expr.type.conforms_to(node.type,self.current_type):
            er = TypeCoolError(INCOMPATIBLE_TYPES, node.expr.type.name, node.id, node.type.name)
            self.add_semantic_error(er, node.row, node.column)
    
    @visitor.when(AssignNode)
    def visit(self, node, scope):
        if node.id == 'self':
            er = SemanticError(ASSIGN_SELF)
            self.add_semantic_error(er, node.row, node.column)

        self.visit(node.expr,scope)
        
        if not scope.is_defined(node.id):
            er = NameCoolError(VARIABLE_NOT_DEFINED, node.id)
            self.add_semantic_error(er, node.row, node.column)
        
        node.type = node.expr.type

        if not node.expr.type.conforms_to(node.type,self.current_type):
            er = TypeCoolError(INCOMPATIBLE_TYPES, node.expr.type.name, node.id, node.type.name)
            self.add_semantic_error(er, node.row, node.column)
     
    @visitor.when(CallNode)
    def visit(self, node, scope):
        # obj,id,args
        self.visit(node.obj,scope)
        for arg in node.args:
            self.visit(arg,scope)
            
        try:
            if node.at:
                node.at = self.context.get_type(node.at)
                if not node.obj.type.conforms_to(node.at,self.current_type):
                    er = TypeCoolError(STATIC_DISPATCH_INCOMPATIBLE_TYPES, node.obj.type.name, node.at.name)
                    self.add_semantic_error(er, node.row, node.column)
                dispatch_type = node.at
            else:
                dispatch_type = node.obj.type
            try:
                method = dispatch_type.get_method(node.id,len(node.args),self.current_type)
                not_conform = [(x,y.type,name) for x,y,name in zip(method.param_types,node.args,method.param_names) if not y.type.conforms_to(x,self.current_type)]
                for x,y,name in not_conform:
                    er = TypeCoolError(INCOMPATIBLE_PARAMS_TYPES, method.name, y.name, name, x.name)
                    self.add_semantic_error(er, node.row, node.column)
                node.type = method.return_type if method.return_type.name != "SELF_TYPE" else node.obj.type
            except SemanticError as er:
                if not any(meth for meth, typex in dispatch_type.all_methods() if meth.name == node.id):
                    raise AttributeCoolError(DISPATCH_UNDEFINED_METHOD, node.id)
                else:
                    raise SemanticError(DISPATCH_METHOD_WRONG_ARGS, node.id)

        except SemanticError as er:
            node.type = ErrorType()
            self.add_semantic_error(er, node.row, node.column)
    
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope):
        
        node.scope = scope.create_child()
        
        for expr in node.expr_list:
            self.visit(expr,node.scope)

        node.type = node.expr_list[-1].type 
    
    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope):
        self.visit(node.condition,scope)
        self.visit(node.then_expr,scope)
        self.visit(node.else_expr,scope)
        
        if node.condition.type != self.context.get_type('Bool') and not node.condition.type is ErrorType:
            er = TypeCoolError(NOT_BOOLEAN_CONDITION)
            self.add_semantic_error(er, node.row, node.column)
        try:
            node.type = node.get_return_type(self.current_type)
        except InferError as er:
            node.type = self.context.get_type("Error")
            self.add_semantic_error(er, node.row, node.column)
            
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope):
        let_scope = scope.create_child()
        curr_scope = let_scope
        for var_node in node.params:
            attr_scope = curr_scope.create_child()
            self.visit(var_node,attr_scope,True)
            curr_scope = attr_scope
        body_scope = curr_scope.create_child()
        self.visit(node.expr,body_scope)
        node.type = node.expr.type
    
    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope):
        node.type = self.context.get_type('Object')
        self.visit(node.condition,scope)
        if node.condition.type != self.context.get_type('Bool'):
            er = TypeCoolError(WHILE_NOT_BOOLEAN_CONDITION)
            self.add_semantic_error(er, node.row, node.column)
        self.visit(node.expr,scope)
    
    @visitor.when(CheckNode)
    def visit(self, node:CheckNode, scope):
        if node.id == 'self':
            er = SemanticError(SELF_IS_READONLY)
            self.add_semantic_error(er, node.row, node.column)
        
        try:
            node.type = self.context.get_type(node.type)
        except SemanticError:
            er = TypeCoolError(UNDEFINED_CLASS_CASE_BRANCH, node.type)
            self.add_semantic_error(er, node.row, node.column)
            node.type = ErrorType()

        node.scope = scope.create_child()
        node.scope.define_variable(node.id,node.type)
        
        self.visit(node.expr,node.scope)
        
        # if not node.expr.type.conforms_to(node.type,self.current_type):
        #     self.errors.append(INCOMPATIBLE_TYPES.format(node.expr.type.name,node.type.name) + f' Line:{node.row} Column:{node.column}')
    
    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope):
        self.visit(node.expr,scope)
        
        types = []
        param_types = []
        for i,param in enumerate(node.params):
            self.visit(param,scope)
            # if not (node.expr.type.conforms_to(param.type,self.current_type) or param.type.conforms_to(node.expr.type,self.current_type)):
            #     self.errors.append(f"Incompatible types {param.type.name} with {node.expr.type.name}" + f' Line:{node.row} Column:{node.column}')
            if any(x for x in param_types if x == param.type):
                er = SemanticError(CASE_TYPES_REPEATED, param.type.name)
                self.add_semantic_error(er, param.row, param.column)
            else:
                param_types.append(param.type)
            types.append((i,param.expr.type))
        
        static_type = types[0][1]
        for i,join in types[1:]:
            static_type = static_type.join(join,self.current_type)
        node.type = static_type
    
    @visitor.when(UnaryNode)
    def visit(self, node, scope):
        self.visit(node.member,scope)
        
        if not self.operator.operation_defined(node,node.member.type):
            node.type = ErrorType()
            node_operator = self.operator.get_operator(node)
            correct_types = self.operator.operations.get_valid_operators_of(node_operator)
            unary_correct_types = [x for x in correct_types if len(x) == 1]
            if len(unary_correct_types) == 0:
                correct_type_name = "No Type"
            else:
                correct_type_name = " or ".join([x[0].name for x in unary_correct_types])
                
            er = TypeCoolError(INVALID_UNARY_OPERATION, node_operator, node.member.type.name, correct_type_name)
            if not isinstance(node.member.type, ErrorType):
                self.add_semantic_error(er, node.row, node.column)
        else:
            node.type = self.operator.type_of_operation(node,node.member.type)
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        self.visit(node.left,scope)
        self.visit(node.right,scope)
        
        if not self.operator.operation_defined(node,node.left.type,node.right.type):
            node.type = ErrorType()
            operator = self.operator.get_operator(node)
            if operator == self.operator.get_operator(EqualNode(None, None)):
                er_message = INVALID_EQUAL_BASIC_TYPE_OPERATION
                er_args = ()
            else:
                er_message = INVALID_BINARY_OPERATION
                er_args = (operator, node.left.type.name,node.right.type.name)
            er = TypeCoolError(er_message, *er_args)
            self.add_semantic_error(er, node.row, node.column)
        else:
            node.type = self.operator.type_of_operation(node,node.left.type,node.right.type)
    
    @visitor.when(ConstantNumNode)
    def visit(self, node, scope):
        node.type = self.context.get_type("Int")

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.type = self.context.get_type("Bool")

    @visitor.when(StringNode)
    def visit(self, node:StringNode, scope):
        node.type = self.context.get_type("String")
        if len(node.lex) > 1024:
            er = LexerCoolError(STRING_TOO_LONG, len(node.lex))
            self.add_semantic_error(er, node.row, node.column)

    @visitor.when(VoidNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VariableNode)
    def visit(self, node, scope):
        if scope.is_defined(node.lex):
            var = scope.find_variable(node.lex)
            node.type = var.type
        else:
            node.type = ErrorType()
            er = NameCoolError(VARIABLE_NOT_DEFINED, node.lex)
            self.add_semantic_error(er, node.row, node.column)

    @visitor.when(InstantiateNode)
    def visit(self, node, scope):
        try:
            node.type = self.context.get_type(node.lex)
        except SemanticError as er:
            er = TypeCoolError(UNDEFINED_NEW_TYPE, node.lex)
            node.type = ErrorType()
            self.add_semantic_error(er, node.type_row, node.type_column)

class AutoResolver:

    def __init__(self, context:Context, errors=[]):
        self.context = context
        self.errors = errors

    def add_semantic_error(self, error:SemanticError, row:int, column:int):
        error.set_position(row, column)
        self.errors.append(error)

    def change_auto_to_concrete_type(self, node, node_type_name="type", less_concrete=False):
        typex = getattr(node, node_type_name)
        if typex.name == "AUTO_TYPE":
            try:
                if less_concrete:
                    setattr(node, node_type_name, typex.get_lower(self.current_type))
                else:
                    setattr(node, node_type_name, typex.get_higher(self.current_type))
            except InferError as er:
                self.add_semantic_error(er, node.row, node.column)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node):
        for declaration in node.declarations:
            self.visit(declaration)
        
    @visitor.when(ClassDeclarationNode)
    def visit(self, node):
        self.current_type = self.context.get_type(node.id)
        for feature in node.features:
            self.visit(feature)
        
    @visitor.when(AttrDeclarationNode)
    def visit(self, node):
        self.change_auto_to_concrete_type(node)
        if not node.expr:
            node.expr = node.type.default
            node.expr.type = node.type
        self.visit(node.expr)

    @visitor.when(FuncDeclarationNode)
    def visit(self, node):
        self.change_auto_to_concrete_type(node)
        for param in node.params:
            self.visit(param)
        
        self.visit(node.body)

    @visitor.when(ParamNode)
    def visit(self, node):
        self.change_auto_to_concrete_type(node, less_concrete=True)

    @visitor.when(VarDeclarationNode)
    def visit(self, node):
        self.change_auto_to_concrete_type(node)
        if not node.expr:
            node.expr = node.type.default
            node.expr.type = node.type
        self.visit(node.expr)
        
    @visitor.when(AssignNode)
    def visit(self, node):
        self.visit(node.expr)
     
    @visitor.when(CallNode)
    def visit(self, node):
        self.visit(node.obj)
        
        for arg in node.args:
            self.visit(arg)
            
        if node.at:
            pass
            
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode):
        for expr in node.expr_list:
            self.visit(expr)

    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode):
        self.visit(node.condition)
        self.visit(node.then_expr)
        self.visit(node.else_expr)
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode):
        for var_node in node.params:
            self.visit(var_node)
        self.visit(node.expr)
    
    @visitor.when(WhileNode)
    def visit(self, node:WhileNode):
        self.visit(node.condition)
        self.visit(node.expr)
    
    @visitor.when(CheckNode)
    def visit(self, node:CheckNode):
        self.visit(node.expr)
    
    @visitor.when(CaseNode)
    def visit(self, node:CaseNode):
        self.visit(node.expr)
        
        for i,param in enumerate(node.params):
            self.visit(param)
    
    @visitor.when(UnaryNode)
    def visit(self, node):
        self.visit(node.member)
        
    @visitor.when(BinaryNode)
    def visit(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
    @visitor.when(ConstantNumNode)
    def visit(self, node):
        pass

    @visitor.when(BoolNode)
    def visit(self, node):
        pass

    @visitor.when(StringNode)
    def visit(self, node:StringNode):
        pass

    @visitor.when(VoidNode)
    def visit(self, node):
        pass

    @visitor.when(VariableNode)
    def visit(self, node):
        pass

    @visitor.when(InstantiateNode)
    def visit(self, node):
        pass


class RunVisitor:
    
    def __init__(self, context:Context, scope, operator, errors=[]):
        self.context = context
        self.scope = scope
        self.errors = errors
        self.operator = operator
    
    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node:ProgramNode, scope=None):
        for decl in node.declarations:
            if decl.id == 'Main':
                for method in [x.node for x,y in self.context.get_type('Main').all_methods()]:
                    if method.id == 'main':
                        main_type = self.context.get_type(decl.id)
                        main_instance = ClassInstance(main_type,self.context,self.operator,self.errors)
                        # method_scope = method.scope.copy()
                        # method_scope.set_variable_value('self',main_instance)
                        # method_scope.set_parent(main_instance.scope)
                        try:
                            value = self.visit(method.body,main_instance.scope)
                        except RunError as err:
                            self.errors.append(err)
                            return None
                        return value
    
    @visitor.when(VarDeclarationNode)
    def visit(self, node:VarDeclarationNode, scope):
        current_value = self.visit(node.expr,scope)
        scope.define_variable(node.id,node.type)
        scope.set_variable_value(node.id,current_value)
        return current_value
        
    @visitor.when(AssignNode)
    def visit(self, node:AssignNode, scope):
        value = self.visit(node.expr,scope)
        scope.set_variable_value(node.id,value)
        return value
    
    @visitor.when(CallNode)
    def visit(self, node:CallNode, scope):
        value = self.visit(node.obj,scope)
        if value.type.name == "Void":
            raise RunError(DISPATCH_VOID + f" Line:{node.row} Column:{node.column}")
        args = [self.visit(x,scope) for x in node.args]
        if node.at:
            method = node.at.get_method(node.id,len(node.args))
        else:
            method = value.type.get_method(node.id,len(node.args))
        func_scope = method.node.scope.copy()
        func_scope.set_parent(value.scope)
        for arg,name in zip(args,method.param_names):
            func_scope.set_variable_value(name,arg)
        # func_scope.set_variable_value('self',value)
        value = self.visit(method.node.body,func_scope)
        return value
    
    @visitor.when(SpecialNode)
    def visit(self, node:SpecialNode, scope):
        try:
            return node.func(scope,self.context,self.operator,self.errors)
        except RunError as cexc:
            raise RunError(cexc.text + f" Line:{node.row} Column:{node.column}")
    
    @visitor.when(BlockNode)
    def visit(self, node:BlockNode, scope):
        body_scope = scope.create_child()
        values = [self.visit(x,body_scope) for x in node.expr_list]
        return values[-1]
    
    @visitor.when(ConditionalNode)
    def visit(self, node:ConditionalNode, scope):
        condition = self.visit(node.condition,scope)
        if condition.value is True:
            return self.visit(node.then_expr,scope)
        if condition.value is False:
            return self.visit(node.else_expr,scope)
        raise RunError(NO_BOOL_CONDITION + f" Line:{node.row} Column:{node.column}") # This connot happend BUT you never know
    
    @visitor.when(LetNode)
    def visit(self, node:LetNode, scope):
        let_scope = scope.create_child()
        for var_decl in node.params:
            value = self.visit(var_decl.expr,let_scope)
            if not let_scope.is_local(var_decl.id):
                let_scope.define_variable(var_decl.id,var_decl.type)
            let_scope.set_variable_value(var_decl.id,value)
        value = self.visit(node.expr,let_scope)
        return value

    @visitor.when(WhileNode)
    def visit(self, node:WhileNode, scope):
        while self.visit(node.condition,scope).value == True:
            self.visit(node.expr,scope)
        typex =  self.context.get_type('Void')
        return ClassInstance(typex,self.context,self.operator,self.errors,value=None)
    
    @visitor.when(CheckNode)
    def visit(self, node:CheckNode, scope,**kwargs):
        node_scope = scope.create_child()
        value = kwargs['value']
        node_scope.define_variable(node.id,value.type)
        node_scope.set_variable_value(node.id,value)
        return self.visit(node.expr,node_scope)
    
    @visitor.when(CaseNode)
    def visit(self, node:CaseNode, scope):
        value = self.visit(node.expr,scope)
        
        if value.type.name == "Void":
            raise RunError(VOID_TYPE_CONFORMS + f" Line: {node.row} Column: {node.column}")
            
        try:
            greaters = (x for x in [(i,x.type) for i,x in enumerate(node.params)] if value.type.conforms_to(x[1],value.type))
            least_pos,least = next(greaters)
            for i,other in greaters:
                least_pos,least = (least_pos,least) if least.conforms_to(other,least) else (i,other)
        except StopIteration:
            raise RunError(CASE_NO_BRANCH_SELECTED.format(value.type.name) + f" Line: {node.row} Column: {node.column}")
        
        return self.visit(node.params[least_pos],scope,value=value)
        
    @visitor.when(UnaryNode)
    def visit(self, node, scope):
        operator = self.operator.get_operator(node)
        value = None
        member_value = self.visit(node.member,scope)
        try:
            value = self.operator.operate(operator,member_value)
        except RunError as err:
            raise RunError(err.text + f' Line:{node.row} Column:{node.column}')
        return value
    
    @visitor.when(BinaryNode)
    def visit(self, node, scope):
        operator = self.operator.get_operator(node)
        value = None
        left_value = self.visit(node.left,scope)
        right_value = self.visit(node.right,scope)
        try:
            value = self.operator.operate(operator,left_value,right_value)
        except RunError as err:
            raise RunError(err.text + f' Line:{node.row} Column:{node.column}')
        return value
    
    @visitor.when(ConstantNumNode)
    def visit(self, node:ConstantNumNode, scope):
        typex = self.context.get_type('Int')
        return ClassInstance(typex,self.context,self.operator,self.errors,value=int(node.lex))
    
    @visitor.when(BoolNode)
    def visit(self, node, scope):
        typex = self.context.get_type("Bool")
        if node.lex[0]=='t': # true
            return ClassInstance(typex,self.context,self.operator,self.errors,value=True)
        return ClassInstance(typex,self.context,self.operator,self.errors,value=False)
            
    @visitor.when(StringNode)
    def visit(self, node, scope):
        typex = self.context.get_type('String')
        string_without_delimitators = node.lex[1:len(node.lex)-1]
        return ClassInstance(typex,self.context,self.operator,self.errors,value=string_without_delimitators)

    @visitor.when(VoidNode)
    def visit(self, node, scope):
        typex =  self.context.get_type('Void')
        return ClassInstance(typex,self.context,self.operator,self.errors,value=None)

    @visitor.when(VariableNode)
    def visit(self, node:VariableNode, scope):
        try:
            value = scope.get_variable_value(node.lex)
        except TypeError as exc: # Variable not assign yet searching in Attr
            try:
                attr = [x.type for x in scope.locals if x.name == 'self'][0].get_attribute(node.lex)
                value = self.visit(attr.node.expr, scope)
            except SemanticError as er: # Attr not found
                er.set_position(node.row, node.column)
                self.errors.append(er)
        return value
    
    @visitor.when(InstantiateNode)
    def visit(self, node:InstantiateNode, scope):
        typex = self.context.get_type(node.lex,scope.find_variable('self').type)
        return ClassInstance(typex,self.context,self.operator,self.errors)
    