class Token:
    def __init__(self, token):
        self.type = token.type
        self.line = token.lineno
        self.value = token.value
        self.column = Token.find_column(token)

    def __str__(self):
        return 'Token(%s, %s, %s, %s)'%(self.type, self.lex, self.line, self.column)

    @staticmethod
    def find_column(token):
        line_star = token.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        return token.lexpos - line_star + 1