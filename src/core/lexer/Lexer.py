import ply.lex as lex
from core.tools.Utils import Token
from core.parser.Parser import CoolGrammar
from core.tools.Errors import LexicographicError

class Lexer:
    states = (
        ('comment', 'exclusive'),
        ('string', 'exclusive')
    )

    # Palabras reservadas del lenguaje COOL
    reserved = {
        'class': 'CLASS',
        'inherits': 'INHERITS',
        'function': 'FUNCTION',
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
        'isvoid': 'ISVOID'
    }

    t_ignore = ' \f\r\t\v'
    t_comment_ignore = ''
    t_string_ignore = ''

    tokens = [
                 # Identifiers
                 'TYPE', 'ID',
                 # Primitive data types
                 'INTEGER', 'STRING', 'BOOL',
                 # Special keywords
                 'ACTION',
                 # Operators
                 'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT', 'NOT',
                 # Literals
                 'PLUS', 'MINUS', 'STAR', 'DIVIDE', 'COLON', 'SEMICOLON',
                 'OPAR', 'CPAR', 'OCUR', 'CCUR', 'AT', 'DOT', 'COMMA',
             ] + list(reserved.values())

    tokens_dict = {}
    for tok in tokens:
        try:
            tokens_dict[tok] = CoolGrammar[tok.lower()].Name
        except:
            pass

    tokens_dict['ACTION'] = CoolGrammar['=>'].Name
    tokens_dict['ASSIGN'] = CoolGrammar['<-'].Name
    tokens_dict['LESS'] = CoolGrammar['<'].Name
    tokens_dict['LESSEQUAL'] = CoolGrammar['<='].Name
    tokens_dict['EQUAL'] = CoolGrammar['='].Name
    tokens_dict['INT_COMPLEMENT'] = CoolGrammar['~'].Name

    tokens_dict['PLUS'] = CoolGrammar['+'].Name
    tokens_dict['MINUS'] = CoolGrammar['-'].Name
    tokens_dict['STAR'] = CoolGrammar['*'].Name
    tokens_dict['DIVIDE'] = CoolGrammar['/'].Name
    tokens_dict['COLON'] = CoolGrammar[':'].Name
    tokens_dict['SEMICOLON'] = CoolGrammar[';'].Name
    tokens_dict['OPAR'] = CoolGrammar['('].Name
    tokens_dict['CPAR'] = CoolGrammar[')'].Name
    tokens_dict['OCUR'] = CoolGrammar['{'].Name
    tokens_dict['CCUR'] = CoolGrammar['}'].Name
    tokens_dict['AT'] = CoolGrammar['@'].Name
    tokens_dict['DOT'] = CoolGrammar['.'].Name
    tokens_dict['COMMA'] = CoolGrammar[','].Name


    def __init__(self):
        self.lexer = lex.lex(module=self)
        self.comment_level = 0
        self.code = ''
        self.current_string = ''
        self.errors = []


    # Expresiones regulares

    def t_INTEGER(self, t):
        r'[0-9]+'
        t.value = int(t.value)
        return t

    def t_BOOL(self, t):
        r't[rR][uU][eE]|f[aA][lL][sS][eE]'
        t.value = True if t.value == 'true' else False
        return t


    # Other tokens with precedence before TYPE and ID

    def t_NOT(self, t):
        r'[nN][oO][tT]'
        return t

    # Identifiers

    def t_TYPE(self, t):
        r'[A-Z][A-Za-z0-9_]*'

        try:
            t.type = self.reserved[t.value.lower()]
        except KeyError:
            pass

        return t

    def t_ID(self, t):
        r'[a-z][A-Za-z0-9_]*'

        try:
            t.type = self.reserved[t.value.lower()]
        except KeyError:
            pass

        return t


    t_ASSIGN = r'<-'
    t_LESS = r'<'
    t_LESSEQUAL = r'<='
    t_EQUAL = r'='
    t_INT_COMPLEMENT = r'~'
    t_ACTION = r'=>'

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_STAR = r'\*'
    t_DIVIDE = r'/'
    t_COLON = r':'
    t_SEMICOLON = r';'
    t_OPAR = r'\('
    t_CPAR = r'\)'
    t_OCUR = r'{'
    t_CCUR = r'}'
    t_AT = r'@'
    t_DOT = r'\.'
    t_COMMA = r','

    ####################
    ##### COMMENTS #####
    ####################
    def t_LINECOMMENT(self, t):
        r'--.*'
        pass

    def t_COMMENTBEGIN(self, t):
        r'\(\*'
        self.comment_level += 1
        t.lexer.begin('comment')

    def t_comment_COMMENTBEGIN(self, t):
        r'\(\*'
        self.comment_level += 1

    def t_comment_COMMENTEND(self, t):
        r'\*\)'
        self.comment_level -= 1
        if self.comment_level == 0:
            t.lexer.begin('INITIAL')

    def t_comment_eof(self, t):
        self.errors.append(LexicographicError(t.lineno,
                  self.find_column(t), 'EOF in comment'))
        self.lexer.begin('INITIAL')

    def t_comment_error(self, t):
        t.lexer.skip(1)

    ############################
    ##### STRING CONSTANTS #####
    ############################

    def t_STRINGBEGIN(self, t):
        r'"'
        self.current_string = ''
        self.lexer.begin('string')

    def t_string_NULL(self, t):
        r'\0'
        self.errors.append(LexicographicError(t.lineno,
                  self.find_column(t), 'Null caracter in string'))
        self.lexer.begin('INITIAL')

    def t_string_NEWLINE(self, t):
        r'\\\n'
        self.current_string += '\n'
        t.lexer.lineno += 1

    def t_string_INVALID_NEWLINE(self, t):
        r'\n'
        t.lexer.lineno += 1
        self.errors.append(LexicographicError(t.lineno,
                  self.find_column(t), 'Unterminated string constant'))
        self.lexer.begin('INITIAL')

    def t_string_SCAPED_SPECIAL_CHARACTER(self, t):
        r'\\(b|t|f)'
        self.current_string += t.value

    def t_string_SCAPED_CHARACTER(self, t):
        r'\\.'
        self.current_string += '\\' + t.value[1]

    def t_string_eof(self, t):
        self.errors.append(LexicographicError(t.lineno,
                  self.find_column(t), 'EOF in string constant'))
        self.lexer.begin('INITIAL')

    def t_string_STRINGEND(self, t):
        r'"'
        t.value = self.current_string
        t.type = 'STRING'
        self.lexer.begin('INITIAL')
        return t

    def t_string_CHARACTER(self, t):
        r'.'
        self.current_string += t.value

    def t_string_error(self, t):
        return t

    ###########################
    ###### SPECIAL RULES ######
    ###########################

    def t_ANY_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def find_column(self, token):
        line_start = self.code.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1 \
               + 3 * len([i for i in self.code[line_start:token.lexpos] if i == '\t'])

    def t_error(self, t):
        self.errors.append(LexicographicError(t.lineno,
                  self.find_column(t), f'ERROR "{t.value[0]}"'))
        t.lexer.skip(1)


    '''
    Dado un string retorna el arreglo de tokens resultante de analizar dicho string
    '''
    def tokenize(self, code):
        tokens = []
        self.code = code

        self.lexer.input(code)
        while True:
            token = self.lexer.token()
            if token is None:
                break

            tokens.append(Token(token.value, self.tokens_dict[token.type],
                                token.lineno, self.find_column(token)))

        tokens.append(Token('$', CoolGrammar.EOF.Name))

        return tokens
