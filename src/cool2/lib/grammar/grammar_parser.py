from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal)
from cmp.ast import Node, AtomicNode, BinaryNode, TernaryNode
from cmp.utils import Token

G_parser = Grammar()
Q = G_parser.NonTerminal('Q', True)
non_terminals = G_parser.NonTerminals('L S X Z E K T N M')
L, S, X, Z, E, K, T, N, M = non_terminals
non_terminals = { x.Name:x for x in non_terminals }
non_terminals[Q.Name] = Q

terminals = G_parser.Terminals('pipe sym der end comma')
pipe, sym, der, end, comma = terminals
terminals = { x.Name:x for x in terminals }
terminals['eof'] = G_parser.EOF

symbols = non_terminals.copy()
symbols.update(terminals)

class GramConcatLines(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return lvalue + '\n' + rvalue

class GramNewProdNode(TernaryNode):
    @staticmethod
    def operate(lvalue, mvalue, rvalue):
        return lvalue + ' > ' + mvalue + rvalue

class GramConcatProdNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return ' | ' + lvalue + rvalue

class GramConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        if rvalue == '':
            return lvalue
        return  lvalue + ' ' + rvalue
    
class SymbolNode(AtomicNode):
    def evaluate(self):
        return self.lex


############################ BEGIN PRODUCTIONS ############################
# ======================================================================= #
Q %= E + end + T, lambda h,s: GramConcatLines(s[1],s[3])
T %= E + end + T, lambda h,s: GramConcatLines(s[1],s[3])
T %= G_parser.Epsilon, lambda h,s: SymbolNode('')
E %= sym + der + L, lambda h,s: s[3], None, None, lambda h,s: SymbolNode(s[1]) 
L %= S + X, lambda h,s: GramNewProdNode(h[0],s[1],s[2])
X %= pipe + S + X, lambda h,s: GramConcatProdNode(s[2],s[3]), None, None, lambda h,s: h[0]
X %= G_parser.Epsilon, lambda h,s: SymbolNode('')
S %= sym + K, lambda h,s: GramConcatNode(SymbolNode(s[1]),s[2])
K %= sym + K, lambda h,s: GramConcatNode(SymbolNode(s[1]),s[2])
K %= G_parser.Epsilon, lambda h,s: SymbolNode('')
# ======================================================================= #
############################# END PRODUCTIONS #############################

from lib.parser.parser_ll1 import ParserLL1
from lib.grammar.grammar_tokens import get_lexer_from_text,nonzero_digits,digits,min_letters,cap_letters,separator,regex_char_separator

# Grammar of the parser of Grammars
gram_parser = ParserLL1(G_parser)

expand = '~'

# Lexer of Grammar of the parser of Grammars
terms = f'sym{separator}[{min_letters}{cap_letters}_][_{min_letters}{cap_letters}{digits}]*{regex_char_separator}pipe{separator}\\|{regex_char_separator}end{separator};{regex_char_separator}der@{expand}{regex_char_separator}space{separator} *{regex_char_separator}comma{separator},{regex_char_separator}'
gram_lexer = None #get_lexer_from_text(terms,[]) ##############################

def fix_gram_text(gram_text,errors):
    gram_text = gram_text.replace('\n','')

    new_errors = []
    tokens = get_grammar_tokens(gram_text,new_errors)
    if new_errors:
        errors.append('Error getting the grammar tokens')
        errors.extend(new_errors)

    new_errors = []
    gramm = gram_parser.evaluate(tokens,new_errors)
    if new_errors:
        errors.append('Error evaluating the grammar definition')
        errors.extend(new_errors)

    return gramm

def get_grammar_from_text(gramm_text, errors):
    """
    returns a Grammar form gramm_text\n
    gramm_text: is the grammar written by the user\n
    NonTerminal_i ~ Production1_1 | ... | Production1_N;\n
    ...
    NonTerminal_j ~ ProductionQ_1 | ... | ProductionZ_P;\n
    """
    gramm_text = fix_gram_text(gramm_text,errors)
    if not gramm_text:
        return None
    
    G = Grammar()
    dic_sym = {}
    
    gramm = gramm_text.split('\n')
    index = 0

    distinguish = ''
    symbols = set()
    non_terminals = set()
    for s in gramm:
        if s:
            s = s.split(' > ')
            if not distinguish:
                distinguish = s[0]
            non_terminals.add(s[0])
            symbols.add(s[0])
            for ps in s[1].split(' | '):
                for q in ps.split(' '):
                    symbols.add(q)
    terminals = symbols.difference(non_terminals)
    non_terminals.remove(distinguish)
    S = G.NonTerminal(distinguish,True)
    dic_sym[distinguish] = S
    non_ter = ' '.join(non_terminals)
    non_ter = G.NonTerminals(non_ter)
    for x in non_ter:
        dic_sym[x.Name] = x
    ter = ' '.join(terminals)
    ter = G.Terminals(ter)
    for x in ter:
        dic_sym[x.Name] = x

    dic_sym.update({"epsilon":G.Epsilon, "$":G.EOF})
    
    s = gramm[index]
    index+=1
    while s != "":
        s = s.split(" > ")
        q = s[1].split(" | ")
        for prod in q:
            p = prod.split(" ")
            try:
                temp = dic_sym[p[0]]
            except KeyError:
                errors.append(f'{p[0]} is not defined in the terminals or in the non_terminals')
                break
            for ter in p[1:]:
                try:
                    temp += dic_sym[ter]
                except KeyError:
                    errors.append(f'{ter} is not defined in the terminals or in the non_terminals')
                    break
            try:
                dic_sym[s[0]] %= temp
            except TypeError:
                errors.append(f'A Non Terminal cant be left part of a production: {s}')
                break
        s = gramm[index]
        index+=1
    return G

def get_grammar_tokens(gram_def,errors:list):
    tokens = []
    for x in gram_lexer(gram_def):
        if x.token_type != 'space':
            try:
               tok = Token(x.lex,symbols[x.token_type])
               tokens.append(tok)
            except KeyError:
                errors.append(f'Unknown Token({x.lex},{x.token_type}) in gram_def')
    return tokens
