import re

class Token:
    def __init__(self, token):
        self.type = token.type
        self.line = token.lineno
        self.value = token.value
        self.column = Token.find_column(token)

    @staticmethod
    def find_column(token):
        line_star = token.lexer.lexdata.rfind('\n', 0, token.lexpos) + 1
        line_tab = len(re.findall('\t', token.lexer.lexdata[line_star: token.lexpos]))*3
        return token.lexpos - line_star + 1 + line_tab