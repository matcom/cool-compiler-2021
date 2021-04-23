from lib.lexer.lexer import DetailLexer as Lexer
import pickle

def save_lexer(table,path,G):
    with open(path,'wb') as f:
        attributes = []
        for prod in G.Productions:
            attributes.append(prod.attributes)
            prod.__delattr__('attributes')
        lexer = Lexer(table,G.EOF)
        pickle.dump(lexer,f,pickle.HIGHEST_PROTOCOL)
        for prod,attr in zip(G.Productions,attributes): 
            prod.attributes = attr
    return lexer

def load_lexer(path):
    with open(path,'rb') as f:
        lexer = pickle.load(f)
    return lexer
