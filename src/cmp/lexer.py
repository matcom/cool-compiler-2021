import ply.lex as lex



reserved = {
	'class': 'CLASS',
	'inherits': 'INHERITS',
	'if': 'IF',
	'then': 'THEN',
	'else': 'ELSE',
	'fi': 'FI',
	'while': 'WHILE',
	'loop': 'LOOP',
	'pool': 'POOL',
	'let': 'LET',
	'in': 'IN',
	'case': 'CASE',
	'of': 'OF',
	'esac': 'ESAC',
	'new': 'NEW',
	'isvoid': 'ISVOID',
    'not': 'NOT'
}

ignored = [' ', '\f', '\r', '\t', '\v']

tokens = [
	# Identifiers
	'TYPE',
    'ID',
	# Basic classes
	'INTEGER',
    'STRING',
    'BOOL',
	# Special keywords
	'ACTION',
    # Literals
    'SUM',  
    'MINUS',
    'STAR',
    'DIVIDE',
    'COLON',
    'SEMICOLON',
    'OPAREN',
    'CPAREN',
    'OBRACE',
    'CBRACE',
    'AT',
    'DOT',
    'COMMA',
	# Operators
	'ASSIGN', 
    'LESS', 
    'LESSEQUAL', 
    'EQUAL', 
    'INT_COMPLEMENT',
    # Comment
    'COMMENT'
] + list(reserved.values())

def t_TYPE(token):
    r'[A-Z][\w]*'
    return token

def t_ID(token):
    r'[a-z][\w]*'
    token.type = reserved.get(token.value.lower(),'ID')
    return token

def t_INTEGER(token):
    r'\d+'
    token.value = int(token.value)
    return token

def t_STRING(token):
    r'"[^"]*"'
    token.value = token.value[1:-1]
    return token

def t_BOOL(token):
    r'true|false'
    token.value = True if token.value == 'true' else False
    return token

t_ACTION = r'\=\>'    
t_SUM = r'\+'        
t_MINUS = r'\-'       
t_STAR = r'\*'    
t_DIVIDE = r'\/'      
t_COLON = r'\:'       
t_SEMICOLON = r'\;'   
t_OPAREN = r'\('      
t_CPAREN = r'\)'      
t_OBRACE = r'\{'      
t_CBRACE = r'\}'      
t_AT = r'\@'          
t_DOT = r'\.'         
t_COMMA = r'\,'       
t_ASSIGN = r'\<\-'    
t_LESS = r'\<'          
t_LESSEQUAL = r'\<\='      
t_EQUAL = r'\='          
t_INT_COMPLEMENT = r'~'     

states = (('COMMENT','exclusive'),)

def t_lineCOMMENT(token):
    r'\-\-[^\n]*'

def t_startCOMMENT(token):
    r'\(\*'
    token.lexer.begin('COMMENT')
    token.lexer.comment_count = 1

def t_COMMENT_open(token):
    r'\(\*'
    token.lexer.comment_count += 1

def t_COMMENT_close(token):
    r'\*\)'
    token.lexer.comment_count -= 1
    if token.lexer.comment_count == 0:
        token.lexer.begin('INITIAL')

def t_COMMENT_newline(token):
    r'\n'
    token.lexer.lineno += 1

def t_COMMENT_error(token):
    token.lexer.skip(1)

def t_newline(token):
    r'\n'
    token.lexer.lineno += 1



t_ignore = ''.join(ignored)

def t_error(token):
    print("Illegal character {} at line {}".format(token.value[0], token.lexer.lineno))
    token.lexer.skip(1)


lexer = lex.lex()
lexer.input('"annon_" true \n + (*jojo\njo*)  "hola"')
while(True):
    token = lexer.token()
    
    if token is None:
        break
    print(token)
    print(token.value)
    