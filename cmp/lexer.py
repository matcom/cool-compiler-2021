from cmp.utils import Token, tokenizer
from cmp.grammar import *

fixed_tokens = { t.Name: Token(t.Name, t) for t in G.terminals if t not in { idx, num, stringx, boolx }}

# @tokenizer(G, fixed_tokens)
# def tokenize_text(token):
#     lex = token.lex
#     try:
#         float(lex)
#         return token.transform_to(num)
#     except ValueError:
#         if lex[0] == '"' and lex[-1] == '"':
#             return token.transform_to(stringx)
#         if lex == 'true' or lex == 'false':
#             return token.transform_to(boolx)
#         return token.transform_to(idx)

def pprint_tokens(tokens, get=False):
    indent = 0
    pending = []
    result = ''
    for token in tokens:
        pending.append(token)
        if token.token_type in { ocur, ccur, semi }:
            if token.token_type == ccur:
                indent -= 1
            if get:
                result += '    '*indent + ' '.join(str(t.token_type) for t in pending) + '\n'
            else:
                print('    '*indent + ' '.join(str(t.token_type) for t in pending))
            pending.clear()
            if token.token_type == ocur:
                indent += 1
    if get:
        result += ' '.join([str(t.token_type) for t in pending]) + '\n'
        return result
    else:
        print(' '.join([str(t.token_type) for t in pending]))


from cmp.utils import Token
from cmp.regex import Regex
from cmp.automata import State


class Lexer:
    def __init__(self, table, eof):
        self.eof = eof
        self.regexs = self._build_regexs(table)
        self.automaton = self._build_automaton()
    
    def _build_regexs(self, table):
        regexs = []
        for n, (token_type, regex) in enumerate(table):
            dfa = Regex(regex)
            automaton_list = State.from_nfa(dfa.automaton, 'texto random pra que haga lo que quiero')
            for i in automaton_list[1]:
                if(i.final):
                    i.tag = (n, token_type)
            regexs.append(automaton_list[0])
                
        return regexs
    
    def _build_automaton(self):
        start = State('start')
        automatons = self.regexs
        for i in automatons:
            start.add_epsilon_transition(i)
        final = start.to_deterministic()
        return final
    
        
    def _walk(self, string):
        state = self.automaton
        final = state if state.final else None
        final_lex = lex = ''
        
        for symbol in string:
            try:
                state = state[symbol][0]
                lex += symbol
                if(state.final):
                    final = state
                    final_lex = lex
            except TypeError:
                # print(symbol, lex, string, state)
                break
                
        return final, final_lex
    
    def _tokenize(self, text):
        pos = 0
        while(len(text) > 0):
            temp = self._walk(text)
            # print(temp)
            
            if(temp[1] == ''):
                assert 1, 0
                
            pos = len(temp[1])
            text = text[pos:len(text)]
            mi = 9999
            final = None
            for i in temp[0].state:
                if i.final:
                    if i.tag[0] <  mi:
                        final = i
                        mi = i.tag[0]
            yield temp[1], final.tag[1]
        
        yield '$', self.eof
    
    def __call__(self, text):
        return [ Token(lex, ttype) for lex, ttype in self._tokenize(text) ]


nonzero_digits = '|'.join(str(n) for n in range(1,10))
alp = [chr(n) for n in range(ord('a'),ord('z') + 1)]
alp.extend([chr(n) for n in range(ord('A'),ord('Z') + 1)])
letters = '|'.join(alp)

alphabet_before = [chr(n) for n in range(1, ord('~') + 1) if n != 34 and n != 124]
alphabet = '|'.join(alphabet_before)

def eliminate_regex_conflict(text):
    result = ''
    for i in text:
        if i in {'(', ')', '*', '\\'}:
            result += '\\'
        result += i
    return result


def tokenize_text(text):
    lexer = Lexer(
        [(t, eliminate_regex_conflict(t.Name)) for t in G.terminals if t not in { idx, num, stringx, boolx }] +
        [(boolx, 'true|false'),
        (num, f'0|({nonzero_digits})(0|{nonzero_digits})*'),
        ('salto', '\n'),
        ('space', '  *'),
        (idx, f'({letters}|_)(_|{letters}|0|{nonzero_digits})*'),
        (stringx, f'"({eliminate_regex_conflict(alphabet)})*"')],
        G.EOF)
    
    tokens = lexer(text)
    # print('tokens', tokens)
    tokens_filtrado = []
    for i in tokens:
        if i.token_type != 'salto' and i.token_type != 'space':
            tokens_filtrado.append(i)
    # print('tokens filtrados', tokens_filtrado)
    return tokens_filtrado