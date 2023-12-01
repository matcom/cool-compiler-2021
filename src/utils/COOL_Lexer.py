import re

'''
Recibe como parametros el lexema, tipo, linea y columna donde se encuentra
'''


class Token:

    def __init__(self, lex, ttype, line, column):

        self.lex = lex
        self.token_type = ttype
        self.line = line
        self.column = column
        self.next_token = None

    def __str__(self):
        return f'({self.line}, {self.column}) - {self.token_type}: {self.lex}'


'''
El lexer es el resultado de la union de todas las expresiones regulares que forman
el lenguaje
'''


class Lexer:

    def __init__(self, table, keywords, ignored_tokens, tokens_toFix, eof):
        self.line = 1
        self.column = 0
        self.table = table
        self.keywords = keywords
        self.ignored_tokens = ignored_tokens
        self.tokens_toFix = tokens_toFix
        self.regex = self._build_regex(table)
        self.errors = []
        self.eof = eof

    def tokenize(self, text):
        while len(text) > 0:

            match = self.regex.match(text)
            error_token = ''

            while not match:
                error_token += text[0]
                text = text[1:]
                if len(text) <= 0:
                    break
                match = self.regex.match(text)

            if error_token:
                self.errors.append(
                    f'({self.line}, {self.column + 1}) - LexicographicError: ERROR "{error_token}"')
                self.column += len(error_token)
                if len(text) <= 0:
                    continue

            lexeme = match.group()
            self.column += len(lexeme) if lexeme != '\t' else 4

            if lexeme == '\n':
                self.line += 1
                self.column = 0

            # COMMENTS
            elif lexeme == '(*':
                text = text[2:]
                openx = 1

                while len(text) > 0:
                    lexeme += text[0]
                    text = text[1:]
                    self.column += 1

                    if lexeme[-1] == '\n':
                        self.line += 1
                        self.column = 0

                    elif lexeme[-2:] == '(*':
                        openx += 1

                    elif lexeme[-2:] == '*)':
                        openx -= 1
                        if openx == 0:
                            break

                else:
                    self.errors.append(
                        f'({self.line}, {self.column + 1}) - LexicographicError: EOF in comment')

            # STRINGS
            elif lexeme == '"':
                text = text[1:]
                while len(text) > 0:
                    c = text[0]
                    text = text[1:]
                    self.column += 1

                    if c == '\\':
                        if text[0] == '\n':
                            lexeme += '\n'
                            self.line += 1
                            self.column = 0

                        elif text[0] == 'b':
                            lexeme += '\b'

                        elif text[0] == 't':
                            lexeme += '\t'

                        elif text[0] == 'n':
                            lexeme += '\n'

                        elif text[0] == 'f':
                            lexeme += '\f'

                        else:
                            lexeme += text[0]

                        text = text[1:]
                        self.column += 1

                    elif c == '\n':
                        self.errors.append(
                            f'({self.line}, {self.column}) - LexicographicError: Unterminated string constant')
                        self.line += 1
                        self.column = 0
                        break

                    elif c == '\0':
                        self.errors.append(
                            f'({self.line}, {self.column}) - LexicographicError: String contains null character')

                    else:
                        lexeme += c
                        if c == '"':
                            break

                else:
                    self.errors.append(
                        f'({self.line}, {self.column}) - LexicographicError: EOF in string constant')

            token_type = match.lastgroup if lexeme.lower(
            ) not in self.keywords and match.lastgroup is not None else match.group().lower()

            yield lexeme, token_type, self.line, self.column - len(lexeme) + 1

            text = text[match.end(
            ):] if lexeme[:2] != '(*' and lexeme[0] != '"' else text

        yield '$', self.eof, 0, 0

    def _build_regex(sef, table):
        return re.compile('|'.join([f'(?P<{name}>{regex})' if name != regex else f'({name})' for name, regex in table.items()]))

    def __call__(self, text):
        return [Token(lex, ttype, line, column) for lex, ttype, line, column in self.tokenize(text) if ttype not in self.ignored_tokens]

    def fixed_tokens(self, tokens):
        for i, token in enumerate(tokens[:(len(tokens) - 1)]):
            token.next_token = tokens[i+1]
        return tokens


'''
Esta clase guarda las propiedades sintacticas de COOL
'''


class COOL_Lexer(Lexer):
    def __init__(self):
        self.regexs = {
            'id': r'[a-z][a-zA-Z0-9_]*',
            'type': r'[A-Z][a-zA-Z0-9_]*',
            'string': r'\"',
            'int': r'\d+',
            'comment': r'(\(\*)|--.*',
            'newline': r'\n',
            'whitespace': r' +',
            'tabulation': r'\t',
            'inherits': r'inherits',
            'isvoid': r'isvoid',
            'class': r'class',
            'while': r'while',
            'false': r'false',
            'then': r'then',
            'else': r'else',
            'loop': r'loop',
            'pool': r'pool',
            'case': r'case',
            'esac': r'esac',
            'true': r'true',
            '<\-': r'<\-',
            'let': r'let',
            'new': r'new',
            'not': r'not',
            '\{': r'\{',
            '\}': r'\}',
            '\(': r'\(',
            '\)': r'\)',
            '\.': r'\.',
            '=>': r'=>',
            'if': r'if',
            'fi': r'fi',
            'in': r'in',
            'of': r'of',
            '\+': r'\+',
            '\-': r'\-',
            '\*': r'\*',
            '<=': r'<=',
            '\~': r'\~',
            ',': r',',
            ':': r':',
            ';': r';',
            '@': r'@',
            '/': r'/',
            '<': r'<',
            '=': r'='}

        self.keywords = ['inherits', 'isvoid', 'class', 'while', 'false', 'then', 'else', 'loop',
                         'pool', 'case', 'esac', 'true', 'let', 'new', 'not', 'if', 'fi', 'in', 'of']

        self.ignored_tokens = ['newline',
                               'whitespace', 'tabulation', 'comment']

        self.tokens_toFix = ['inherits', 'isvoid', 'class', 'while', 'then', 'else', 'loop', 'case',
                             'let', 'new', 'not', 'if', 'in', 'of', '<-']

        Lexer.__init__(self, self.regexs, self.keywords,
                       self.ignored_tokens, self.tokens_toFix, 'eof')
