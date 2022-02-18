import ply.lex as lex
import utils.ast_nodes as ast

tokens = ('NUMBER', # otros
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
          'USTRING',          
          )

# palabras reservadas
reserved = {
    'if' : 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'inherits': 'INHERITS',
    'class': 'CLASS',
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
    'not': 'NOT',
}

tokens = list(tokens) + list(reserved.values())

t_SINGLE_LINE_COMMENT = r'--.*'


def t_TYPE(t):
    r'[A-Z][a-zA-Z_0-9]*'
    t.type = 'TYPE'
    return t

def t_ID(t):
    r'[a-z][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t


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


def t_IF(t):
    r'(i|I)(f|F)'
    t.type = reserved.get(t.value,'IF') 
    return t

def t_FI(t):
    r'(f|F)(i|I)'
    t.type = reserved.get(t.value,'FI') 
    return t

def t_THEN(t):
    r'(t|T)(h|H)(e|E)(n|N)'
    t.type = reserved.get(t.value,'THEN') 
    return t

def t_ELSE(t):
    r'(e|E)(l|L)(s|S)(e|E)'
    t.type = reserved.get(t.value,'ELSE') 
    return t

def t_INHERITS(t):
    r'(I|i)(N|n)(H|h)(E|e)(R|r)(I|i)(T|t)(S|s)'
    t.type = reserved.get(t.value,'INHERITS') 
    return t

def t_CLASS(t):
    r'(C|c)(L|l)(A|a)(S|s)(S|s)'
    t.type = reserved.get(t.value,'CLASS') 
    return t

def t_WHILE(t):
    r'(W|w)(H|h)(I|i)(L|l)(E|e)'
    t.type = reserved.get(t.value,'WHILE') 
    return t

def t_LOOP(t):
    r'(L|l)(O|o)(O|o)(P|p)'
    t.type = reserved.get(t.value,'LOOP') 
    return t

def t_LET(t):
    r'(l|L)(e|E)(t|T)'
    t.type = reserved.get(t.value,'LET') 
    return t

def t_IN(t):
    r'(i|I)(n|N)'
    t.type = reserved.get(t.value,'IN') 
    return t

def t_CASE(t):
    r'(C|c)(A|a)(S|s)(E|e)'
    t.type = reserved.get(t.value,'CASE') 
    return t

def t_OF(t):
    r'(o|O)(f|F)'
    t.type = reserved.get(t.value,'OF') 
    return t

def t_ESAC(t):
    r'(e|E)(s|S)(a|A)(c|C)'
    t.type = reserved.get(t.value,'ESAC') 
    return t

def t_NEW(t):
    r'(N|n)(E|e)(W|w)'
    t.type = reserved.get(t.value,'NEW') 
    return t

def t_ISVOID(t):
    r'(I|i)(S|s)(V|v)(O|o)(I|i)(d|D)'
    t.type = reserved.get(t.value,'ISVOID') 
    return t
    
def t_NOT(t):
    r'(N|n)(O|o)(t|T)'
    t.type = reserved.get(t.value,'NOT') 
    return t

##########################################################

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_TRUE(t):
    r'(T|t)(R|r)(U|u)(E|e)'
    t.value = True
    return t

def t_FALSE(t):
    r'(F|f)(A|a)(l|L)(s|S)(e|E)'
    t.value = False
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
    return ('error', t.lineno, t.lexpos, t.value[0])
   

lexer = lex.lex()
