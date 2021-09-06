import ply.lex as lex




class CoolLexer:

    reserved = {
        'class': 'CLASS',
        'else': 'ELSE',
        'false': 'FALSE',
        'fi': 'FI',
        'if': 'IF',
        'in': 'IN',
        'inherits': 'INHERITS',
        'isvoid': 'ISVOID',
        'let': 'LET',
        'loop': 'LOOP',
        'pool': 'POOL',
        'then': 'THEN',
        'while': 'WHILE',
        'case': 'CASE',
        'esac': 'ESAC',
        'new': 'NEW',
        'of': 'OF',
        'not': 'NOT'
        'true': 'TRUE'
    }

    tokens = [
        'ID',
        'TYPE',
        'LPAREN',
        'RPAREN',
        'LBRACE',
        'RBRACE',
        'COLON',
        'SEMICOLON',
        'COMMA',
        'DOT',
        'AT',
        'ASSIGN',
        'PLUS',
        'MINUS',
        'STAR',
        'DIV',
        'EQUAL',
        'LESS',
        'LESSEQ',
        'ARROW',
        'INT',
        'STRING',
        'BOOLEAN',
        'NOT'
    ] + list(reserved.values())



    def find_column(self, t):
        line_start = self.text.rfind('\n', 0, t.lexpos) + 1
        return (t.lexpos - line_start) + 1

    def add_row_column(self, t):
        t.row = t.lexer.lineno
        t.column = self.find_column(t)






    def t_LPAREN(self, t):
        r'\('
        self.add_row_column(t)
        return t
    
    def t_RPAREN(self, t):
        r'\)'
        self.add_row_column(t)
        return t

    def t_LBRACE(self, t):
        r'\{'
        self.add_row_column(t)
        return t
    
    def t_RPAREN(self, t):
        r'\}'
        self.add_row_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.add_row_column(t)
        return t

    def t_SEMICOLON(self, t):
        r';'
        self.add_row_column(t)
        return t

    def t_DOT(self, t):
        r'\.'
        self.add_row_column(t)
        return t





