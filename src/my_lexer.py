import ply.lex as lex
from ply.lex import TOKEN
from errors import LexicographicError

#Reserved words
keywords = {
		'class': 'CLASS',
		'let': 'LET',
		'loop': 'LOOP',
		'inherits': 'INHERITS',
		'pool': 'POOL',
		'if': 'IF',
		'then': 'THEN',
		'else': 'ELSE',
		'fi': 'FI',
		'while': 'WHILE',
		'case': 'CASE',
		'of': 'OF',
		'esac': 'ESAC',
		'new': 'NEW',
		'not': 'NOT',
		'isvoid': 'ISVOID',
		'in': 'IN',
		'true': 'TRUE',
		'false': 'FALSE'
}

#Declare the tokens
tokens = ('TYPE', 'ID', 'INTEGER', 'STRING', 'ACTION', 
			"LPAREN", "RPAREN", "LBRACE", "RBRACE", "COLON", 
			"COMMA", "DOT", "SEMICOLON", "AT", "PLUS", "MINUS", 
			"MULTIPLY", "DIVIDE", "EQ", "LT", "LTEQ", "ASSIGN", 
			"COMPLEMENT") + tuple(keywords.values())

class MyLexer:
	def __init__(self, data):
		self.tokens = tokens
		self.keywords = keywords
		self.lexer = None
		self.data = data
		self.errors = False
		self.eof = False
	
	#Build the lexer
	def build(self, **kwargs):
		self.lexer = lex.lex(module=self, **kwargs)
	
	def input(self, code):
		self.lexer.input(code)

	def token(self):
		next_token = None
		try:
			next_token = self.lexer.token()
		except:
			pass
		return next_token
	
	def check(self):
		self.input(self.data)
		while not self.eof:
			self.token()
		return self.errors
		
	#Declare the states
	@property
	def states(self):
		return (
				('string', 'exclusive'),
				('comment1', 'exclusive'),
				('comment2', 'exclusive'),        
			   )
	
	#Ignored characters
	t_ignore = ' \t\r\f\v'

	@TOKEN(r'\d+')
	def t_INTEGER(self, token):
		token.value = int(token.value)
		token.lexpos = find_column(self.data, token.lexpos)
		return token

	@TOKEN(r'[A-Z][a-zA-Z_0-9]*')
	def t_TYPE(self, token):
		#Check for reserved words
		value = token.value.lower()
		if value in self.keywords.keys(): 
			token.value = value
			token.type = self.keywords[value]
		else:
			token.type = "TYPE"
		token.lexpos = find_column(self.data, token.lexpos)
		return token

	@TOKEN(r'[a-z][a-zA-Z_0-9]*')
	def t_ID(self, token):
		#Check for reserved words
		value = token.value.lower()
		if value in self.keywords.keys(): 
			token.value = value
			token.type = self.keywords[value]
		else:
			token.type = "ID"
		token.lexpos = find_column(self.data, token.lexpos)
		return token

	@TOKEN(r'\n+')
	def t_newline(self, token):
		token.lexer.lineno += len(token.value)

	#EOF handling rule
	def t_eof(self, token):
		self.eof = True
		return None
		
	@TOKEN(r'\"')
	def t_start_string(self, token):
		token.lexer.push_state("string")
		token.lexer.string_backslashed = False
		token.lexer.string_buffer = ""
		token.lexer.string_lineno = token.lineno
		token.lexer.string_lexpos = find_column(self.data, token.lexpos)

	@TOKEN(r'\n')
	def t_string_newline(self, token):
		token.lexer.lineno += 1
		if not token.lexer.string_backslashed:
			self.errors = True
			token.lexpos = find_column(self.data, token.lexpos)
			print(LexicographicError(token.lineno, token.lexpos, "Unterminated string constant"))
			token.lexer.pop_state()
		else:
			token.lexer.string_backslashed = False

	@TOKEN(r'\"')
	def t_string_end(self, token):
		if not token.lexer.string_backslashed:
			token.lexer.pop_state()
			token.lineno = token.lexer.string_lineno
			token.lexpos = token.lexer.string_lexpos
			token.value = token.lexer.string_buffer
			token.type = "STRING"
			return token
		else:
			token.lexer.string_buffer += '"'
			token.lexer.string_backslashed = False

	@TOKEN(r'[^\n]')
	def t_string_anything(self, token):
		if token.value == '\0':
			token.lexpos = find_column(self.data, token.lexpos)
			self.errors = True
			print(LexicographicError(token.lineno, token.lexpos, "String contains null character"))
		if token.lexer.string_backslashed:
			if token.value == 'b':
				token.lexer.string_buffer += '\b'
			elif token.value == 't':
				token.lexer.string_buffer += '\t'
			elif token.value == 'n':
				token.lexer.string_buffer += '\n'
			elif token.value == 'f':
				token.lexer.string_buffer += '\f'
			elif token.value == '\\':
				token.lexer.string_buffer += '\\'
			else:
				token.lexer.string_buffer += token.value
			token.lexer.string_backslashed = False
		else:
			if token.value != '\\':
				token.lexer.string_buffer += token.value
			else:
				token.lexer.string_backslashed = True

	#String error handler
	def t_string_error(self, token):
		token.lexer.skip(1)

	def t_string_eof(self, token):
		self.errors = True
		self.eof = True
		token.lexpos = find_column(self.data, token.lexpos)
		print(LexicographicError(token.lineno, token.lexpos, "EOF in string constant"))
	
	#String ignored characters
	t_string_ignore = ''

	#Comments type 1 State
	@TOKEN(r'\-\-')
	def t_start_comment1(self, token):
		token.lexer.push_state("comment1")

	@TOKEN(r'\n')
	def t_comment1_end(self, token):
		token.lexer.lineno += 1
		token.lexer.pop_state()	
	
	def t_comment1_error(self, token):
		self.lexer.skip(1)

	#Comment ignored characters
	t_comment1_ignore = ''
	
	#Comments type 2 State
	@TOKEN(r'\(\*')
	def t_start_comment2(self, token):
		token.lexer.push_state("comment2")

	@TOKEN(r'\(\*')
	def t_comment2_nested(self, token):
		token.lexer.push_state("comment2")

	@TOKEN(r'\*\)')
	def t_comment2_end(self, token):
		token.lexer.pop_state()

	@TOKEN(r'\n')
	def t_comment2_newline(self, token):
		token.lexer.lineno += 1
	
	def t_comment2_error(self, token):
		self.lexer.skip(1)
		
	def t_comment2_eof(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		self.errors = True
		self.eof = True
		print(LexicographicError(token.lineno, token.lexpos, "EOF in comment"))
		return None

	#Comment ignored characters
	t_comment2_ignore = ''

	#Operators
	@TOKEN(r'\+')
	def t_PLUS(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\-')
	def t_MINUS(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\*')
	def t_MULTIPLY(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\/')
	def t_DIVIDE(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'\:')
	def t_COLON(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\;')
	def t_SEMICOLON(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token

	@TOKEN(r'\(')
	def t_LPAREN(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\)')
	def t_RPAREN(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token	
	
	@TOKEN(r'\{')
	def t_LBRACE(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\}')
	def t_RBRACE(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\@')
	def t_AT(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\.')
	def t_DOT(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'\,')
	def t_COMMA(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\=\>')
	def t_ACTION(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	@TOKEN(r'\=')
	def t_EQ(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'\<\=')
	def t_LTEQ(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'\<\-')
	def t_ASSIGN(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'\<')
	def t_LT(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
		
	@TOKEN(r'~')
	def t_COMPLEMENT(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		return token
	
	#Error handling rule
	def t_error(self, token):
		token.lexpos = find_column(self.data, token.lexpos)
		self.errors = True
		print(LexicographicError(token.lineno, token.lexpos, "ERROR \"{}\"".format(token.value[0])))
		token.lexer.skip(1)
		
def find_column(data, lexpos):
	index = data.rfind('\n', 0, lexpos) + 1
	colum = 0
	n = 0
	while index < lexpos:
		c = data[index]
		if c == '\t':
			colum += 4 - n
			n = 0
		else:
			colum = colum + 1
			n += 1
			if n == 4:
				n = 0
		index += 1
	return colum + 1
