from cmp.ast import Node, AtomicNode, UnaryNode, BinaryNode
from cmp.utils import Token
from cmp.pycompiler import (EOF, Epsilon, Grammar, NonTerminal, Production,
                            Sentence, SentenceList, Symbol, Terminal)
from lib.utils.automaton import *
from lib.parser.parser_ll1 import ParserLL1


G = Grammar()

EPSILON = 'ε'

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z, R, Q = G.NonTerminals('T F A X Y Z R Q')
pipe, star, opar, cpar, symbol, epsilon, plus, qtn, obra, cbra = G.Terminals(f'| * ( ) symbol {EPSILON} + ? [ ]')

# Your code here!!!
E %= T + X, lambda h,s: s[2], None,lambda h,s: s[1]

X %= pipe + T + X, lambda h,s: UnionNode(h[0],s[3]), None, None,lambda h,s: s[2]
X %= G.Epsilon, lambda h,s: h[0]

T %= A + Y, lambda h,s: s[2], None,lambda h,s: s[1]

Y %= A + Y, lambda h,s: ConcatNode(h[0],s[2]), None,lambda h,s: s[1]
Y %= G.Epsilon, lambda h,s: h[0]

A %= Z + F, lambda h,s: s[2] ,None ,lambda h,s: s[1]

F %= star + F, lambda h,s: s[2], None, lambda h,s: ClosureNode(h[0])
F %= plus + F, lambda h,s: s[2],None,lambda h,s: PlusNode(h[0])
F %= qtn + F, lambda h,s: s[2], None, lambda h,s: QuestionNode(h[0])
F %= G.Epsilon, lambda h,s: h[0]

R %= A + Q, lambda h,s: s[2], None,lambda h,s: s[1]

Q %= A + Q, lambda h,s: UnionNode(h[0],s[2]), None, lambda h,s: s[1]
Q %= G.Epsilon, lambda h,s: h[0]

Z %= symbol, lambda h,s: SymbolNode(s[1]), None
Z %= opar + E + cpar, lambda h,s: s[2], None, None, None
Z %= obra + R + cbra, lambda h,s: s[2], None, None, None
Z %= epsilon, lambda h,s: EpsilonNode(s[1]), None


regex_parser = ParserLL1(G)

class EpsilonNode(AtomicNode):
    def evaluate(self):
        automata = NFA(1,{0},{},0)
        return '',automata

class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        # Your code here!!!
        automata = NFA(2,{1},{(0,s):[1]},0)
        return f'{s}',automata

class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        # Your code here!!!
        return f'({value[0]})*',automata_closure(value[1])

class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return f'({lvalue[0]}|{rvalue[0]})',automata_union(lvalue[1],rvalue[1])

class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        # Your code here!!!
        return f'{lvalue[0]}{rvalue[0]}',automata_concatenation(lvalue[1],rvalue[1])

class PlusNode(UnaryNode):
    @staticmethod
    def operate(value):
        # Your code here!!!
        return f'({value[0]})+',automata_concatenation(value[1],automata_closure(value[1])) 

class QuestionNode(UnaryNode):
    @staticmethod
    def operate(value):
        # Your code here!!!
        epsilon = NFA(1,{0},{},0)
        return f'({value[0]})?',automata_union(value[1],epsilon) 

fixed_tokens = {
        '*'     : Token('*'     , star),
        '('     : Token('('     , opar),
        ')'     : Token(')'     , cpar),
        '|'     : Token('|'     , pipe),
        '?'     : Token('?'     , qtn),
        '+'     : Token('+'     , plus),
        '['     : Token('['     , obra),
        ']'     : Token(']'     , cbra),
        EPSILON : Token(EPSILON , epsilon),
    }

def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    # > fixed_tokens = ???
    # Your code here!!!
    
    skip = False
    for i, char in enumerate(text):
        
        if skip:
            skip = False
            continue
        
        if skip_whitespaces and char.isspace():
            continue
        # Your code here!!!
        if char == '\\':
            try:
                tokens.append(Token(text[i+1],symbol))
            except IndexError:
                tokens.append(Token('\\',symbol))
            skip = True
            continue
                        
        try:
            tokens.append(fixed_tokens[char])
        except KeyError:
            tokens.append(Token(char,symbol))
        
    tokens.append(Token('$', G.EOF))
    return tokens

def regex_automaton(regex,skip_whitespces=False,return_regex = False):
    """
    returns the minimal dfa that recognize regex
    """
    tokens = regex_tokenizer(regex,G,skip_whitespces)
    errors = []
    regex,nfa = regex_parser.evaluate(tokens,errors)
    if nfa:
        dfa = nfa_to_dfa(nfa)
        mini = automata_minimization(dfa)
        if return_regex:
            return mini,regex
        return mini
    return None