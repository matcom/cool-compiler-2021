import ply.lex as lex
import utils.ast_nodes as ast

lexer_errors = []

tokens = ('NUMBER', # otros
          'USTRING',  
          'STRING',
          'ID',
          'TYPE',
          'TRUE',
          'FALSE',
          'MINUS', # simbolos matematicos
          'PLUS',
          'DIV',
          'TIMES',
          'LESS',
          'LESSEQUAL',
          'EQUAL',
          'COMPLEMENT',
          'OBRACE', # signos de puntuacion
          'CBRACE',
          'OPAR',
          'CPAR',
          'DOT',
          'COMA',
          'COLON',
          'SEMI',
          'ARROBA',
          'ASSIGN',
          'ARROW',
          'SINGLE_LINE_COMMENT', # comentarios
          )

# palabras reservadas
reserved = {
    'if'      : 'IF',
    'then'    : 'THEN',
    'else'    : 'ELSE',
    'fi'      : 'FI',
    'inherits': 'INHERITS',
    'class'   : 'CLASS',
    'while'   : 'WHILE',
    'loop'    : 'LOOP',
    'pool'    : 'POOL',
    'let'     : 'LET',
    'in'      : 'IN',
    'case'    : 'CASE',
    'of'      : 'OF',
    'esac'    : 'ESAC',
    'new'     : 'NEW',
    'isvoid'  : 'ISVOID',
    'not'     : 'NOT',
}

booleans = ['true', 'false']

tokens = list(tokens) + list(reserved.values())

t_SINGLE_LINE_COMMENT = r'--.*'


###############  Bloque turistico  #################
def t_TYPE(t):
    r'[A-Z][a-zA-Z_0-9]*'
    if t.value.lower() in reserved.keys(): # Check for reserved words
        t.type = reserved.get(t.value, reserved[t.value.lower()])
    elif t.value.lower() in booleans: # Generating booleans 
        t.type = reserved.get(t.value.lower == "true", t.value.upper())
    else:
        t.type = reserved.get(t.value,'TYPE')
    return t

def t_ID(t): 
    r'[a-z][a-zA-Z_0-9]*'
    if t.value.lower() in reserved.keys(): # Check for reserved words
        t.type = reserved.get(t.value, reserved[t.value.lower()])
    elif t.value.lower() in booleans: # Generating booleans
        t.type = reserved.get(t.value.lower == "true", t.value.upper())
    else:
        t.type = reserved.get(t.value,'ID') 
    return t
#####################################################W

def t_STRING(t):
    # r'\"(.|\\\n)*\"'
    r'\"([^\r\n\"\\]|(\\\n)|(\\.))*\"'
    
    t.lineno += t.value.count('\n')
    t.type = reserved.get(t.value,'STRING') 
    return t

def t_USTRING(t):
    # r'\"(.|\\\n)*\"'
    r'\"([^\r\n\"\\]|(\\\n)|(\\.))*'
    
    t.lineno += t.value.count('\n')
    t.type = reserved.get(t.value,'USTRING') 
    return t

##########################################################

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIV  = r'/'
t_LESSEQUAL = r'<='
t_LESS = r'<'
t_COMPLEMENT = r'~'
t_EQUAL = r'='

t_OPAR = r'\('
t_CPAR = r'\)'
t_OBRACE = r'{'
t_CBRACE = r'}'
t_DOT = r'\.'
t_SEMI = r';'
t_COLON = r':'
t_ARROBA = r'@'
t_ASSIGN = r'<-'
t_ARROW = r'=>'
t_COMA = r'\,'



def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    t.lexer.skip(1)
    lexer_errors.append(('error', t.lineno, t.lexpos, t.value[0]))
   

lexer = lex.lex()
