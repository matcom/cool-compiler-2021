literals=[
    'SEMI',     # ;
    'COLON',    # :
    'COMMA',    # , 
    'DOT',      # .
    'OPAR',     # (
    'CPAR',     # )
    'OCUR',     # {
    'CCUR',     # }
    'LARROW',   # <-
    'ARROBA',   # @
    'RARROW',   # =>
    'NOX',      # ~
    'EQUAL',    # =
    'PLUS',     # +
    'MINUS',    # -
    'STAR',     # *
    'DIV',      # /
    'LESS',     # <
    'LESSEQ',   # <=
    'ID',    
    'TYPE',    
    'NUMBER',
    'STRING'
]

reserved = {
    'isvoid' : 'isvoid',
    'not' : 'not',
    'if' : 'if',
    'else' : 'else',
    'then' : 'then',
    'fi' : 'fi',
    'class' : 'class',
    'inherits' : 'inherits',
    'while' : 'while',
    'loop' : 'loop',
    'pool' : 'pool',
    'let' : 'let',
    'in' : 'in',
    'case' : 'case',
    'esac' : 'esac',
    'of' : 'of',
    'new' : 'new',
    'true': 'true',
    'false':'false'

 }

tokens = list(reserved.values()) + literals

class Token:
    def __init__(self, line: int, column: int, type: str, value: str) -> None:
       self.line = line
       self.column = column
       self.type = type
       self.value = value

    def __str__(self) -> str:
        return f'{self.type} {self.value} {self.line} {self.column}' 
    

    def __repr__(self):
        return str(self)