WRONG_SIGNATURE = 'Method "{0}" already defined in "{1}" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
ATTRIBUTE_NOT_DEFINED = 'Attribute "{0}" is not defined in class "{1}".'
ATTRIBUTE_ALREADY_DEFINED = 'Attribute "{0}" is already defined in class "{1}".'
LOCAL_ALREADY_DEFINED = 'Variable "{0}" is already defined in method "{1}".'
INCOMPATIBLE_TYPES = 'Cannot convert "{0}" into "{1}".'
VARIABLE_NOT_DEFINED = 'Variable "{0}" is not defined in "{1}".'
INVALID_UNARY_OPERATION = 'Operation {0} is not defined with "{1}".'
INVALID_BINARY_OPERATION = 'Operation {0} is not defined between "{1}" and "{2}".'
NOT_BOOLEAN_CONDITION = 'A conditional must be a Bool type instead of {0} type.'
CIRCULAR_DEPENDENCY = 'Circular Dependency with types "{0}" and "{1}".'
VOID_TYPE_CONFORMS = "Void is not a valid type."
NO_OPERATION_DEFINDED = "No operations defined with operator {0} and types {1}."
MULTIPLE_OPERATION_DEFINED = "Multiple operations defined with operator {0} and types {1}."
CASE_NO_BRANCH_SELECTED = "No branch can be selected. Type {0} is not conformed by any of the branches."
NO_BOOL_CONDITION = "The condition value type is not Bool."
DISPATCH_VOID = "Can't dispatch a Void value."
METHOD_NOT_DEFINED = "Method '{0}' is not defined{1} in '{2}' with {3} params."
METHOD_ALREADY_DEFINED = "Method '{0}' with {1} params already defined in {2}"
NO_ENTRY_POINT = "The program must define a 'main' method with no parameters in the 'Main' class"
NO_MAIN_TYPE = "The program must define a 'Main' type"
CASE_TYPES_REPEATED = "Type {0} already present in case expression."
ZERO_DIVISION = "Divison by 0 not defined."
SUBSTR_OUT_RANGE = "Index out of range in substr, word:'{0}' substr begin:{1} substr length:{2}."
ATTRIBUTE_CANT_INFER = "No attribute '{0}' in inferred types."
METHOD_CANT_INFER = "No method '{0}' with {1} params in inferred types."
TYPE_NOT_DEFINED = "Type '{0}' is not defined."
TYPE_ALREADY_DEFINED = "Type with the same name ({0}) already in context."
TYPE_CANT_INFER = "Cant infer type in given context."

class CoolError(Exception):
    @property
    def text(self):
        return self.args[0]


class SemanticError(CoolError):
    pass

class InferError(SemanticError):
    pass

class RunError(CoolError):
    pass

class CoolTypeError(CoolError):
    pass
