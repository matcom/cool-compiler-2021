from compiler_component import CompilerComponent
import ply.lex as lex

# funcion que retorna el texto de la linea donde hubo un error lexico
def printLine(text, lineno): #text = texto a tokenizar, lineno: linea donde hubo error
    count = 0
    start_index = 0
    last_index = 0
    for i in range(len(text)):
        if text[i] == '\n':
            count += 1
            if count == lineno:
                last_index = i
                break

            if count == lineno-1:
                start_index = i

    return text[start_index +1: last_index] 

class Tokenizer:

    def __init__(self):
        self.errors = []    

    reserved = {

        'class':'CLASS',
        'else':'ELSE',
        'false':'FALSE',
        'fi':'FI',
        'if':"IF",
        'in':'IN',
        'inherits': 'INHERITS',
        'isvoid':'ISVOID',
        'let':'LET',
        'loop':'LOOP',
        'pool':'POOL',
        'then':'THEN',
        'while':'WHILE',
        'case':'CASE',
        'esac':'ESAC',
        'new':'NEW',
        'of':'OF',
        'not':'NOT',
        'true':'TRUE'

    }

    tokens = ['STRING', 'LPAREN', 'RPAREN', 'LBRACE' , 'RBRACE', 'PLUS', 'MINUS',
    'TIMES', 'DIVIDE', 'SEMICOLON', 'COMMA', 'ID', 'MINOR', 'MINOR_EQUALS', "EQUALS", 
    'LEFT_ARROW', 'RIGHT_ARROW', 'DOT', 'DOUBLE_DOT', "ARROBA", 'NUMBER'] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_SEMICOLON = r';'
    r_COMMA = r','
    t_MINOR = r'<'
    t_MINOR_EQUALS = r'<='
    t_EQUALS = r'='
    t_LEFT_ARROW = r'<-'
    t_RIGHT_ARROW = r'=>'
    t_DOT = r'\.'
    t_DOUBLE_DOT = r':'
    t_ARROBA = r'@'

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^"]*"'
        return t    

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        v = t.value.lower()
        #true o false tienen que escribirse en letra inicial minuscula, de lo contrario son IDs
        if v == 'true' or v == 'false':
            if t.value[0] == 'T' or t.value[0] == 'F':
                return t

        t.type = self.reserved.get(t.value.lower(), 'ID')
        return t

    def t_comment(self, t):
        r'--[^\n]*\n'
        t.lexer.lineno += 1

    def t_comment_end_string(self, t):
        r'--[^$]*$'
        t.lexer.lineno += 1  

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        error = 'Error en la linea ' + str(t.lexer.lineno) + ': \'' + printLine(t.lexer.lexdata, t.lexer.lineno)
        error += '\' -->  Problema con el caracter \'' + t.value[0] + '\''
        self.errors.append(error)
        t.lexer.skip(1)


    t_ignore_WHITESPACE = r'\s'

    #funcion para tokenizar (devuelve una tupla: (tokens, errores))
    def tokenize(self, data, lexer): #data: texto a tokenizar, lexer: encargado de tokenizar, el campo object del lexer debe ser de tipo Tokenizer
        self.errors = [] #se almacenan los errores en el proceso de tokenizar
        
        lexer.input(data)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                return (tokens, self.errors)
            tokens.append(tok)

class Lexer(CompilerComponent):
    def __init__(self, cool_program: str) -> None:
        super().__init__()
        self.cool_program = cool_program
        self.errors = []

    def execute(self):
        tokenizer = Tokenizer()
        lexer = lex.lex(tokenizer)
        tokens, self.errors = tokenizer.tokenize(self.cool_program, lexer)
        for t in tokens:
            print(t)

    def has_errors(self):
        return len(self.errors) == 0

    def print_errors(self):
        for e in self.errors:
            print(e)

########################### Testing ##############################
data = '''--aaaa
--bbbbadsfdasg
a+4class{}(a)let if fi while = <=<
--aaa'''
lexer = Lexer(data)

##### borrar luego ########################################