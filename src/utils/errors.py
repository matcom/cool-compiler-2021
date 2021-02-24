
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

