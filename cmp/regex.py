from cmp.pycompiler import Grammar
from cmp.utils import Token
from cmp.tools2 import evaluate_parse
from cmp.tools2 import metodo_predictivo_no_recursivo
from cmp.tools2 import nfa_to_dfa
from cmp.tools2 import automata_union, automata_concatenation, automata_closure, automata_minimization
from cmp.tools2 import get_printer
from cmp.tools2 import Node, AtomicNode, UnaryNode, BinaryNode, EpsilonNode, SymbolNode, ClosureNode, UnionNode, ConcatNode
from pprint import pprint as pp
import pydot

class Regex:
    def __init__(self, regular_exp):

        self.regular_exp = regular_exp
        self.tokens = regex_tokenizer(regular_exp, G, False)
        self.left_parse = parser(self.tokens)
        self.ast = evaluate_parse(self.left_parse, self.tokens)
        self.nfa = self.ast.evaluate()
        self.dfa = nfa_to_dfa(self.nfa)
        self.mini = automata_minimization(self.dfa)
        self.automaton = self.mini

    def __call__(self, string):
        return self.mini.recognize(string)

    def __repr__(self):
        return 'Regex: ' + self.regular_exp


G = Grammar()

E = G.NonTerminal('E', True)
T, F, A, X, Y, Z = G.NonTerminals('T F A X Y Z')
pipe, star, opar, cpar, symbol, epsilon = G.Terminals('| * ( ) symbol ε')

# > PRODUCTIONS???
E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]

X %= pipe + T + X, lambda h, s: s[3], None, None, lambda h, s: UnionNode(h[0], s[2])
X %= G.Epsilon, lambda h, s: h[0]

T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]

Y %= F + Y, lambda h, s: s[2], None, lambda h, s: ConcatNode(h[0], s[1])
Y %= G.Epsilon, lambda h, s: h[0]

F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]

Z %= star + Z, lambda h, s: s[2], None, lambda h, s: ClosureNode(h[0])
Z %= G.Epsilon, lambda h, s: h[0]

A %= symbol, lambda h, s: SymbolNode(s[1])
A %= opar + E + cpar, lambda h, s: s[2], None, None, None
A %= epsilon, lambda h, s: EpsilonNode(s[1])



def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    jump = False

    # print(text)

    for char in text:
        if skip_whitespaces and char.isspace():
            continue
        elif(char == '\\' and not jump):
            jump = True
        elif(char == '*' and not jump):
            tokens.append(Token('*', star))
        elif(char == '(' and not jump):
            tokens.append(Token('(', opar))
        elif(char == ')' and not jump):
            tokens.append(Token(')', cpar))
        elif(char == '|' and not jump):
            tokens.append(Token('|', pipe))
        elif(char == 'ε' and not jump):
            tokens.append(Token('ε', epsilon))
        else:
            tokens.append(Token(char, symbol))
            jump = False

    tokens.append(Token('$', G.EOF))
    return tokens


parser = metodo_predictivo_no_recursivo(G)



printer = get_printer(AtomicNode=AtomicNode, UnaryNode=UnaryNode, BinaryNode=BinaryNode)
