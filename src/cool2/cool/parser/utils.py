from cmp.pycompiler import Production
from lib.lang.language_lr import LanguageLR,LR1Parser,LALR1Parser
import pickle

def save_parser(path,G):
    pType = G.pType
    G.pType = Production
    attributes = []
    for prod in G.Productions:
        attributes.append(prod.attributes)
        prod.__delattr__('attributes')
    parser = LALR1Parser(G)
    with open(path,'wb') as f:
        pickle.dump(parser,f,pickle.HIGHEST_PROTOCOL)
    for prod,attr in zip(parser.grammar.Productions,attributes): 
        prod.attributes = attr
    G.pType = pType
    return parser

def load_parser(path,G):
    with open(path,'rb') as f:
        parser = pickle.load(f)
        for prod,prod2 in zip(parser.grammar.Productions,G.Productions):
            prod.attributes = prod2.attributes
    return parser
