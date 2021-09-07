import ply.lex as lex
import re
from ..cmp.grammar import G


class CoolLexer(object):

    __init__(self):
        self.count = 0
        self.build()

    states = (
        ('string','exclusive'),
        ('comment','exclusive'),
    )

    reserved = {
        'class': 'CLASS',
        'inherits': 'INHERITS',
        'let': 'LET',
        'in': 'IN',
        'case': 'CASE',
        'of': 'OF',
        'esac': 'ESAC',
        'while': 'WHILE',
        'loop': 'LOOP',
        'pool': 'POOL',
        'if': 'IF',
        'then': 'THEN',
        'else': 'ELSE',
        'fi': 'FI',
        'isvoid': 'ISVOID',
        'not': 'NOT',
        'new': 'NEW',
        'true': 'TRUE',
        'false': 'FALSE'
    }

    tokens = [
        'SEMICOLON',
        'COLON',
        'COMMA',
        'DOT',
        'OPAR',
        'CPAR',
        'OCUR',
        'CCUR',
        'LARROW',
        'RARROW',
        'AT',
        'EQUAL',
        'PLUS',
        'MINUS',
        'STAR',
        'DIV',
        'LESS',
        'LEQ',
        'NEG',
        'TYPEIDENTIFIER',
        'OBJECTIDENTIFIER',
        'NUMBER',
        'STRING'
    ] + list(reserved.values())

    token_type = {
        'CLASS' : G.classx,
        'INHERITS' : G.inherits,
        'LET' : G.let,
        'IN' : G.inx,
        'CASE': G.case,
        'OF': G.of,
        'ESAC': G.esac,
        'WHILE': G.whilex,
        'LOOP': G.loop,
        'POOL': G.pool,
        'IF': G.ifx,
        'THEN': G.then,
        'ELSE': G.elsex,
        'FI': G.fi,
        'ISVOID': G.isvoid,
        'NOT': G.notx,
        'NEW': G.new,
        'TRUE': G.boolx,
        'FALSE': G.boolx,
        'SEMICOLON': G.semi,
        'COLON': G.colon,
        'COMMA': G.comma,
        'DOT': G.dot,
        'OPAR': G.opar,
        'CPAR': G.cpar,
        'OCUR': G.ocur,
        'CCUR': G.ccur,
        'LARROW': G.larrow,
        'RARROW': G.rarrow,
        'AT': G.at,
        'EQUAL': G.equal,
        'PLUS': G.plus,
        'MINUS': G.minus,
        'STAR': G.star,
        'DIV': G.div,
        'LESS': G.less,
        'LEQ': G.leq,
        'NEG': G.neg,
        'TYPEIDENTIFIER': G.typeid,
        'OBJECTIDENTIFIER': G.objectid,
        'NUMBER': G.num,
        'STRING': G.stringx
    }

    def t_NUMBER(t):
        r'\d+'
        t.value = int(t.value)
        self.add_column(t)
        return t

    # Define a rule so we can track line numbers
    def t_newline(t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        self.count = t.lexpos + len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t\f\r\v'

    def t_COMMENTLINE(self, t):
        r'--.*'

    def t_TYPEIDENTIFIER(self, t):
        r'[A-Z][0-9A-Za-z_]*'
        val = t.value.lower()
        if val not in ['true', 'false']:
            t.type = self.reserved.get(val, 'TYPEIDENTIFIER')
        self.add_column(t)
        return t

    def t_OBJECTIDENTIFIER(self, t):
        r'[a-z][0-9A-Za-z_]*'
        val = t.value.lower()
        t.type = self.reserved.get(val, 'OBJECTIDENTIFIER')
        self.add_column(t)
        return t
         
    def t_SEMICOLON(self, t):
        r';'
        self.add_column(t)
        return t

    def t_COLON(self, t):
        r':'
        self.add_column(t)
        return t

    def t_COMMA(self, t):
        r','
        self.add_column(t)
        return t
    
    def t_DOT(self, t):
        r'\.'
        self.add_column(t)
        return t
    
    def t_OPAR(self, t):
        r'\('
        self.add_column(t)
        return t
    
    def t_CPAR(self, t):
        r'\)'
        self.add_column(t)
        return t

    def t_OCUR(self, t):
        r'{'
        self.add_column(t)
        return t

    def t_CCUR(self, t):
        r'}'
        self.add_column(t)
        return t

    def t_LARROW(self, t):
        r'<-'
        self.add_column(t)
        return t

    def t_RARROW(self, t):
        r'=>'
        self.add_column(t)
        return t

    def t_AT(self, t):
        r'@'
        self.add_column(t)
        return t

    def t_EQUAL(self, t):
        r'='
        self.add_column(t)
        return t

    def t_PLUS(self, t):
        r'\+'
        self.add_column(t)
        return t

    def t_MINUS(self, t):
        r'-'
        self.add_column(t)
        return t

    def t_STAR(self, t):
        r'\*'
        self.add_column(t)
        return t

    def t_DIV(self, t):
        r'/'
        self.add_column(t)
        return t

    def t_LESS(self, t):
        r'<'
        self.add_column(t)
        return t

    def t_LEQ(self, t):
        r'<='
        self.add_column(t)
        return t

    def T_NEG(self, t):
        r'~'
        self.add_column(t)
        return t


    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


    def add_column(self, t):
        t.col = t.lexpos - self.count

