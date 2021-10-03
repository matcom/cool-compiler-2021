from .cool_lexer import CoolLexer


data = '''a(*(*(**)*)*)a*)e*)eeeee(*a*)'''
lexer = CoolLexer()
for tok in lexer.tokenize(data):
    print(tok)