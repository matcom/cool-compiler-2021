from error.errors import PositionError

STRING_TOO_LONG = "String too long. Max length is 1024 chars, have {0} chars"

SYNTACTIC_ERROR = 'at or near {0}'
REDEFINITION_BASIC_CLASS = 'Redefinition of basic class {0}.'
METHOD_REDEFINED_WRONG_SIGNATURE_PARAM = 'In redefined method {0}, parameter type {1} is different from original type {2}.'
METHOD_REDEFINED_WRONG_SIGNATURE_RETURN = "In redefined method {0}, return type {1} is different from original return type {2}."
METHOD_REDEFINED_WRONG_PARAM_AMOUNT = "Incompatible number of formal parameters in redefined method {0}."
SELF_IS_READONLY = 'Variable "self" is read-only.'
ASSIGN_SELF = "Cannot assign to 'self'."
LET_BOUND_SELF = "'self' cannot be bound in a 'let' expression."
PARAM_NAME_SELF = "'self' cannot be the name of a formal parameter."
ATTRIBUTE_NAME_SELF = "'self' cannot be the name of an attribute."
ATTRIBUTE_NOT_DEFINED = 'Attribute "{0}" is not defined in class "{1}".'
ATTRIBUTE_ALREADY_DEFINED = 'Attribute {0} is multiply defined in class.'
ATTRIBUTE_ALREADY_DEFINED_IN_PARENT = 'Attribute {0} is an attribute of an inherited class.'
LOCAL_ALREADY_DEFINED = 'Variable "{0}" is already defined in method "{1}".'
INCOMPATIBLE_TYPES = "Inferred type {0} of initialization of {1} does not conform to identifier's declared type {2}."
UNDEFINED_CLASS_CASE_BRANCH = 'Class {0} of case branch is undefined.'
UNDEFINED_PARAM_TYPE = "Class {0} of formal parameter {1} is undefined."
UNDEFINED_RETURN_TYPE = "Undefined return type {0} in method {1}."
UNDEFINED_NEW_TYPE = "'new' used with undefined class {0}."
ATTRIBUTE_INCOMPATIBLE_TYPES = 'Inferred type {2} of initialization of attribute {0} does not conform to declared type {1}.'
METHOD_INCOMPATIBLE_RETURN_TYPE = "Inferred return type {2} of method {0} does not conform to declared return type {1}."
VARIABLE_NOT_DEFINED = 'Undeclared identifier {0}.'
INVALID_UNARY_OPERATION = "Argument of '{0}' has type {1} instead of {2}."
INVALID_BINARY_OPERATION = 'non-{1} arguments: {1} {0} {2}'
NOT_BOOLEAN_CONDITION = "Predicate of 'if' does not have type Bool."
WHILE_NOT_BOOLEAN_CONDITION = "Loop condition does not have type Bool."
CIRCULAR_DEPENDENCY = 'Class {0}, or an ancestor of {0}, is involved in an inheritance cycle.'
VOID_TYPE_CONFORMS = "Void is not a valid type."
NO_OPERATION_DEFINDED = "No operations defined with operator {0} and types {1}."
MULTIPLE_OPERATION_DEFINED = "Multiple operations defined with operator {0} and types {1}."
CASE_NO_BRANCH_SELECTED = "No branch can be selected. Type {0} is not conformed by any of the branches."
NO_BOOL_CONDITION = "The condition value type is not Bool."
DISPATCH_VOID = "Can't dispatch a Void value."
DISPATCH_UNDEFINED_METHOD = "Dispatch to undefined method {0}."
DISPATCH_METHOD_WRONG_ARGS = "Method {0} called with wrong number of arguments."
STATIC_DISPATCH_INCOMPATIBLE_TYPES = "Expression type {0} does not conform to declared static dispatch type {1}."
INCOMPATIBLE_PARAMS_TYPES = "In call of method {0}, type {1} of parameter {2} does not conform to declared type {3}."
METHOD_NOT_DEFINED = "Method '{0}' is not defined{1} in '{2}' with {3} params."
METHOD_ALREADY_DEFINED = "Method {0} is multiply defined."
METHOD_REPEATED_ARGS_NAME = "Formal parameter {0} is multiply defined."
ATTRIBUTE_TYPE_UNDEFINED = "Class {0} of attribute {1} is undefined."
NO_ENTRY_POINT = "The program must define a 'main' method with no parameters in the 'Main' class"
NO_MAIN_TYPE = "The program must define a 'Main' type"
INVALID_EQUAL_BASIC_TYPE_OPERATION = "Illegal comparison with a basic type."
CASE_TYPES_REPEATED = "Duplicate branch {0} in case statement."
ZERO_DIVISION = "Divison by 0 not defined."
SUBSTR_OUT_RANGE = "Index out of range in substr, word:'{0}' substr begin:{1} substr length:{2}."
ATTRIBUTE_CANT_INFER = "No attribute '{0}' in inferred types."
METHOD_CANT_INFER = "No method '{0}' with {1} params in inferred types."
TYPE_NOT_DEFINED = "Type '{0}' is not defined."
LET_BOUND_TYPE_NOT_DEFINED = "Class {0} of let-bound identifier {1} is undefined."
TYPE_ALREADY_DEFINED = "Classes may not be redefined"
TYPE_CANT_INFER = "Cant infer type in given context."
TYPE_CANT_BE_INHERITED = "Class {0} cannot inherit class {1}."
UNDEFINED_INHERITED_TYPE = "Class {0} inherits from an undefined class {1}."
NO_COMMON_TYPE = "No common types between {0} and {1}"
READ_IS_NOT_INT = "Invalid type: {0} is not an Int"

class LexerCoolError(PositionError):
    """
    Error class for lexical errors
    """
    
    FORMAT = "({}, {}) - {}: {}"
    
    ERROR_TYPE = "LexicographicError"

class SemanticError(PositionError):
    """
    Error class for semantic errors
    """

    FORMAT = "({}, {}) - {}: {}"
    ERROR_TYPE = "SemanticError"

class SyntacticCoolError(PositionError):
    """
    Error class for syntactic errors
    """

    ERROR_TYPE = "SyntacticError"

class NameCoolError(SemanticError):
    ERROR_TYPE = "NameError"

class TypeCoolError(SemanticError):
    ERROR_TYPE = "TypeError"

class AttributeCoolError(SemanticError):
    ERROR_TYPE = "AttributeError"
    
class InferError(SemanticError):
    ERROR_TYPE = "InferenceError"

