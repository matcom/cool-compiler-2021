import sys

class Error:
	error_type = 'Error'

	def __init__(self, line, index, message):
		self.line = line
		self.index = index
		self.message = message

	def __str__(self):
		return '({}, {}) - {}: {}'.format(self.line, self.index, self.error_type, self.message)

class CompilerError(Error):
    '''
    Se reporta al detectar alguna anomalía con la entrada del compilador.
    Por ejemplo, si el fichero a compilar no existe
    '''
    error_type = "CompilerError"

class LexicographicError(Error):
    '''
    Errores detectados por el Lexer
    '''
    error_type = "LexicographicError"

class SyntacticError(Error):
    '''
    Errores detectados por el parser
    '''
    error_type = "SyntacticError"

class NameError(Error):
    '''
    Se reporta al referenciar un identificador en un ámbito que no es visible
    '''
    error_type = "NameError"

class TypeError(Error):
    '''
    Se reporta al detectar un problema de tipos. Incluye:
    - incompatibilidad de tipos entre rvalue y lvalue
    - operación no definida entre objetos de ciertos tipos, y
    - tipo referenciado no definido
    '''
    error_type = "TypeError"

class AttributeError(Error):
    '''
    Se reporta cuando un atributo o método se referencia pero no está definido
    '''

    error_type = "AttributeError"

class SemanticError(Error):
    '''
    Cualquier otro error semántico
    '''
    error_type = "SemanticError"
