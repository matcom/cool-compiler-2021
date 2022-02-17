"""
Compilation errors.
"""

# lexical analysis
LEX_ERROR = '(%s, %s) - LexicographicError: Unexpected symbol "%s".'
UNT_STR = '(%s, %s) - LexicographicError: Unterminated string.'
EOF_STR = '(%s, %s) - LexicographicError: EOF in string.'
NULL_STR = '(%s, %s) - LexicographicError: String contains null character.'
EOF_COMM = '(%s, %s) - LexicographicError: EOF in comment.'

# parsing
SYN_ERROR = '(%s, %s) - SyntacticError: Syntax error at or near "%s".'
SYN_EOF = '(0, 0) - SyntacticError: ERROR at or near EOF.'   # empty program

# semantic analysis
CANNOT_INHERIT = '%s - SemanticError: Type "%s" cannot be inherited.'
CYCLIC_INHERITANCE = '%s - SemanticError: Cyclic inheritance involving "%s".'
TYPE_ALREADY_DEFINED = '%s - SemanticError: Type "%s" already defined.'
ATTRIBUTE_DEFINED_IN_PARENT = '%s - SemanticError: Attribute "%s" is already defined in parent.'
ATTRIBUTE_ALREADY_DEFINED = '%s - SemanticError: Attribute "%s" already defined in "%s".'
METHOD_ALREADY_DEFINED = '%s - SemanticError: Method "%s" already defined in "%s".'
WRONG_SIGNATURE = '%s - SemanticError: Method "%s" already defined in "%s" with a different signature.'
LOCAL_ALREADY_DEFINED = '%s - SemanticError: Variable "%s" is already defined in method "%s".'
SELF_TYPE_INVALID_PARAM_TYPE = '%s - SemanticError: SELF_TYPE cannot be a static type for a parameter.'
SELF_INVALID_ID = '%s - SemanticError: Cannot define "self" as attribute of a class or an identifier.'
SELF_IS_READONLY = '%s - SemanticError: Variable "self" is read-only.'
CASE_DUPLICATED_BRANCH = '%s - SemanticError: Duplicate branch "%s" in case statement.'
UNDEFINED_METHOD = '%s - AttributeError: Method "%s" is not defined in "%s" or inherited.'
UNDEFINED_TYPE = '%s - TypeError: Type "%s" is not defined.'
INCOMPATIBLE_TYPES = '%s - TypeError: Cannot convert "%s" into "%s".'
INVALID_ANCESTOR = '%s - TypeError: Class "%s" has not class "%s" as ancestor.'
INVALID_BINARY_OPERATOR = '%s - TypeError: Operation "%s" is not defined between "%s" and "%s".'
INVALID_UNARY_OPERATOR = '%s - TypeError: Operation "%s" is not defined for "%s".'
VARIABLE_NOT_DEFINED = '%s - NameError: Variable "%s" is not defined in "%s".'
