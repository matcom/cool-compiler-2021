import ply.lex as lex

class COOL_Lexer:
    tokens = [
        'OBJECTID', # object identifiers
        'TYPEID', # type identifiers
        'INT_CONST', # integer constants 
        'STRING_CONST', # string constants

        #symbols
        'DOT', #.
        'COMMA', #,
        'COLON', #:
        'SEMICOLON', #;
        'AT', #@
        'TILDE', #~
        'PLUS', #+
        'MINUS', #-
        'STAR', #*
        'DIV', #/
        'LEQ', #<=
        'LOWER', #<
        'EQUAL', #=
        'ASSIGN', #<-
        'CASSIGN', #=>
        'OPAR', #(
        'CPAR', #)
        'OCUR', #{
        'CCUR', #}
    ]
    
    keywords = {
        'class' : 'CLASS',
        'else' : 'ELSE',
        'false' : 'FALSE',
        'fi' : 'FI',
        'if' : 'IF',
        'in' : 'IN',
        'inherits' : 'INHERITS',
        'isvoid' : 'ISVOID',
        'let' : 'LET',
        'loop' : 'LOOP',
        'pool' : 'POOL',
        'then' : 'THEN',
        'while' : 'WHILE',
        'case' : 'CASE',
        'esac' : 'ESAC',
        'new' : 'NEW',
        'of' : 'OF',
        'not' : 'NOT',
        'true' : 'TRUE'
    }

    tokens += list(keywords.values())

    def __init__(self):
        self.errors = []
        self.prev_last_newline = 0
        self.current_last_newline = 0
    
    def build(self):
        self.lexer = lex.lex(module=self)

    def tokenize(self, text):
        self.last_newline = 0
        self.lexer.input(text)
        for t in self.lexer:
            t.lexpos = t.lexpos - self.prev_last_newline + 1
            self.prev_last_newline = self.current_last_newline
            yield t

    ######################################################################
    #                           Literals                                 #
    ######################################################################
    t_INT_CONST = r'[0-9]+'

    def t_OBJECTID(self, t):
        r'[a-z][a-zA-Z0-9_]*' # object identifiers must start with lower case
        t.type = self.keywords.get(t.value.lower(), 'OBJECTID') # try match with keywords that also match the objectid pattern
        return t

    def t_TYPEID(self, t):
        r'[A-Z][a-zA-Z0-9_]*' # type identifiers must start with upper case
        val = t.value.lower()
        if val != 'true' and val != 'false': # discard `lower` and `false` that start with lower case
            t.type = self.keywords.get(val, 'TYPEID')
        return t

    def t_STRING_CONST(self, t):
        r'\"' # match the first "
        value = '\"'
        text = t.lexer.lexdata
        pos = t.lexer.lexpos

        contains_null = False
        while True:
            if pos >= len(text): # founded EOF before closing "
                t.lexer.lexpos = pos
                self.register_error(t.lexer.lineno, t.lexer.lexpos - self.current_last_newline + 1, "LexicographicError: EOF in string constant")
                return
            c = text[pos]

            if c == '\\':
                if text[pos+1] == '\n':
                    value += '\n'
                    t.lexer.lineno += 1 
                    self.current_last_newline = pos + 2
                elif text.startswith('\r\n', pos+1):
                    value += '\r\n'
                    t.lexer.lineno += 1 
                    pos+=1
                    self.current_last_newline = pos + 1
                elif text[pos+1] in ('b', 'f', 't', 'n'): # i'm not very sure about this
                    value += f'\\{text[pos+1]}'
                else:
                    value += text[pos+1]
                pos += 2
            elif c == '\n': # string with no scaped \n# try match with false or true that also match the identifier pattern and have higher precedence
                t.lexer.lexpos = pos
                self.register_error(t.lineno, t.lexer.lexpos - self.current_last_newline + 1, "LexicographicError: Unterminated string constant")
                return
            elif c == '\0':
                contains_null = True
                self.register_error(t.lineno, pos - self.current_last_newline + 1, "LexicographicError: String contains null character")
                pos += 1
            else:
                value += c
                pos += 1
                if c == '\"':
                    break
            
        t.lexer.lexpos = pos
        t.value = value
        t.type = 'STRING_CONST'
        if not contains_null:
            return t

    #######################################################################
    #                            Comments                                 #
    #######################################################################

    def t_SINGLE_LINE_COMMENT(self, t):
        r'--'
        value = '--'
        text = t.lexer.lexdata
        pos = t.lexer.lexpos

        while True:
            if pos >= len(text):
                break
            if text[pos] == '\n':
                t.lexer.lineno += 1
                value += text[pos]
                pos+=1
                self.current_last_newline = pos
                break
            value += text[pos]
            pos+=1
        
        t.lexer.lexpos = pos

    def t_MULTI_LINE_COMMENT(self, t):
        r'\(\*'
        opar = 1
        value = '(*'
        text = t.lexer.lexdata
        pos = t.lexer.lexpos

        while opar > 0:
            if pos >= len(text):
                t.lexer.lexpos = pos
                self.register_error(t.lexer.lineno, t.lexer.lexpos - self.current_last_newline, 'LexicographicError: EOF in comment')
                return
            
            if text.startswith('(*', pos):
                value += '(*'
                pos += 2
                opar += 1
            elif text.startswith('*)', pos):
                opar -= 1
                pos +=2 
                value += '*)'
            else:
                if text[pos] == '\n':
                    t.lexer.lineno += 1
                    self.current_last_newline = pos
                value += text[pos]
                pos += 1
        t.lexer.lexpos = pos

    #######################################################################
    #                               Symbols                               #
    ####################################################################### 
    t_DOT = r'\.'
    t_COMMA = r','
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_AT = r'@'
    t_TILDE = r'~'
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_DIV = r'/'
    t_LEQ = r'<='
    t_LOWER = r'<'
    t_EQUAL = r'='
    t_ASSIGN = r'<-'
    t_CASSIGN = r'=>'
    t_OPAR = r'\('
    t_CPAR = r'\)'
    t_OCUR = r'{'
    t_CCUR = r'}'
    
    #######################################################################
    #                             Ignored                                 #
    #######################################################################     

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.prev_last_newline = t.lexer.lexpos
        self.current_last_newline = t.lexer.lexpos

    t_ignore = ' \t\r'

    ########################################################################
    #                           Error Handling                             #
    ######################################################################## 

    def t_error(self, t): # not recognized symbol
        self.register_error(t.lexer.lineno, t.lexer.lexpos - self.prev_last_newline + 1, f"LexicographicError: ERROR \"{t.value[0]}\"")
        t.lexer.skip(1)

    def register_error(self, line, column, text):
        self.errors.append(f'{line,column} - {text}')


