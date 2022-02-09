from parsing.ast import *
from cmp.semantic import SemanticError, Attribute, Method, Context
from cmp.semantic import Type, ErrorType, StringType, IntType, AutoType, BoolType, ObjectType, IOType, SelfType 

def AnalizeClassAutoTypes(class_type, errors, inferences):
    for attribute in class_type.attributes:
        if attribute.type == AutoType():
            if attribute.type.infered_type is None:
                errors.append(f"Can not infered the type of the attribute '{attribute.name}' of the class '{class_type.name}'.")
            else:
                inferences.append(f"The type of the attribute '{attribute.name}' of the class '{class_type.name}' was infered to '{attribute.type.infered_type.name}'.")

    for method in class_type.methods:
        if method.return_type == AutoType():
            if method.return_type.infered_type is None:
                errors.append(f"Can not infered the return type of the method '{method.name}' of the class '{class_type.name}'.")
            else:
                inferences.append(f"The return type of the method '{method.name}' of the class '{class_type.name}' was infered to '{method.return_type.infered_type.name}'.")

def AnalizeScopeAutoTypes(scope, errors, inferences):
    stack = [scope]
    while len(stack) != 0:
        temp = stack.pop(0)
        for s in temp.children:
            stack.append(s)

        for var in temp.locals:
            if var.type == AutoType():
                if var.type.infered_type is None:
                    errors.append(f"Can not infered the type of the variable '{var.name}' of the class '{temp.class_name}'.")
                else:
                    inferences.append(f"The type of the variable '{var.name}' of the class '{temp.class_name}' was infered to '{var.type.infered_type.name}'.")

def find_parent_type(current_type, type1, type2):
    if type1 == AutoType() and type2 != AutoType():
        return type2
    elif type2 == AutoType():
        return type1

    if type1 == SelfType():
        type1 = current_type
    if type2 == SelfType():
        type2 = current_type

    if type1 == type2:
        return type1
    elif type1 == ErrorType() or type2 == ErrorType():
        return ErrorType()
    elif type1 == ObjectType() or type2 == ObjectType():
        return ObjectType()
    
    parent1 = find_parent_type(current_type, type1.parent, type2)
    parent2 = find_parent_type(current_type, type1, type2.parent)
    parent3 = find_parent_type(current_type, type1.parent, type2.parent)

    if parent1.conforms_to(parent2):
        temp = parent1
    else:
        temp = parent2

    if temp.conforms_to(parent3):
        return temp 
    else:
        return parent3 

def InferType(current_type, auto_var, not_auto_var):
    if not_auto_var != ErrorType():
        if auto_var.infered_type is not None:
            temp = find_parent_type(current_type, auto_var.infered_type, not_auto_var)
           
            if auto_var.infered_type != temp :
                auto_var.infered_type = temp
                return True
        else:
            auto_var.infered_type = not_auto_var 
            return True

    return False