
class CoolError(Exception):
    def __init__(self, line, column, text):
        super().__init__(text)
        self.line = line
        self.column = column

    @property
    def error_type(self):
        return 'CoolError'

    @property
    def text(self):
        return self.args[0]

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.error_type}: {self.text}'

    def __repr__(self):
        return str(self)

class CompilerError(CoolError):
    '''
    Errores detectados con la entrada del compilador.
    '''
    WRONG_EXTENTION = 'Cool program file must end with a ".cl" extension'
    UNKNOWN_FILE = 'The file "%s" does not exist'

    @property
    def error_type(self):
        return 'CompilerError'

class LexicographicError(CoolError):
    '''
    Errores detectados por el lexer.
    '''
    UNKNOWN_TOKEN = 'ERROR "%s"\n'
    UNTERMINATED_STRING = 'Unterminated string constant\n'
    EOF_COMMENT = 'EOF in comment\n'
    EOF_STRING = 'EOF in string constant\n'
    NULL_STRING = 'String contains null character\n'

    @property
    def error_type(self):
        return 'LexicographicError'

class SyntacticError(CoolError):
    '''
    Errores detectados por el parser.
    '''
    ERROR = 'ERROR at or near "%s"'

    @property
    def error_type(self):
        return 'SyntacticError'

class SemanticError(CoolError):
    '''
    Errores detectados por cualquier otro error semántico. 
    '''
    SELF_IS_READONLY = 'Cannot assign to \'self\''
    SELF_IN_LET = '\'self\' cannot be bound in a \'let\' expression'
    SELF_PARAM = "'self' cannot be the name of a formal parameter"
    SELF_ATTR = "'self' cannot be the name of an attribute"
    LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s"'
    ARGUMENT_ERROR = 'Method %s called with wrong number of arguments'
    REDEFINITION_ERROR = 'Redefinition of basic class %s'
    INHERIT_ERROR = 'Class %s cannot inherit class %s'
    DUPLICATE_CASE_BRANCH = 'Duplicate branch %s in case statement'
    TYPE_ALREADY_DEFINED = 'Classes may not be redefined'
    ATTRIBUTE_ALREADY_DEFINED = 'Attribute %s is multiply defined in class'
    ATTR_DEFINED_PARENT = 'Attribute %s is an attribute of an inherited class'
    METHOD_ALREADY_DEFINED = 'Method %s is multiply defined'
    CIRCULAR_DEPENDENCY = 'Class %s, or an ancestor of %s, is involved in an inheritance cycle'
    WRONG_SIGNATURE_RETURN = 'In redefined method %s, return type %s is different from original return type %s'
    WRONG_NUMBER_PARAM = 'Incompatible number of formal parameters in redefined method %s'
    PARAMETER_MULTY_DEFINED = 'Formal parameter %s is multiply defined'
    WRONG_SIGNATURE_PARAMETER = 'In redefined method %s, parameter type %s is different from original type %s'

    @property
    def error_type(self):
        return 'SemanticError'

class NamesError(SemanticError):
    '''
    Errores detectados al referenciar un identificador 
    en un ámbito en el que no es visible.
    '''
    VARIABLE_NOT_DEFINED = 'Undeclared identifier %s'
    
    @property
    def error_type(self):
        return 'NameError'

class TypesError(SemanticError):
    '''
    Errores detectados al identificar un problema de tipos.
    '''
    INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s"'
    ATTR_TYPE_ERROR = 'Inferred type %s of initialization of attribute %s does not conform to declared type %s'
    ATTR_TYPE_UNDEFINED = 'Class %s of attribute %s is undefined'
    BOPERATION_NOT_DEFINED = 'non-Int arguments: %s %s %s'
    COMPARISON_ERROR = 'Illegal comparison with a basic type'
    UOPERATION_NOT_DEFINED = 'Argument of \'%s\' has type %s instead of %s'
    CLASS_CASE_BRANCH_UNDEFINED  = 'Class %s of case branch is undefined'
    PREDICATE_ERROR = 'Predicate of \'%s\' does not have type %s'
    INCOSISTENT_ARG_TYPE = 'In call of method %s, type %s of parameter %s does not conform to declared type %s'
    INCOMPATIBLE_TYPES_DISPATCH = 'Expression type %s does not conform to declared static dispatch type %s'
    INHERIT_UNDEFINED = 'Class %s inherits from an undefined class %s'
    UNCONFORMS_TYPE = 'Inferred type %s of initialization of %s does not conform to identifier\'s declared type %s'
    UNDEFINED_TYPE_LET = 'Class %s of let-bound identifier %s is undefined'
    LOOP_CONDITION_ERROR = 'Loop condition does not have type Bool'
    RETURN_TYPE_ERROR = 'Inferred return type %s of method test does not conform to declared return type %s'
    PARAMETER_UNDEFINED = 'Class %s of formal parameter %s is undefined'
    RETURN_TYPE_UNDEFINED = 'Undefined return type %s in method %s'
    NEW_UNDEFINED_CLASS = '\'new\' used with undefined class %s'
    PARENT_ALREADY_DEFINED = 'Parent type is already set for "%s"'
    TYPE_NOT_DEFINED = 'Type "%s" is not defined'

    @property
    def error_type(self):
        return 'TypeError'

class AttributesError(SemanticError):
    '''
    Errores detectados cuando un atributo o método 
    se referencia pero no está definido.
    '''
    DISPATCH_UNDEFINED = 'Dispatch to undefined method %s'
    METHOD_NOT_DEFINED = 'Method "%s" is not defined in "%s"'
    ATTRIBUTE_NOT_DEFINED = 'Attribute "%s" is not defined in %s'

    @property
    def error_type(self):
        return 'AttributeError'