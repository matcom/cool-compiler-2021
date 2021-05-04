class LexicographicError:
    @staticmethod
    def text(line, column, text):
        return  '(%s, %s) - LexicographicError: %s'%(line, column, text)

class SyntacticError:
    @staticmethod
    def text(line, column, text):
        return  '(%s, %s) - SyntacticError: ERROR at or near "%s"'%(line, column, text)
    @staticmethod
    def text_eof():
        return '(0, 0) - SyntacticError: ERROR at or near "EOF"'