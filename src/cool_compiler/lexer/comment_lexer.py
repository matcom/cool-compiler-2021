from sly import Lexer, lex

class CoolComment(Lexer):
    tokens = { TEXT }

    ignore_open = r'\(\*'
    ignore_close = r'\*\)'
    ignore_newline = r'\n'
    TEXT = r'.'

    def __init__(self, lexer ):
        self.lexer = lexer
        self.pos = 0
        self.count_new_line = 0
        self.s = 0
        self.len = 0
    
    def ignore_open(self, token):
        self.s += 1

    def ignore_close(self, token):
        self.s -= 1
        if not self.s > 0:
            self.index = self.len
            self.pos = token.index 
    
    def ignore_newline(self, token):
        self.count_new_line += 1
    
    def comment_analizer(self):
        text = self.lexer.text[self.lexer.index-2:]
        self.len = len(text)
        for last in self.tokenize(text):
            pass
        
        return self.s > 0, self.pos, self.count_new_line

    


