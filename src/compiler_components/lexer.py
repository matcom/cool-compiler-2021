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
    'LEFT_ARROW', 'RIGHT_ARROW', 'DOT', 'DOUBLE_DOT', "ARROBA", 'NUMBER', 'SELF', 'NHANHARA'] + list(reserved.values())

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_SEMICOLON = r';'
    t_COMMA = r','
    t_MINOR = r'<'
    t_MINOR_EQUALS = r'<='
    t_EQUALS = r'='
    t_LEFT_ARROW = r'<-'
    t_RIGHT_ARROW = r'=>'
    t_DOT = r'\.'
    t_DOUBLE_DOT = r':'
    t_ARROBA = r'@'
    t_NHANHARA = r'~'
    
    def t_SELF(self, t):
        r'self'
        return t

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
    
    def t_commentMultiline(self, t):
        r'\(\*'
        s = ''
        count = 1
        end_re = lex.re.compile('\*\)')
        open_re = lex.re.compile('\(\*')
        any_re = lex.re.compile('[^\(\)\*]*')
        while count > 0:
            if t.lexer.lexpos == len(t.lexer.lexdata):
                break

            m = end_re.match(t.lexer.lexdata[t.lexer.lexpos:])
            
            if not m is None:
                s+= m.group()
                t.lexer.skip(2)
                count -= 1
                continue
            
            m = open_re.match(t.lexer.lexdata[t.lexer.lexpos:])
            if not m is None:
                s+=m.group()
                t.lexer.skip(2)
                count += 1
                continue

            m = any_re.match(t.lexer.lexdata[t.lexer.lexpos:])
            if m.group() == '':
                s+= str(t.lexer.lexdata[t.lexer.lexpos])
                t.lexer.skip(1)
            else:
                s += m.group()
                t.lexer.skip(len(m.group()))

        t.lexer.lineno += len(s.split('\n')) - 1
        if count > 0:
            self.errors.append("(" + str(t.lexer.lineno) + ", " + str(t.lexer.lexpos) + ") - LexicographicError: EOF in comment")




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
data = '''--Any characters between two dashes “--” and the next newline
--(or EOF, if there is no next newline) are treated as comments

(*(*(*
Comments may also be written by enclosing
text in (∗ . . . ∗). The latter form of comment may be nested.
Comments cannot cross file boundaries.
*)*)*)

class Error() {

        (* There was once a comment,
         that was quite long.
         But, the reader soon discovered that
         the comment was indeed longer than
         previously assumed. Now, the reader
         was in a real dilemma; is the comment
         ever gonna end? If I stop reading, will
         it end?
         He started imagining all sorts of things.
         He thought about heisenberg's cat and how
         how that relates to the end of the sentence.
         He thought to himself "I'm gonna stop reading".
         "If I keep reading this comment, I'm gonna know
         the fate of this sentence; That will be disastorous."
         He knew that such a comment was gonna extend to
         another file. It was too awesome to be contained in
         a single file. And he would have kept reading too...
         if only...
         cool wasn't a super-duper-fab-awesomest language;
         but cool is that language;
         "This comment shall go not cross this file" said cool.
         Alas! The reader could read no more.
         There was once a comment,
         that was quite long.
         But, the reader soon discovered that
         the comment was indeed longer than
         previously assumed. Now, the reader
         was in a real dilemma; is the comment
         ever gonna end? If I stop reading, will
         it end?
         He started imagining all sorts of things.
         He thought about heisenberg's cat and how
         how that relates to the end of the sentence.
         He thought to himself "I'm gonna stop reading".
         "If I keep reading this comment, I'm gonna know
         the fate of this sentence; That will be disastorous."
         He knew that such a comment was gonna extend to
         another file. It was too awesome to be contained in
         a single file. And he would have kept reading too...
         if only...
         cool wasn't a super-duper-fab-awesomest language;
         but cool is that language;
         "This comment shall go not cross this file" said cool.
         Alas! The reader could read no more.''' 
lexer = Lexer(data)
lexer.execute()
lexer.print_errors()
print(len(data))
##### borrar luego ########################################