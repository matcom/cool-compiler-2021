ATTRIBUTE_OVERRIDE_ERROR = '(%d, %d) - SemanticError: Attribute "%s" already defined in "%s", attributes cannot be overridden'
METHOD_OVERRIDE_PARAM_ERROR = '(%d, %d) - SemanticError: In redefinded method "%s", the number of parameters different from the original definition. Expected %d, instead of %d'
METHOD_OVERRIDE_PARAM_ERROR = '(%d, %d) - SemanticError: In redefinded method "%s", param type "%s" is different from original param type "%s"'
METHOD_OVERRIDE_RETURN_ERROR = '(%d, %d) - SemanticError: In redefinded method "%s", return type "%s" is different from original return type "%s"'

INCOMPATIBLE_TYPES = '(%d, %d) - TypeError: Cannot convert "%s" into "%s".'
INVALID_PARAM_TYPE = (
    '(%d, %d) - TypeError: "%s" cannot be a static type of a parameter.'
)
INVALID_CASE_TYPE = (
    '(%d, %d) - TypeError: "%s" cannot be a static type of a case branch.'
)
INVALID_PARENT_TYPE = '(%d, %d) - SemanticError: Class "%s" cannot inherits from "%s"'
INVALID_ANCESTOR = '(%d, %d) - TypeError: Class "%s" has no an ancestor class "%s".'

INVALID_EQ_COMPARISON_OPERATION = '(%d, %d) - TypeError: For operation "=" if one of the expression has static type Int, Bool or String, then the other must have the same static type'
INVALID_BINARY_OPERATION = (
    '(%d, %d) - TypeError: Operation "%s" is not defined between "%s" and "%s".'
)
INVALID_UNARY_OPERATION = (
    '(%d, %d) - TypeError: Operation "%s" is not defined for "%s".'
)

DISPATCH_UNDEFINED_METHOD = (
    '(%d, %d) - AttributeError: Dispatch undefined method "%s" from type %s'
)
DISPATCH_WITH_WRONG_NUMBER_OF_ARGS = '(%d, %d) - SemanticError: Method "%s" of type "%s" called with wrong number of arguments. Expected %d instead of %d'


SELF_IS_READONLY = '(%d, %d) - SemanticError: Variable "self" is read-only.'
SELF_INVALID_ATTRIBUTE_ID = (
    '(%d, %d) - SemanticError: Cannot set "self" as attribute of a class.'
)
SELF_INVALID_PARAM_ID = (
    '(%d, %d) - SemanticError: Cannot set "self" as parameter of a method.'
)
SELF_USED_IN_LET = (
    '(%d, %d) - SemanticError: "self" cannot be bound in a "let" expression'
)
LOCAL_ALREADY_DEFINED = (
    '(%d, %d) - SemanticError: Variable "%s" is already defined in method "%s".'
)
UNDEFINED_VARIABLE = '(%d, %d) - NameError: Variable "%s" is not defined in "%s".'
INVALID_REDEFINITION_CLASS = (
    '(%d, %d) - SemanticError: Invalid redefinition of class "%s"'
)
PARENT_ALREADY_SET = '(%d, %d) - SemanticError: Parent type is already set for "%s"'
PARENT_UNDEFINED = (
    '(%d, %d) - TypeError: Parent type for class "%s" is an undefined type "%s"'
)
ATTRIBUTE_ALREADY_DEFINED = (
    '(%d, %d) - SemanticError: Attribute "%s" is already defined in "%s".'
)
METHOD_ALREADY_DEFINED = '(%d, %d) - SemanticError: Method "%s" already defined in %s'
DUPLICATE_BARNCH_IN_CASE = (
    '(%d, %d) - SemanticError: Duplicate branch "%s" in case statement'
)

CYCLIC_DEPENDENCY = '(%d, %d) - SemanticError: Class "%s", or an ancestor of "%s", is involved in an inheritance cycle'

UNDEFINDED_ATTRIBUTE = '(%d, %d) - SemanticError: Attribute "%s" is not defined in %s'
UNDEFINDED_METHOD = '(%d, %d) - SemanticError: Method "%s" is not defined in %s'
UNDEFINED_TYPE = '(%d, %d) - TypeError: Type "%s" is not defined'
UNDEFINED_NEW_TYPE = (
    '(%d, %d) - TypeError: Using "new" expresion with undefined type "%s"'
)
UNDEFINED_TYPE_IN_BRANCH = (
    '(%d, %d) - TypeError: Class "%s" of case branch is undefined'
)
UNDEFINED_RETURN_TYPE = (
    '(%d, %d) - TypeError: Undefined return type "%s" in method "%s", in class "%s"'
)
UNDEFINED_PARAM_TYPE = (
    '(%d, %d) - TypeError: Undefined param type "%s" in method "%s", in class "%s"'
)
UNDEFINED_ATTRIBUTE_TYPE = (
    '(%d, %d) - TypeError: Undefined type "%s" for attribute "%s" in class "%s"'
)

INFERENCE_ERROR_ATTRIBUTE = (
    '(%d, %d) - InferenceError: Cannot infer type for attribute "%s".'
)
INFERENCE_ERROR_PARAMETER = (
    '(%d, %d) - InferenceError: Cannot infer type for parameter "%s".'
)
INFERENCE_ERROR_VARIABLE = (
    '(%d, %d) - InferenceError: Cannot infer type for variable "%s".'
)
INFERENCE_ERROR_METHOD = (
    '(%d, %d) - InferenceError: Cannot infer return type for method "%s".'
)

DIVIDE_BY_ZERO = "(%d, %d) - ZeroDivisionError: Division by zero."
INPUT_INT_ERROR = "(%d, %d) - InputError: Expected a number."
MAIN_CLASS_NOT_FOUND = "(%d, %d) - MainClassNotFound: no Main class in program."
MAIN_METHOD_NOT_FOUND = "(%d, %d) - MainMethodNotFound: no main method in class Main."
VOID_EXPRESSION = "(%d, %d) - VoidReferenceError: Object reference not set to an instance of an object."
CASE_OF_ERROR = "(%d, %d) - CaseOfError: No branch matches wit de dynamic type of the case expression."
