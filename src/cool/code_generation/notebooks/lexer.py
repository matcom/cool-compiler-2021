from cmp.ast import AtomicNode, BinaryNode, UnaryNode
from cmp.automata import State
from cmp.pycompiler import Grammar
from cmp.tools.automata import (
    DFA,
    NFA,
    automata_closure,
    automata_concatenation,
    automata_minimization,
    automata_union,
    nfa_to_dfa,
)
from cmp.tools.evaluation import evaluate_parse
from cmp.tools.parsing import metodo_predictivo_no_recursivo
from cmp.utils import Token


class EpsilonNode(AtomicNode):
    def evaluate(self):
        return DFA(states=1, finals=[0], transitions={})


class SymbolNode(AtomicNode):
    def evaluate(self):
        s = self.lex
        return DFA(states=2, finals=[1], transitions={(0, s): 1})


class ClosureNode(UnaryNode):
    @staticmethod
    def operate(value):
        return automata_closure(value)


class UnionNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_union(lvalue, rvalue)


class ConcatNode(BinaryNode):
    @staticmethod
    def operate(lvalue, rvalue):
        return automata_concatenation(lvalue, rvalue)


def regex_tokenizer(text, G, skip_whitespaces=True):
    tokens = []
    fixed_tokens = {x: Token(x, G[x]) for x in ["|", "*", "(", ")", "ε"]}
    iter_text = iter(text)
    for c in iter_text:
        if c == "\\":
            tokens.append(Token(next(iter_text), G["symbol"]))
            continue

        if skip_whitespaces and c.isspace():
            continue

        try:
            token = fixed_tokens[c]
        except KeyError:
            token = Token(c, G["symbol"])
        tokens.append(token)
    tokens.append(Token("$", G.EOF))
    return tokens


def build_grammar():
    G = Grammar()
    E = G.NonTerminal("E", True)
    T, F, A, X, Y, Z = G.NonTerminals("T F A X Y Z")
    pipe, star, opar, cpar, symbol, epsilon = G.Terminals("| * ( ) symbol ε")
    E %= T + X, lambda h, s: s[2], None, lambda h, s: s[1]
    X %= pipe + E, lambda h, s: UnionNode(h[0], s[2])
    X %= G.Epsilon, lambda h, s: h[0]
    T %= F + Y, lambda h, s: s[2], None, lambda h, s: s[1]
    Y %= T, lambda h, s: ConcatNode(h[0], s[1])
    Y %= G.Epsilon, lambda h, s: h[0]
    F %= A + Z, lambda h, s: s[2], None, lambda h, s: s[1]
    Z %= star, lambda h, s: ClosureNode(h[0])
    Z %= G.Epsilon, lambda h, s: h[0]
    A %= symbol, lambda h, s: SymbolNode(s[1])
    A %= epsilon, lambda h, s: EpsilonNode(s[1])
    A %= opar + E + cpar, lambda h, s: s[2]
    return G


G = build_grammar()
parser = metodo_predictivo_no_recursivo(G)


class Regex:
    def __init__(self, regex, skip_whitespaces=False):
        self.regex = regex
        self.automaton = self.build_automaton(regex)

    def __call__(self, text):
        return self.automaton.recognize(text)

    @staticmethod
    def build_automaton(regex, skip_whitespaces=False):
        tokens = regex_tokenizer(regex, G, skip_whitespaces=False)
        left_parse = parser(tokens)
        ast = evaluate_parse(left_parse, tokens)
        nfa = ast.evaluate()
        dfa = nfa_to_dfa(nfa)
        dfa = automata_minimization(dfa)
        return dfa


class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()

    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            automaton = Regex.build_automaton(regex)
            automaton, states = State.from_nfa(automaton, get_states=True)

            for state in states:
                if state.final:
                    state.tag = (n, token_type)

            regexs.append(automaton)
        return regexs

    def _build_automaton(self):
        start = State("start")
        regexs = self.regexs

        for regex in regexs:
            start.add_epsilon_transition(regex)

        return start.to_deterministic()

    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ""

        for symbol in string:
            try:
                state = state[symbol][0]
                lex += symbol
                final, final_lex = (state, lex) if state.final else (final, final_lex)
            except TypeError:
                break

        return final, final_lex

    def _tokenize(self, text):
        while text:
            state, lex = self._walk(text)

            if state is not None:
                text = text[len(lex) :]
                token_type = min(
                    (s for s in state.state if s.final), key=lambda x: x.tag
                ).tag[1]
                yield lex, token_type

            else:
                return None

        yield "$", self.eof

    def __call__(self, text):
        return [Token(lex, token_type) for lex, token_type in self._tokenize(text)]
