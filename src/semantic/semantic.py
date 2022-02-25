import semantic.types as CT
from parser.ast import *
from semantic.types import append_error_semantic

def semantic_check(node):
    if type(node) is ProgramNode:
        program_visitor(node)

def class_visitor(_class: ClassDeclarationNode, index: CT.Tipos, scope: dict):
    
    index = CT.TypesByName[_class.type]
    scope = scope.copy()
    scope['self'] = index
    for feature in _class.feature_nodes:
        if type(feature) is AttrDeclarationNode:
            attr_declaration_visitor(feature, index, scope)
        if type(feature) is FuncDeclarationNode:
            func_declaration_visitor(feature, index, scope)

def program_visitor(program: ProgramNode):
 
    # Check type declaration (check duplicated types...) Check jerarquia de tipos
    if not (CT.check_type(program) and CT.check_jerarquia(program)):
        return

    # Check class Main
    try:
        CT.TypesByName['Main']
    except KeyError:
        append_error_semantic(0, 0, f'Main class undeclared')
        return

    # Check all methos and attributes for all declared types, and add them to respective type
    list_type_result = [CT.ObjectType, CT.IntType, CT.StringType, CT.BoolType, CT.IOType]

    classes = program.classes.copy()

    while len(classes) != 0:
        c: ClassDeclarationNode = classes.pop()
        if c.parent_type is not None:
            padre = CT.TypesByName[c.parent_type]

            if padre not in list_type_result:
                classes = [c] + classes
                continue

        classT = CT.TypesByName[c.type]
        for f in c.feature_nodes:
            if type(f) is FuncDeclarationNode:
                arg_type = [param[1] for param in f.params]
                result, msg = classT.add_method(
                    f.id, arg_type, f.return_type)

                if not result:
                    append_error_semantic(f.lineno, f.colno, msg)
            elif type(f) is AttrDeclarationNode:
                result, msg = classT.add_attr(f.id, f.type, f.expr)
                if not result:
                    append_error_semantic(f.lineno, f.colno, msg)
        list_type_result.append(classT)
        
    # Check recursive each delared class
    for c in program.classes:
        class_visitor(c, None, {})

def def_attribute_visitor(def_attr: AttrDeclarationNode, index: CT.Tipos, scope: dict):
    # Check if TYPE exists
    id = CT.get_type(def_attr.type)
    if id is None:
        append_error_semantic(def_attr.lineno, def_attr.colno, f'TypeError: Class {def_attr.type} of let-bound identifier {def_attr.id} is undefined')
    # Check if EXPR is not None
    if def_attr.expr:
        # Check EXPR
        express = expression_visitor(
            def_attr.expr, index, scope)
        # Check type(EXPR) <= TYPE
        if not CT.check_herencia(express, id) and id is not None and express is not None:
            append_error_semantic(def_attr.lineno, def_attr.colno, f'TypeError: Inferred type {express} of initialization of {def_attr.id} does not conform to identifier\'s declared type {id}.')
    # Type of the attribute is TYPE
    return id

def attr_declaration_visitor(attr: AttrDeclarationNode, index: CT.Tipos, scope: dict):
    if attr.id == 'self':
        append_error_semantic(attr.lineno, attr.colno,f'SemanticError: \'self\' cannot be the name of an attribute.')
    if attr.expr:
        # Check EXPR
        express = expression_visitor(attr.expr, index, scope)
        attr_type = CT.get_type(attr.type)
        # type(EXPR) <= TYPE
        if attr_type is not None and not CT.check_herencia(express, attr_type):
            append_error_semantic(attr.lineno, attr.expr.colno, f'TypeError: Inferred type {express} of initialization of attribute d does not conform to declared type {attr_type}.')
        else:
            return attr_type

def expression_visitor(expression, index: CT.Tipos, scope: dict) -> CT.Tipos:
    try:
        return __visitors__[type(expression)](expression, index, scope)
    except KeyError:
        print(f'Not visitor for {expression}')


def func_declaration_visitor(function: FuncDeclarationNode, index: CT.Tipos, scope: dict):
    scope = scope.copy()
    # Add PARAMS to scope. Type of PARAMS already check in program_visitor(4)
    arg_names = set()
    for arg in function.params:
        if arg[0] == 'self':
            append_error_semantic(function.lineno, function.colno,
                               f'SemanticError: \'self\' cannot be the name of a formal parameter.')
        if arg[0] in arg_names:
            append_error_semantic(
                function.lineno, function.colno, f'SemanticError: Formal parameter {arg[0]} is multiply defined.')
            return
        arg_names.add(arg[0])
        scope[arg[0]] = CT.get_type(arg[1])
    # Check EXPR
    bloque = expression_visitor(
        function.expressions, index, scope)
    resultados = CT.get_type(function.return_type)
    # Update RETURN_TYPE with current class type if that is SELFTYPE
    if resultados == CT.SelfType:
        resultados = index
    # Check type(EXPR) <= RETURN_TYPE
    if CT.check_herencia(bloque, resultados):
        return resultados
    elif bloque is not None:
        append_error_semantic(function.lineno, function.colno,
                           f'TypeError: Inferred return type {bloque} of method {function.id} does not conform to declared return type {resultados}.')

def func_call_visitor(func_call: FuncCallNode, index: CT.Tipos, scope: dict):
    args_types = []    
    msg = None
    func_call.self_type = index
    method = None
    # Compute args type, not check yet, because check need wait to find the specific function
    for arg in func_call.args:
        arg_type = expression_visitor(arg, index, scope)
        args_types.append(arg_type)
    # EXPR is not None (cases 1 and 2)
    if func_call.object:
        # Check type(EXPR)
        object_type = expression_visitor(func_call.object, index, scope)
        if object_type is None:
            return None
        # TYPE is not None
        if func_call.type:
            # Check TYPE
            specific_type = CT.get_type(func_call.type)
            if specific_type is None:
                append_error_semantic(func_call.lineno, func_call.colno, f'unknown type \'{func_call.type}\'')
            # Check type(EXPR) <= TYPE
            elif CT.check_herencia(object_type, specific_type):
                method, _, msg = specific_type.metodos_no_heredados(func_call.id, args_types)
                # If returned type of the funtion is SELFTYPE then returned type is TYPE
                if method is not None and method.returnedType == CT.SelfType:
                    method.returnedType = specific_type
            else:
                append_error_semantic(func_call.lineno, func_call.colno, f'TypeError: Expression type {object_type} does not conform to declared static dispatch type {specific_type}.')
                return None
        else:
            method, _, msg = object_type.get_method(func_call.id, args_types)
            if method is not None and method.returnedType == CT.SelfType:
                method.returnedType = object_type
    # If EXPR is None
    else:
        method, _, msg = index.get_method(func_call.id, args_types)
    if method is None and msg is not None:
        append_error_semantic(func_call.lineno, func_call.colno, msg)
    # If returned type of the function is SELFTYPE then returned type is current class type
    elif method.returnedType == CT.SelfType:
        func_call.returned_type = index
    else:
        # Type of function call is the returned type of function
        func_call.returned_type = method.returnedType
    return func_call.returned_type

def assignment_visitor(assign: AssignNode, index: CT.Tipos, scope: dict):
    if assign.id == 'self':
        append_error_semantic(assign.lineno, assign.colno,
                           f'SemanticError: Cannot assign to \'self\'.')
    # Check type(ID)
    try:
        # First find in scope
        id = scope[assign.id]
    except KeyError:
        # Second find in current class attributes
        attr, _ = CT.get_attribute(index, assign.id)
        if attr is None:
            append_error_semantic(assign.id.lineno, assign.id.colno,
                               f'NameError: Undeclared identifier {assign.id}.')
            id = None
        else:
            id = attr.attrType
    # Check EXPR
    express = expression_visitor(assign.expr, index, scope)
    # Check type(EXPR) <= type(ID)
    if not CT.check_herencia(express, id) and id is not None and express is not None:
        append_error_semantic(assign.expr.lineno, assign.expr.colno,
                           f'TypeError: Inferred type {express} of initialization of {assign.id} does not conform to identifier\'s declared type {id}.')
    # Type of assigment is type(EXPR)
    assign.returned_type = express
    return express

def block_expr_visitor(block: BlockNode, index: CT.Tipos, scope: dict):
    final_type = None
    # Check each epression in EXPR_LIST
    for expr in block.expressions:
        final_type = expression_visitor(expr, index, scope)
    # Type of block is type of the last expression in EXPR_LIST
    block.returned_type = final_type
    return final_type

def int_visitor(expr: IntNode, index, scope):
    # Type os int is Int 
    expr.returned_type = CT.IntType
    return CT.IntType


def bool_visitor(expr: BoolNode, index, scope):
    # Type of bool is Bool 
    expr.returned_type = CT.BoolType
    return CT.BoolType


def string_visitor(expr: StringNode, index, scope):
    # Type of string is String :)  
    expr.returned_type = CT.StringType
    return CT.StringType

def if_visitor(if_struct: IfNode, index: CT.Tipos, scope: dict):
    # Check IF_EXPR. type(IF_EXPR) must be a Bool
    expression = expression_visitor(if_struct.if_expr, index, scope)
    if expression != CT.BoolType and expression is not None:
        append_error_semantic(if_struct.if_expr.lineno, if_struct.if_expr.colno,f'TypeError: Predicate of \'if\' does not have type {CT.BoolType}.')
    # Check THEN_EXPR
    then_type = expression_visitor(if_struct.then_expr, index, scope)
    # Check ELSE_EXPR
    else_type = expression_visitor(if_struct.else_expr, index, scope)
    # Type of \"if\" stament is the pronounced join of THEN_EXPR and ELSE_EXPR
    if_struct.returned_type = CT.join_set(then_type, else_type)
    return if_struct.returned_type

def let_visitor(let: LetNode, index: CT.Tipos, scope: dict):
    scope = scope.copy()
    # Check all attributes in LET_ATTRS
    for attribute in let.let_attrs:
        if attribute.id == 'self':
            append_error_semantic(
                attribute.lineno, attribute.colno, f'SemanticError: \'self\' cannot be bound in a \'let\' expression.')
        attribute_type = expression_visitor(
            attribute, index, scope)
        if attribute_type is None:
            return None
        scope[attribute.id] = attribute_type
    # Check EXPR and Type of let is type(EXPR)
    let.returned_type = expression_visitor(let.expr, index, scope)
    return let.returned_type

def loop_expr_visitor(loop: WhileNode, index: CT.Tipos, scope: dict):
    # Check CONDITION_EXPR. type(CONDITION_EXPR) must be a Bool
    expression = expression_visitor(loop.cond, index, scope)
    if expression != CT.BoolType and expression is not None:
        append_error_semantic(loop.cond.lineno, loop.cond.colno,f'TypeError: Loop condition does not have type {CT.BoolType}.')
    # Check EXPR
    expression_visitor(loop.body, index, scope)
    # Type of loop is Oject
    loop.returned_type = CT.ObjectType
    return CT.ObjectType

def case_expr_visitor(case: CaseNode, index: CT.Tipos, scope: dict):
    branch_types = set()
    # Check EXPR
    expression_visitor(case.expr, index, scope)
    # Check first branch
    branch_0 = case.case_list[0]
    branch_types.add(branch_0.type)
    # Check TYPE_1
    branch_0_type = CT.get_type(branch_0.type)
    temp = scope.copy()
    if branch_0_type is None:
        append_error_semantic(branch_0.lineno, branch_0.colno, f'TypeError: Class {branch_0.type} of case branch is undefined.')
    else:
        # Update local  with ID_1
        temp[branch_0.id] = branch_0_type
    # Check EXPR_1 and set current type as type(EXPR_1)
    current_type = expression_visitor(branch_0.expr, index, temp)

    # Check rest of branches (k=2,...,n)
    for branch in case.case_list[1:]:
        if branch.type in branch_types:
            append_error_semantic(branch.lineno, branch.colno,f'SemanticError: Duplicate branch {branch.type} in case statement.')
        temp = scope.copy()
        # Check TYPE_k
        branch_type = CT.get_type(branch.type)
        if branch_type is None:
            append_error_semantic(branch.lineno, branch.colno,f'TypeError: Class {branch.type} of case branch is undefined.')
        # Update local  with ID_k
        temp[branch.id] = branch_type
        # Check EXPR_k and set current type as pronounced join of current type and  type(EXPR_k)
        current_type = CT.join_set(current_type, expression_visitor(branch.expr, index, temp))
    # Type of case is the pronounced join of all branch expressions types, then is the current type at final of step 3)
    case.returned_type = current_type
    return case.returned_type

def logic_negation_visitor(negation: NotNode, index: CT.Tipos, scope: dict):
    # Check EXPR
    value = expression_visitor(negation.val, index, scope)
    # Check type(EXPR) must be Bool
    if value != CT.BoolType and value is not None:
        append_error_semantic(negation.lineno, negation.colno, f'TypeError: Argument of \'not\' has type {CT.IntType} instead of {value}.')
    # Type of the logic negation is Bool
    negation.returned_type=CT.BoolType
    return CT.BoolType

def negation_visitor(negation: IntCompNode, index: CT.Tipos, scope: dict):
    # Check EXPR
    value = expression_visitor(negation.val, index, scope)
    # Check type(EXPR) must be Int
    if value != CT.IntType and value is not None:
        append_error_semantic(negation.lineno, negation.colno,f'TypeError: Argument of \'~\' has type {value} instead of {CT.IntType}.')
    # Type of the binary negation (~) is Int
    negation.returned_type=CT.BoolType
    return CT.IntType

def arithmetic_operator_visitor(operator: BinaryNode, index: CT.Tipos, scope: dict):
    # Check LEXPR, must be Int
    left = expression_visitor(operator.lvalue, index, scope)
    if left != CT.IntType and left is not None:
        append_error_semantic(operator.lineno, operator.colno,f'TypeError: non-Int arguments: {left} + {CT.IntType}')
    # Check REXPR, must be a Int
    right = expression_visitor(operator.rvalue, index, scope)
    if right != CT.IntType and right is not None:
        append_error_semantic(operator.lineno, operator.colno,f'TypeError: non-Int arguments: {CT.IntType} + {right}')
    # Type of the arithmetic operator (binary) is Int
    operator.returned_type = CT.IntType
    return CT.IntType

def var_visitor(var: VarNode, index: CT.Tipos, scope: dict):
    # Check if ID is in local 
    if var.id in scope.keys():
        var.returned_type = scope[var.id]
    else:
        # Check if ID is an class attribute
        attribute, _ = CT.get_attribute(index, var.id)
        if attribute is not None:
            var.returned_type = attribute.attrType
        else:
            append_error_semantic(var.lineno, var.colno,f'NameError: Undeclared identifier {var.id}.')
    # Type of var is the already funded type
    return var.returned_type

def comparison_visitor(cmp: BinaryNode, index: CT.Tipos, scope: dict):
    # Check LEXPR, must be Int
    left = expression_visitor(cmp.lvalue, index, scope)
    if left != CT.IntType and left is not None:
        append_error_semantic(cmp.lvalue.lineno, cmp.lvalue.colno,f'TypeError: non-{CT.IntType} arguments: {left} < {CT.IntType}')
    # Check REXPR, must be Int
    right = expression_visitor(cmp.rvalue, index, scope)
    if right != CT.IntType and right is not None:
        append_error_semantic(cmp.rvalue.lineno, cmp.rvalue.colno,f'TypeError: non-{CT.IntType} arguments: {CT.IntType} < {right}')
    # Type of the comparison is Bool
    cmp.returned_type = CT.BoolType
    return CT.BoolType

def new_expr_visitor(new: NewNode, index: CT.Tipos, scope: dict):
    # Check TYPE exists
    tipo = CT.get_type(new.type)
    if not tipo:
        append_error_semantic(new.lineno, new.colno, f'TypeError:  \'new\' used with undefined class {new.type}.')
    # Is TYPE is SELFTYPE then TYPE is updated to current class type
    if tipo == CT.SelfType:
        new.returned_type = index
    else:
        new.returned_type = tipo
    # Type of new is TYPE
    return new.returned_type

def equal_visitor(equal: EqualNode, index: CT.Tipos, scope: dict):
    # Check LEXPR
    left = expression_visitor(equal.lvalue, index, scope)
    # Check REXPR
    right = expression_visitor(equal.rvalue, index, scope)
    # Check type(LEXPR) is equal to type(REXPR) and must be Int, Bool or String
    static_types = [CT.IntType, CT.BoolType, CT.StringType]
    if (left in static_types or right in static_types) and left != right:
        append_error_semantic(equal.lineno, equal.colno,f'TypeError: Illegal comparison with a basic type.')
    # Type of the equal is Bool
    equal.returned_type = CT.BoolType
    return CT.BoolType

def is_void_expr_visitor(isvoid: IsVoidNode, index: CT.Tipos, scope: dict):
    # Check EXPR
    expression_visitor(isvoid.val, index, scope)
    # Type of the isvoid is Bool
    isvoid.returned_type = CT.BoolType
    return CT.BoolType

__visitors__ = {
    AttrDeclarationNode: def_attribute_visitor,
    FuncCallNode: func_call_visitor,
    BoolNode: bool_visitor,
    StringNode: string_visitor,
    IntNode: int_visitor,
    BlockNode: block_expr_visitor,      
    VarNode: var_visitor,    
    DivNode: arithmetic_operator_visitor,
    PlusNode: arithmetic_operator_visitor,    
    MultNode: arithmetic_operator_visitor,
    MinusNode: arithmetic_operator_visitor,    
    IntCompNode: negation_visitor,
    NewNode: new_expr_visitor,
    NotNode: logic_negation_visitor,    
    AssignNode: assignment_visitor,
    EqualNode: equal_visitor,      
    LessEqualNode: comparison_visitor,
    LessThanNode: comparison_visitor,
    LetNode: let_visitor,
    IfNode: if_visitor,    
    CaseNode: case_expr_visitor,
    IsVoidNode: is_void_expr_visitor,
    WhileNode: loop_expr_visitor    
}   