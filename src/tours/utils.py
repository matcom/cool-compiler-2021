from parsing.ast import *
from cmp.semantic import ErrorType, ObjectType, SelfType 


def find_parent_type(current_type, type1, type2):
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


def is_base_class(id):
    return id in ['Object', 'IO', 'Int', 'String', 'Bool']